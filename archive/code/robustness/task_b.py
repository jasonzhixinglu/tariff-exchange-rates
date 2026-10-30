# -*- coding: utf-8 -*-
"""Task B: finite unilateral tariff and bilateral retaliation, N = 3, exact.

rho*(tau) solves log e_AC(tau; rho) = 0 in the exact model.
Local check: log e_AC = a(rho) tau + b_C tau^2 / 2 + O(tau^3), so near tau = 0
    rho*(tau) = rho*_0 + kappa tau,   kappa = -b_C / (2 a'(rho*_0)).
  unilateral:  a = (rho - 3 rho_D)/(6 M_3),  a' = 1/(6 M_3)  ->  kappa = -3 M_3 b_C
  retaliation: a = (rho - rho_D)/(2 M_3),    a' = 1/(2 M_3)  ->  kappa = -M_3 b_C
b_C is derived symbolically by second-order perturbation of the sympy model
at the symmetric free-trade baseline, and checked against finite differences
of the exact solver.
"""
import json
import os
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import model as M
import style

HERE = os.path.dirname(__file__)
CALS = {
    "baseline": dict(aD=0.7, aT=0.6, eta=1.5),
    "US-like": dict(aD=0.8, aT=0.4, eta=1.5),
    "low home bias, high eta": dict(aD=0.5, aT=0.6, eta=3.0),
}
SCEN = {"unilateral": [(0, 1)], "retaliation": [(0, 1), (1, 0)]}


def tariffs(scen, tau):
    T = np.zeros((3, 3))
    for (i, j) in SCEN[scen]:
        T[i, j] = tau
    return T


def nuC(cal, rho, scen, tau):
    P = M.symmetric(3, rho=rho, **cal)
    return M.solve(P, tariffs(scen, tau))[1]


def rho_star(cal, scen, tau, guess):
    f = lambda r: nuC(cal, r, scen, tau)
    lo, hi = guess * 0.6, guess * 1.6
    while f(lo) > 0:
        lo *= 0.8
    while f(hi) < 0:
        hi *= 1.3
        if hi > 200:
            return float("nan")
    return brentq(f, lo, hi, xtol=1e-11)


# ------------------------------------------------------------ symbolic b_C
def symbolic_bC(scen):
    """Second derivative of nu_C along the tariff path, at the symmetric
    free-trade baseline, as a function of (alpha_D, alpha_T, eta, rho)."""
    aD, aT, eta, rho = sp.symbols("alpha_D alpha_T eta rho", positive=True)
    z = sp.Symbol("z")
    TB, S = M.symbolic_model(3)
    path = {S["tau"][k]: z for k in SCEN[scen]}
    base = M.symmetric_subs(S, 3, aD, aT, eta, rho)
    for k in SCEN[scen]:
        base.pop(S["tau"][k])
    base[z] = 0
    TBz = [TB[i].xreplace(path) for i in (1, 2)]
    v = [S["nu"][1], S["nu"][2]]
    ev = lambda e: sp.simplify(e.xreplace(base))
    J = sp.Matrix(2, 2, lambda i, l: ev(sp.diff(TBz[i], v[l])))
    Fz = sp.Matrix([ev(sp.diff(TBz[i], z)) for i in range(2)])
    d1 = sp.simplify(-J.LUsolve(Fz))                  # nu'
    rhs = []
    for i in range(2):
        e = TBz[i]
        H = sum(ev(sp.diff(e, v[l], v[k])) * d1[l] * d1[k] for l in range(2) for k in range(2))
        K = sum(ev(sp.diff(e, v[l], z)) * d1[l] for l in range(2))
        Lz = ev(sp.diff(e, z, 2))
        rhs.append(H + 2 * K + Lz)
    d2 = sp.simplify(-J.LUsolve(sp.Matrix(rhs)))      # nu''
    return (aD, aT, eta, rho), d1, d2


