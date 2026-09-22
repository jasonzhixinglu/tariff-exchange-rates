# -*- coding: utf-8 -*-
"""Task A: common external tariff baseline.

Baseline: A levies tau0 on all N-1 partners; partners symmetric, no tariffs of
their own.  Tariff changes are measured as t_j = d log(1+tau_Aj), which equals
d tau_Aj at tau0 = 0 (thresholds do not depend on this scaling).

Closed forms (derived in the memo, checked here against the exact model):
  baseline objects
    theta = tau0/(1+tau0)
    mu_A  = import share of A's tradable spending,  sigma_A = alpha_T mu_A
    mu_P  = import share of a partner's tradable spending
    omega = share of A's good in a partner's import bundle
    phi   = sigma_A / (1 - theta sigma_A)
    X     = f_Aj = f_jA,  Y = f_jk  (border flows),  x = X/(X+(N-1)Y)
  eigenvalues
    g_S = -X rho_D(tau0),   rho_D(tau0) = 1 - phi(1-theta) + (eta-1)(1-mu_A)(1+phi theta)
    g_D = -X rho
    j_S =  X M_S,   M_S = 1 + (eta-1)(1-mu_A)(1+phi theta) + (rho-1)(1-omega) + (eta-1)(1-mu_P) omega
    j_D =  (X+(N-1)Y) M_D,
          M_D = 1 + (rho-1)(N-3+omega)/(N-2) + (eta-1)(1-mu_P)(N-1-omega)/(N-2)
  bystander threshold (further tariff on B, or preferential cut for B)
    lambda_A = lambda_R  <=>  rho_D(tau0) M_D = x rho M_S
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import model as M
import style

HERE = os.path.dirname(__file__)
CAL = dict(aD=0.7, aT=0.6, eta=1.5)


def baseline(N, tau0, rho, aD=0.7, aT=0.6, eta=1.5):
    P = M.symmetric(N, aD=aD, aT=aT, eta=eta, rho=rho)
    T = np.zeros((N, N)); T[0, 1:] = tau0
    P = P.with_(tau=T)
    nu = M.solve(P)
    return P, nu


def objects(P, nu):
    N = P.N
    pc = M.pieces(M.full(nu), P)
    s, f = pc["s"], pc["f"]
    tau0 = P.tau[0, 1]
    theta = tau0 / (1 + tau0)
    sigA = s[0, 1:].sum()
    muA = sigA / P.aT[0]
    impP = s[1, [0] + list(range(2, N))].sum()
    muP = impP / P.aT[1]
    omega = s[1, 0] / impP
    phi = sigA / (1 - theta * sigA)
    X, Y = f[0, 1], (f[1, 2] if N > 2 else 0.0)
    return dict(theta=theta, muA=muA, muP=muP, omega=omega, phi=phi, X=X, Y=Y,
                x=X / (X + (N - 1) * Y), fA=f[1, 0])


def closed_form(o, N, rho, eta):
    rD = 1 - o["phi"] * (1 - o["theta"]) + (eta - 1) * (1 - o["muA"]) * (1 + o["phi"] * o["theta"])
    MS = (1 + (eta - 1) * (1 - o["muA"]) * (1 + o["phi"] * o["theta"])
          + (rho - 1) * (1 - o["omega"]) + (eta - 1) * (1 - o["muP"]) * o["omega"])
    MD = (1 + (rho - 1) * (N - 3 + o["omega"]) / (N - 2)
          + (eta - 1) * (1 - o["muP"]) * (N - 1 - o["omega"]) / (N - 2))
    X, Y = o["X"], o["Y"]
    return dict(gS=-X * rD, gD=-X * rho, jS=X * MS, jD=(X + (N - 1) * Y) * MD,
                rhoD_tau=rD, MS=MS, MD=MD)


def eigen_numeric(P, nu):
    N = P.N
    J, _, Gf = M.linearize(P, nu, logtariff=True)
    G = Gf[1:, 0, 1:]                       # partners' TB w.r.t. A's tariffs
    one = np.ones(N - 1)
    v = np.zeros(N - 1); v[0], v[1] = 1, -1
    return dict(gS=(G @ one)[0], gD=(G @ v)[0], jS=(-J @ one)[0], jD=(-J @ v)[0],
                sym_G=np.max(np.abs(G @ one - (G @ one)[0])),
                sym_J=np.max(np.abs(-J @ one - (-J @ one)[0])))


def gap(N, tau0, rho, **cal):
    """lambda_A - lambda_R at the tau0 baseline (sign of d nu_C for a further
    tariff on B)."""
    P, nu = baseline(N, tau0, rho, **cal)
    c = closed_form(objects(P, nu), N, rho, P.eta[0])
    return c["gS"] / c["jS"] - c["gD"] / c["jD"]


def threshold_local(N, tau0, **cal):
    rD = M.rhoD(cal.get("aD", .7), cal.get("aT", .6), cal.get("eta", 1.5))
    return brentq(lambda r: gap(N, tau0, r, **cal), 0.5 * N * rD, 3 * N * rD, xtol=1e-12)


def nuC_exact(N, tau0, rho, dB, **cal):
    """Exact log e_AC after moving tau_AB from tau0 to tau0 + dB, minus before."""
    P, nu = baseline(N, tau0, rho, **cal)
    T = P.tau.copy(); T[0, 1] = tau0 + dB
    nu1 = M.solve(P, T, nu0=nu)
    return nu1[1] - nu[1]


def threshold_exact(N, tau0, dB, rmax=60.0, **cal):
    """Smallest rho at which the exact bystander response changes sign;
    nan if none on (1, rmax]."""
    f = lambda r: nuC_exact(N, tau0, r, dB, **cal)
    rs = np.concatenate([np.linspace(1.05, 12, 45), np.linspace(12.5, rmax, 30)])
    vals = [f(r) for r in rs]
    for a, b, fa, fb in zip(rs[:-1], rs[1:], vals[:-1], vals[1:]):
        if np.sign(fa) != np.sign(fb):
            return brentq(f, a, b, xtol=1e-10)
    return float("nan")


if __name__ == "__main__":
    out = {}
    rD0 = M.rhoD(**{k: CAL[k] for k in ("aD", "aT", "eta")})
    # ---------------------------------------------------- 1. formula check
    worst = 0.0
    rows = []
    for N in (3, 4, 5):
        for tau0 in (0.0, 0.25, 0.5, 1.0):
            for rho in (1.5, 3.5, 7.0):
                P, nu = baseline(N, tau0, rho, **CAL)
                o = objects(P, nu)
                c = closed_form(o, N, rho, CAL["eta"])
                n = eigen_numeric(P, nu)
                err = max(abs(c[k] - n[k]) / abs(n[k]) for k in ("gS", "gD", "jS", "jD"))
                worst = max(worst, err, n["sym_G"], n["sym_J"])
                rows.append(dict(N=N, tau0=tau0, rho=rho, rel_err=err,
                                 lamA=n["gS"] / n["jS"], lamR=n["gD"] / n["jD"],
                                 MML=bool(n["jS"] > 0 and n["jD"] >= n["jS"])))
    print("closed-form eigenvalues vs exact model: max rel. error %.1e" % worst)
    out["eigen_check_max_rel_err"] = worst
    out["eigen_rows"] = rows

    # ---------------------------------------------------- 2. thresholds
    grid = np.linspace(0, 1, 21)
    th = {}
    for N in (3, 4, 5):
        th[N] = [threshold_local(N, t, **CAL) for t in grid]
        print("N=%d  rho*/(N rho_D): tau0=0 %.4f  0.5 %.4f  1 %.4f" %
              (N, th[N][0] / (N * rD0), th[N][10] / (N * rD0), th[N][-1] / (N * rD0)))
    out["grid"] = grid.tolist()
    out["local_threshold"] = {str(N): v for N, v in th.items()}

    # exact checks at N = 3: small further tariff (-> local), finite PTA cut
    chk = []
    for tau0 in (0.25, 0.5, 1.0):
        loc = threshold_local(3, tau0, **CAL)
        up = threshold_exact(3, tau0, 1e-4, **CAL)
        dn = threshold_exact(3, tau0, -1e-4, **CAL)
        pta = threshold_exact(3, tau0, -tau0, **CAL)          # full preferential cut
        chk.append(dict(tau0=tau0, local=loc, exact_up=up, exact_down=dn, exact_full_pta=pta))
        print("tau0=%.2f local %.5f | exact +1e-4 %.5f | exact -1e-4 %.5f | full PTA cut %.5f"
              % (tau0, loc, up, dn, pta))
    out["exact_checks"] = chk
    pta_grid = np.linspace(0.05, 1, 20)
    out["pta_grid"] = pta_grid.tolist()
    out["pta_exact_N3"] = [threshold_exact(3, t, -t, **CAL) for t in pta_grid]
    print("full PTA cut, exact rho*:", np.round(out["pta_exact_N3"], 3))

    # decomposition of the tau0 effect at N = 3, at the local threshold
    dec = []
    for tau0 in (0.0, 0.5, 1.0):
        r = threshold_local(3, tau0, **CAL)
        P, nu = baseline(3, tau0, r, **CAL)
        o = objects(P, nu)
        c = closed_form(o, 3, r, CAL["eta"])
        dec.append(dict(tau0=tau0, rho_star=r, rhoD_tau=c["rhoD_tau"], MS=c["MS"], MD=c["MD"],
                        x=o["x"], omega=o["omega"], muA=o["muA"], muP=o["muP"],
                        nu_common=float(nu[0])))
    out["decomposition_N3"] = dec
    for d in dec:
        print("  tau0=%.1f rho*=%.4f rhoD(tau0)=%.4f M_S=%.4f M_D=%.4f x=%.4f omega=%.4f nu0=%.4f"
              % (d["tau0"], d["rho_star"], d["rhoD_tau"], d["MS"], d["MD"], d["x"], d["omega"], d["nu_common"]))

    json.dump(out, open(os.path.join(HERE, "results", "task_a.json"), "w"), indent=1)

    # ---------------------------------------------------- figure
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    for N, c in zip((3, 4, 5), style.SERIES):
        ax.plot(grid, np.array(th[N]) / (N * rD0), color=c, lw=1.8, label="N = %d, local" % N)
    ax.plot(pta_grid, np.array(out["pta_exact_N3"]) / (3 * rD0), color=style.SERIES[0], lw=1.2,
            ls=(0, (4, 2)), label="N = 3, exact full cut on B")
    ax.axhline(1, color=style.MUTED, lw=0.8)
    ax.set_xlabel(r"common external tariff $\tau_0$")
    ax.set_ylabel(r"$\rho^\ast(\tau_0)\,/\,N\rho_D$")
    ax.legend(frameon=False, fontsize=8)
    style.finish(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figures", "task_a_threshold.png"), dpi=200)
    print("figure written")
