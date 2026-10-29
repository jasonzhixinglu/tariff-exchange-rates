"""Appendix C: departures from the symmetric free-trade benchmark (N = 3, 5).

Recomputes every number of Appendix C of the draft from the exact model:
  C.1 common external tariff tau0: local threshold rho*(tau0) / N rho_D, and the
      discrete preferential cut from tau0 = 0.5;
  C.2 finite tariffs: rho*(tau) solving log e_AC(tau) = 0 from free trade;
  C.3 sensitivities d rho*/dx at the symmetric point; windows of reversal;
  C.4 the counterexample to the ordering d nu_B < d nu_C.
Both the "Figure 2" calibration (alpha_D, alpha_T, eta) = (0.7, 0.6, 1.5) of
the derivations note and the US-like calibration (0.8, 0.4, 1.5) are reported.
Writes code/results/appendix_c.json.
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from model import closed_forms as cf  # noqa: E402
from model import linear as lin  # noqa: E402
from model import nested_ces as nc  # noqa: E402

CALS = {"fig2": cf.FIG2, "us_like": cf.US_LIKE}


def tariff_on(N, pairs, value):
    t = np.zeros((N, N))
    for i, j in pairs:
        t[i, j] = value
    return t


# ------------------------------------------------------------------ C.1
def rho_star_common_tariff(N, tau0, cal):
    """Local bystander threshold at a common external tariff tau0 (baseline
    re-solved at each rho; tariff change measured as d log(1 + tau_AB))."""
    tau = tariff_on(N, [(0, j) for j in range(1, N)], tau0)
    d = tariff_on(N, [(0, 1)], 1.0)

    def f(rho):
        P = nc.symmetric(N, rho=rho, **cal)
        nu = nc.solve(P, tau)
        dnu, J = nc.local_response(P, tau, nu, d)
        assert lin.mml(J)
        return dnu[1]
    return brentq(f, 1.05, 60.0, xtol=1e-10)


def rho_star_preferential_cut(tau0, cal):
    """Exact N = 3: removing the tariff on B from tau0 raises e_AC iff rho > rho*."""
    N = 3
    tau = tariff_on(N, [(0, 1), (0, 2)], tau0)
    cut = tariff_on(N, [(0, 2)], tau0)

    def f(rho):
        P = nc.symmetric(N, rho=rho, **cal)
        nu0 = nc.solve(P, tau)
        nu1 = nc.solve(P, cut, nu0=nu0)
        return nu1[1] - nu0[1]
    return brentq(f, 1.05, 60.0, xtol=1e-10)


# ------------------------------------------------------------------ C.2
def solve_path(P, tau_final, steps=8):
    nu = np.zeros(P.N - 1)
    for s in np.linspace(0, 1, steps + 1)[1:]:
        nu = nc.solve(P, s * tau_final, nu0=nu)
    return nu


def rho_star_finite(tau, kind, cal):
    N = 3
    pairs = [(0, 1)] if kind == "unilateral" else [(0, 1), (1, 0)]
    T = tariff_on(N, pairs, tau)
    rD = cf.rhoD(**cal)
    lo, hi = (1.05, 3 * rD + 1.0) if kind == "unilateral" else (1.01, 3 * rD)

    def f(rho):
        return solve_path(nc.symmetric(N, rho=rho, **cal), T)[1]
    return brentq(f, lo, hi, xtol=1e-10)


def kappa_war(cal):
    aD, aT, eta = cal["aD"], cal["aT"], cal["eta"]
    mm = cf.m(aD, aT)
    return (1 - aD) / 4 * (aD * (eta - 1) ** 2 + 3 * aD * aT * (eta - 1) + 2 * aT * (1 - mm))


# ------------------------------------------------------------------ C.3
def prims3(cal, rho, beta_AB=0.5, L=(1.0, 1.0, 1.0), aD_A=None):
    aD = np.full(3, cal["aD"])
    if aD_A is not None:
        aD[0] = aD_A
    beta = np.array([[0, beta_AB, 1 - beta_AB], [0.5, 0, 0.5], [0.5, 0.5, 0]])
    return nc.Primitives(N=3, L=np.array(L, float), aD=aD, aT=cal["aT"], eta=cal["eta"],
                         rho=rho, beta=beta)


def bystander_free_trade(P):
    nu = nc.solve(P)
    base = nc.baseline_shares(P, nu)
    return lin.response(base, tariff_on(3, [(0, 1)], 1.0))[1], base


def rho_star_prims(cal, **kw):
    rD3 = 3 * cf.rhoD(**cal)
    return brentq(lambda r: bystander_free_trade(prims3(cal, r, **kw))[0],
                  rD3 - 1.5, rD3 + 2.5, xtol=1e-13)


def sensitivities(cal, h=1e-4):
    out = {}
    specs = {
        "beta_AB": lambda x: dict(beta_AB=0.5 + x),
        "L_B": lambda x: dict(L=(1.0, 1.0 + x, 1.0)),
        "L_C": lambda x: dict(L=(1.0, 1.0, 1.0 + x)),
        "aD_A": lambda x: dict(aD_A=cal["aD"] + x),
    }
    for k, spec in specs.items():
        out[k] = (rho_star_prims(cal, **spec(h)) - rho_star_prims(cal, **spec(-h))) / (2 * h)
    return out


def reversal_windows(cal, L_B, rho_max=1000.0, n=400):
    grid = np.exp(np.linspace(np.log(1.02), np.log(rho_max), n))
    f = lambda r: bystander_free_trade(prims3(cal, r, L=(1.0, L_B, 1.0)))[0]
    vals = [f(r) for r in grid]
    roots = [brentq(f, a, b, xtol=1e-9) for a, b, fa, fb in
             zip(grid[:-1], grid[1:], vals[:-1], vals[1:]) if np.sign(fa) != np.sign(fb)]
    shares = {}
    for r in (5.0, 20.0, 100.0):
        _, base = bystander_free_trade(prims3(cal, r, L=(1.0, L_B, 1.0)))
        shares[r] = base["b"][0, 1]
    return roots, shares, bool(np.all(np.array(vals) < 0))


# ------------------------------------------------------------------ C.4
def ordering_counterexample():
    beta = np.array([[0, 0.86, 0.14], [0.65, 0, 0.35], [0.19, 0.81, 0]])
    P = nc.Primitives(N=3, L=np.array([5.12, 4.26, 2.28]), aD=0.89, aT=0.6, eta=3.74,
                      rho=1.20, beta=beta)
    nu = nc.solve(P)
    base = nc.baseline_shares(P, nu)
    dnu = lin.response(base, tariff_on(3, [(0, 1)], 1.0))
    nu1 = nc.solve(P, tariff_on(3, [(0, 1)], 0.01), nu0=nu)
    exact = (nu1 - nu) / 0.01
    return dict(dnuB=dnu[0], dnuC=dnu[1], diff=dnu[0] - dnu[1], exact_diff=exact[0] - exact[1],
                mml=lin.mml(lin.reduced_jacobian(base)))


def main():
    res = {}
    for name, cal in CALS.items():
        rD = cf.rhoD(**cal)
        r = {"rho_D": rD}
        r["C1_ratio"] = {str(N): {str(t0): rho_star_common_tariff(N, t0, cal) / (N * rD)
                                  for t0 in (0.25, 0.5, 1.0)} for N in (3, 5)}
        r["C1_local_tau0_0.5_N3"] = rho_star_common_tariff(3, 0.5, cal)
        r["C1_cut_tau0_0.5_N3"] = rho_star_preferential_cut(0.5, cal)
        r["C2_unilateral"] = {str(t): rho_star_finite(t, "unilateral", cal) for t in (0.01, 0.25, 0.5, 1.0, 1.45)}
        r["C2_retaliation"] = {str(t): rho_star_finite(t, "retaliation", cal) for t in (0.01, 0.25, 0.5, 1.0, 1.45)}
        r["C2_unilateral_ratio_tau1"] = r["C2_unilateral"]["1.0"] / (3 * rD)
        r["C2_retaliation_ratio_tau1"] = r["C2_retaliation"]["1.0"] / rD
        r["C2_kappa_war_closed"] = kappa_war(cal)
        r["C2_kappa_war_fd"] = (r["C2_retaliation"]["0.01"] - rD) / 0.01
        r["C3_sensitivities"] = sensitivities(cal)
        print(name, json.dumps(r, indent=1))
        res[name] = r
    roots, shares, never = reversal_windows(CALS["fig2"], 2.2)
    res["C3_window_LB_2.2_fig2"] = dict(roots=roots, import_share_from_B=shares)
    roots26, _, never26 = reversal_windows(CALS["fig2"], 2.6)
    res["C3_window_LB_2.6_fig2"] = dict(roots=roots26, never_reverses_rho_le_1000=never26)
    res["C4_ordering"] = ordering_counterexample()
    print(json.dumps({k: res[k] for k in res if k.startswith("C3_w") or k.startswith("C4")}, indent=1))
    with open(os.path.join(HERE, "..", "results", "appendix_c.json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__" and "--kappa-grid" not in sys.argv:
    main()


def kappa_uni_grid(tau=0.01):
    """Sign of the finite-tariff slope of the unilateral threshold,
    (rho*(tau) - 3 rho_D)/tau, on a grid alpha_D in [1/3,1), alpha_T in (0,1],
    eta in [1,10] (the box of the derivations note)."""
    out = []
    for aD in (0.34, 0.5, 0.7, 0.9):
        for aT in (0.1, 0.4, 0.7, 1.0):
            for eta in (1.0, 2.0, 5.0, 10.0):
                cal = dict(aD=aD, aT=aT, eta=eta)
                rD3 = 3 * cf.rhoD(**cal)
                T = tariff_on(3, [(0, 1)], tau)
                f = lambda r: nc.solve(nc.symmetric(3, rho=r, **cal), T)[1]
                r = brentq(f, max(1.01, rD3 - 2), rD3 + 1, xtol=1e-12)
                out.append(dict(aD=aD, aT=aT, eta=eta, slope=(r - rD3) / tau))
    return out


if __name__ == "__main__" and "--kappa-grid" in sys.argv:
    g = kappa_uni_grid()
    s = [x["slope"] for x in g]
    print("kappa_uni grid: n=%d, max slope %.4f, min %.4f" % (len(s), max(s), min(s)))
    res = json.load(open(os.path.join(HERE, "..", "results", "appendix_c.json")))
    res["C2_kappa_uni_grid"] = dict(n=len(s), max_slope=max(s), min_slope=min(s), points=g)
    json.dump(res, open(os.path.join(HERE, "..", "results", "appendix_c.json"), "w"), indent=1)