if __name__ == "__main__":
    out = {"cal": CALS, "scen": {}}
    syms = {}
    for scen in SCEN:
        (aD, aT, eta, rho), d1, d2 = symbolic_bC(scen)
        syms[scen] = ((aD, aT, eta, rho), d1, d2)
        print(scen, "nu_C' =", sp.factor(d1[1]))
    tau_grid = np.concatenate([[0.01, 0.025], np.linspace(0.05, 1.0, 20)])
    for scen in SCEN:
        (aD, aT, eta, rho), d1, d2 = syms[scen]
        res = {}
        for name, cal in CALS.items():
            rD = M.rhoD(cal["aD"], cal["aT"], cal["eta"])
            r0 = 3 * rD if scen == "unilateral" else rD
            M3 = M.MN(3, cal["aD"], cal["eta"], r0)
            sub = {aD: cal["aD"], aT: cal["aT"], eta: cal["eta"], rho: r0}
            bC = float(d2[1].subs(sub))
            # finite-difference check of b_C on the exact solver
            h = 1e-3
            fd = (nuC(cal, r0, scen, h) - 2 * 0 + nuC(cal, r0, scen, -h)) / h ** 2
            kappa = -(3 if scen == "unilateral" else 1) * M3 * bC
            rs = []
            g = r0
            for t in tau_grid:
                g = rho_star(cal, scen, t, g)
                rs.append(g)
            rs = np.array(rs)
            slope_num = (rs[0] - r0) / tau_grid[0]
            res[name] = dict(rhoD=rD, rho0=r0, M3=M3, bC_symbolic=bC, bC_fd=fd, kappa=kappa,
                             slope_at_tau_0_01=slope_num, tau=tau_grid.tolist(), rho_star=rs.tolist(),
                             ratio=(rs / r0).tolist())
            print("%-12s %-24s rho0=%.4f b_C=%.5f (fd %.5f) kappa=%.4f  (rho*(0.01)-rho0)/0.01=%.4f"
                  "  rho*/rho0 at tau=0.5: %.4f, 1: %.4f"
                  % (scen, name, r0, bC, fd, kappa, slope_num, rs[int(np.argmin(abs(tau_grid - 0.5)))] / r0, rs[-1] / r0))
        out["scen"][scen] = res
    # closed form b_C at the symmetric baseline (unilateral), for the memo
    (aD, aT, eta, rho), d1, d2 = syms["unilateral"]
    rD = aD * eta + (1 - aD) * (1 - aT)
    bC_at = sp.factor(sp.simplify(d2[1].subs(rho, 3 * rD)))
    out["bC_unilateral_at_3rhoD"] = str(bC_at)
    (aD, aT, eta, rho), d1w, d2w = syms["retaliation"]
    bC_war = sp.factor(sp.simplify(d2w[1].subs(rho, rD)))
    out["bC_retaliation_at_rhoD"] = str(bC_war)
    print("b_C (unilateral, rho = 3 rho_D) =", bC_at)
    print("b_C (retaliation, rho = rho_D)  =", bC_war)
    json.dump(out, open(os.path.join(HERE, "results", "task_b.json"), "w"), indent=1)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=False)
    for ax, scen, lab in zip(axes, SCEN, (r"$\rho^\ast(\tau)/3\rho_D$", r"$\rho^\ast(\tau)/\rho_D$")):
        for (name, r), c in zip(out["scen"][scen].items(), style.SERIES):
            t = np.array(r["tau"])
            ax.plot(np.r_[0, t], np.r_[1, r["ratio"]], color=c, lw=1.7, label=name)
            tt = np.linspace(0, 0.35, 10)
            ax.plot(tt, 1 + r["kappa"] * tt / r["rho0"], color=c, lw=0.9, ls=(0, (3, 2)))
        ax.axhline(1, color=style.MUTED, lw=0.7)
        ax.set_xlabel(r"tariff $\tau$")
        ax.set_ylabel(lab)
        ax.set_title("(a) unilateral tariff on B" if scen == "unilateral"
                     else r"(b) bilateral retaliation, $\tau_{AB}=\tau_{BA}=\tau$", fontsize=9)
        style.finish(ax)
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.text(0.5, 0.005, "dashed: local slope $\\rho^\\ast_0+\\kappa\\tau$", ha="center", fontsize=7.5,
             color="0.4")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(HERE, "figures", "task_b_threshold.png"), dpi=200)
    print("figure written")
