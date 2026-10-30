"""
Reproduce and verify every quantitative claim in the August 2026 referee
report, plus the repo-specific findings documented in REVISION_PLAN.md.

Sections
--------
1. Income-formula bug: old (fixed-weight) vs corrected (realized-share)
   tariff revenue, and the spurious sign reversal it produced.
2. Flat single-elasticity CES at the paper's symmetric calibration:
   log e_AC asymptotes to 0^- (impossibility), analytic slope -1/(12 sigma),
   constant threshold gap rho* - sigma = +0.50.
3. Nested (eta, rho) model: analytic threshold
       rho* = 3 [1 + aD (eta - 1) - aT (1 - aD)]
   verified against nonlinear solves; rho* grid; third-country size; the
   large-tariff threshold path rho*(tau).
4. Trade-war comparative static: magnitude decreasing in sigma (flat CES)
   but increasing in rho (nested) — referee report section 4.3.
5. Effect of the income fix on the paper's published calibration numbers.
6. (--symbolic) Symbolic derivation of the threshold via sympy.

Run:  python scripts/verify_referee_claims.py [--symbolic]
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, fsolve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tariff_exchange_rates.equilibrium import solve_3country  # noqa: E402


# ===========================================================================
# Standalone nested (eta, rho) three-country model
#
#   C_i  = C_Ti^aT * C_Ni^(1-aT)                     (Cobb-Douglas outer)
#   C_Ti = CES(eta)  over {home variety, import bundle M_i}, home weight aD
#   M_i  = CES(rho)  over the two foreign varieties, weights 1/2
#
# eta = home-vs-import (macro Armington) elasticity
# rho = cross-origin (micro) elasticity
# Flat CES with a single sigma is the special case rho = eta = sigma
# (up to the weight convention; see flat-CES check below).
#
# This implementation matches the referee's replication and is the
# reference against which the Phase 2 package implementation is tested.
# ===========================================================================

def nested_trade_balances(nu, tau, aD, aT, eta, rho, L):
    """TB_i (producer-price value, own currency) at log-rates nu = (nu_B, nu_C)."""
    if abs(eta - 1) < 1e-7:
        eta = 1 + 1e-7
    if abs(rho - 1) < 1e-7:
        rho = 1 + 1e-7
    idx = [0, 1, 2]
    v = np.exp(np.r_[0.0, nu])          # wage of i in A's currency (= e_Ai)
    aM = 1 - aD
    p = np.array([[(1 + tau[i][j]) * v[j] for j in idx] for i in idx])
    sh = np.zeros((3, 3))               # expenditure share of TOTAL income on j
    for i in idx:
        f = [j for j in idx if j != i]
        PM = sum(0.5 * p[i][j] ** (1 - rho) for j in f) ** (1 / (1 - rho))
        PT = (aD * p[i][i] ** (1 - eta) + aM * PM ** (1 - eta)) ** (1 / (1 - eta))
        sh[i][i] = aT * aD * p[i][i] ** (1 - eta) / PT ** (1 - eta)
        for j in f:
            sh[i][j] = (aT * aM * PM ** (1 - eta) / PT ** (1 - eta)
                        * 0.5 * p[i][j] ** (1 - rho) / PM ** (1 - rho))
    inc = np.array([
        v[i] * L[i] / (1 - sum(tau[i][j] / (1 + tau[i][j]) * sh[i][j]
                               for j in idx if j != i))
        for i in idx
    ])
    E = np.array([[sh[i][j] * inc[i] for j in idx] for i in idx])
    return np.array([
        sum(E[k][i] / (1 + tau[k][i]) for k in idx if k != i)
        - sum(E[i][j] / (1 + tau[i][j]) for j in idx if j != i)
        for i in idx
    ])


def zero_tau():
    return [[0.0] * 3 for _ in range(3)]


def isolated(t):
    T = zero_tau()
    T[0][1] = t
    return T


def war(t_ab, t_ba=None):
    T = zero_tau()
    T[0][1] = t_ab
    T[1][0] = t_ab if t_ba is None else t_ba
    return T


def nested_equilibrium(tau, aD, aT, eta, rho, L, x0=None):
    x0 = x0 if x0 is not None else [np.log(L[1]), np.log(L[2])]
    return fsolve(lambda x: nested_trade_balances(x, tau, aD, aT, eta, rho, L)[1:],
                  x0, xtol=1e-13)


def d_log_eAC(rho, aD, aT, eta, L, h=1e-6, tau0=0.0):
    """Numerical d log e_AC / d tau at tau = tau0 (isolated tariff)."""
    x0 = nested_equilibrium(isolated(tau0), aD, aT, eta, rho, L)
    x1 = nested_equilibrium(isolated(tau0 + h), aD, aT, eta, rho, L, x0)
    return (x1[1] - x0[1]) / h


def rho_star(aD, aT, eta):
    """Analytic threshold, equal sizes, symmetric weights, tau -> 0."""
    return 3 * (1 + aD * (eta - 1) - aT * (1 - aD))


def analytic_slope(rho, aD, aT, eta):
    """Analytic d log e_AC / d tau |_{tau=0}, equal sizes."""
    return -(rho_star(aD, aT, eta) - rho) / (3 * (3 * aD * (eta - 1) + rho + 1))


def rho_star_numeric(aD, aT, eta, L, lo=1.05, hi=20.0, tau0=0.0):
    """Threshold for general sizes / tariff levels by root-finding on the slope."""
    return brentq(lambda r: d_log_eAC(r, aD, aT, eta, L, tau0=tau0), lo, hi, xtol=1e-6)


# ===========================================================================
# Package model helpers (flat CES, corrected)
# ===========================================================================

def flat_params(sigma, alpha_T=(0.25, 0.25, 0.25), alpha_N=None, L=(1, 1, 1)):
    alpha_T = np.asarray(alpha_T, dtype=float)
    return {
        "productivity_T": np.ones(3), "productivity_N": np.ones(3),
        "labor": np.asarray(L, dtype=float), "alpha_T": alpha_T,
        "alpha_N": 1.0 - alpha_T.sum() if alpha_N is None else alpha_N,
        "sigma": sigma, "prices_T": np.ones(3),
    }


def flat_solve(sigma, tariffs, **kw):
    return solve_3country(flat_params(sigma, **kw), np.asarray(tariffs))


# ===========================================================================
# Report sections
# ===========================================================================

def section1():
    print("=" * 76)
    print("1. INCOME-FORMULA BUG (repo finding, REVISION_PLAN 3.1)")
    print("=" * 76)
    print("Isolated tariff tau_AB = 1, symmetric baseline. 'old' = fixed-weight")
    print("tariff revenue (pre-fix code); 'corrected' = realized CES shares;")
    print("'referee' = referee's independent nested replication.\n")
    old = {0.5: (-0.3972, -0.1488), 1.0: (-0.2719, -0.0488),
           2.0: (-0.1927, +0.0048), 5.0: (-0.1140, +0.0218)}
    ref = {0.5: (-0.3587, -0.1133), 1.0: (-0.2719, -0.0488),
           2.0: (-0.2110, -0.0163), 5.0: (-0.1286, -0.0013)}
    print(f"{'sigma':>6} | {'old e_AB':>9} {'old e_AC':>9} | "
          f"{'corr e_AB':>9} {'corr e_AC':>9} | {'ref e_AB':>9} {'ref e_AC':>9}")
    for s in [0.5, 1.0, 2.0, 5.0]:
        r = flat_solve(s, isolated(1.0))
        print(f"{s:>6.1f} | {old[s][0]:>+9.4f} {old[s][1]:>+9.4f} | "
              f"{r['log_e_AB']:>+9.4f} {r['log_e_AC']:>+9.4f} | "
              f"{ref[s][0]:>+9.4f} {ref[s][1]:>+9.4f}")
        assert abs(r["log_e_AB"] - ref[s][0]) < 5e-5
        assert abs(r["log_e_AC"] - ref[s][1]) < 5e-5
    print("\nOld code showed a spurious sign flip in log e_AC at sigma >~ 1.9;")
    print("corrected model matches the referee to 4 decimals at every sigma. [OK]\n")


def section2():
    print("=" * 76)
    print("2. FLAT CES: IMPOSSIBILITY AT THE PAPER'S CALIBRATION (referee 5.3)")
    print("=" * 76)
    print("alpha_Tj = alpha_N = 1/4  =>  aD = 1/3, aT = 3/4 (knife edge).")
    print("Analytic local slope: d log e_AC/d tau|_0 = -1/(12 sigma);")
    print("threshold gap rho* - sigma = +0.50 for ALL sigma.\n")
    print(f"{'sigma':>6} {'log e_AC (tau=1)':>17} {'num slope':>12} "
          f"{'-1/(12s)':>10} {'rho*-sigma':>11}")
    h = 1e-6
    for s in [0.5, 1.0, 2.0, 5.0, 20.0]:
        eq = flat_solve(s, isolated(1.0))
        base = flat_solve(s, zero_tau())
        pert = flat_solve(s, isolated(h))
        slope = (pert["log_e_AC"] - base["log_e_AC"]) / h
        gap = rho_star(1 / 3, 0.75, s) - s
        print(f"{s:>6.1f} {eq['log_e_AC']:>+17.5f} {slope:>+12.6f} "
              f"{-1 / (12 * s):>+10.6f} {gap:>+11.2f}")
        assert eq["log_e_AC"] <= 1e-8
        assert abs(slope - (-1 / (12 * s))) < 1e-3 / s
        assert abs(gap - 0.50) < 1e-12
    print("\nNo crossing at any sigma: an asymptote, not a near-reversal. [OK]\n")


def section3():
    print("=" * 76)
    print("3. NESTED (eta, rho) MODEL: THRESHOLD rho* (referee 5.2, 5.4-5.6)")
    print("=" * 76)
    print("rho* = 3 [1 + aD (eta - 1) - aT (1 - aD)]\n")

    print("3a. Analytic vs numerical slope (equal sizes):")
    for aD, aT, eta, rho in [(.8, .4, 1.5, 4.5), (.8, .4, 1.5, 3.0),
                             (1 / 3, .75, 2.0, 2.0), (.7, .4, 2.0, 6.0)]:
        a = analytic_slope(rho, aD, aT, eta)
        n = d_log_eAC(rho, aD, aT, eta, [1, 1, 1])
        print(f"    aD={aD:.3f} aT={aT:.2f} eta={eta:.1f} rho={rho:.1f}"
              f"   analytic={a:+.6f}  numeric={n:+.6f}"
              f"   rho*={rho_star(aD, aT, eta):.2f}")
        assert abs(a - n) < 1e-6

    print("\n3b. rho* grid, aT = 0.40 (referee 5.4):")
    etas = [1.0, 1.5, 2.0]
    print("            " + "".join(f"eta={e:<10.1f}" for e in etas))
    for aD in [.6, .7, .8, .85, .9]:
        print(f"    aD={aD:.2f}  "
              + "".join(f"{rho_star(aD, .4, e):<14.2f}" for e in etas))
    assert abs(rho_star(.8, .4, 1.5) - 3.96) < 1e-10

    print("\n3c. rho* by third-country size (aD=.80, aT=.40, eta=1.5, L_B=1.21):")
    expected = {"Vietnam": (0.055, 8.76), "EU": (0.86, 4.32),
                "equal": (1.00, 4.24), "ROW": (3.51, 3.78)}
    for lab, (LC, ref) in expected.items():
        lo, hi = (6, 14) if LC < 0.1 else (2, 10)
        rs = brentq(lambda r: d_log_eAC(r, .8, .4, 1.5, [1, 1.21, LC]), lo, hi)
        print(f"    {lab:8s} L_C={LC:5.3f}   rho* = {rs:5.2f}   (referee: {ref})")
        assert abs(rs - ref) < 0.01
    print("    (small C => high threshold: Vietnam is the HARDEST configuration)")

    print("\n3d. Large-tariff thresholds, equal sizes, aD=.8 aT=.4 eta=1.5.")
    print("    cumulative: rho s.t. the TOTAL change log e_AC(tau) = 0")
    print("                (referee 5.6's definition; policy-relevant for a")
    print("                 discrete tariff)")
    print("    marginal:   rho s.t. d log e_AC/d tau = 0 AT tau (lower still)")
    ref_cum = {0.2: 3.55, 0.5: 3.19, 1.0: 2.86, 1.45: 2.70}

    def cum_change(rho, tau0):
        x0 = nested_equilibrium(zero_tau(), .8, .4, 1.5, rho, [1, 1, 1])
        x1 = nested_equilibrium(isolated(tau0), .8, .4, 1.5, rho, [1, 1, 1], x0)
        return x1[1] - x0[1]

    print(f"    tau=0.00   cumulative = marginal = {rho_star(.8, .4, 1.5):.2f}")
    for tau0 in [0.2, 0.5, 1.0, 1.45]:
        rs_cum = brentq(lambda r: cum_change(r, tau0), 1.5, 8.0, xtol=1e-6)
        rs_marg = rho_star_numeric(.8, .4, 1.5, [1, 1, 1], lo=1.5, hi=8.0,
                                   tau0=tau0)
        print(f"    tau={tau0:4.2f}   cumulative = {rs_cum:4.2f} "
              f"(referee: {ref_cum[tau0]:4.2f})   marginal = {rs_marg:4.2f}")
        assert abs(rs_cum - ref_cum[tau0]) < 0.01
    print("    (both decreasing in tau: the tau->0 threshold is conservative)\n")


def section4():
    print("=" * 76)
    print("4. TRADE WAR: MAGNITUDE COMPARATIVE STATIC (referee 4.3)")
    print("=" * 76)
    print("tau_AB = tau_BA = 0.5, equal sizes. Paper claims increasing in the")
    print("elasticity; true only for rho in the nest, FALSE for flat sigma.\n")
    prev_flat, prev_nest = np.inf, -np.inf
    for rho in [1.5, 3.0, 6.0, 10.0]:
        n1 = nested_equilibrium(war(.5), .8, .4, 1.5, rho, [1, 1, 1])
        n2 = nested_equilibrium(war(.5), 1 / 3, .75, rho, rho, [1, 1, 1])
        print(f"    rho={rho:5.1f}   nested(eta=1.5): log e_AC={n1[1]:+.4f}"
              f"   flat(sigma=rho): log e_AC={n2[1]:+.4f}")
        assert n1[1] > prev_nest and n2[1] < prev_flat
        prev_flat, prev_nest = n2[1], n1[1]
    print("    [OK] nested increasing in rho; flat decreasing in sigma\n")


def section5():
    print("=" * 76)
    print("5. EFFECT OF THE INCOME FIX ON THE PUBLISHED CALIBRATION")
    print("=" * 76)
    print("Percent changes 100*(e1/e0 - 1) vs free trade; published values")
    print("from paper Table 4 / Figure 8 (pre-fix code).\n")
    cfgs = {
        "EU":  dict(alpha_T=(.097, .165, .138), L=(1, 1.21, .86), sigma=6),
        "VNM": dict(alpha_T=(.138, .236, .026), L=(1, 1.21, .055), sigma=8),
        "ROW": dict(alpha_T=(.034, .057, .309), L=(1, 1.21, 3.51), sigma=2),
    }
    regimes = {"R1": (0.20, 0.00, 0.00), "R2": (1.45, 1.25, 0.10)}
    published = {("EU", "R1"): (-4.31, -0.40), ("EU", "R2"): (+1.10, +7.29),
                 ("VNM", "R1"): (-7.19, -0.55), ("VNM", "R2"): (+0.26, +6.40),
                 ("ROW", "R1"): (-0.98, -0.19), ("ROW", "R2"): (-1.49, +0.87)}
    for name, cfg in cfgs.items():
        for rn, (tAB, tBA, tAC) in regimes.items():
            T = np.zeros((3, 3))
            T[0, 1], T[1, 0], T[0, 2] = tAB, tBA, tAC
            kw = dict(alpha_T=cfg["alpha_T"], L=cfg["L"])
            base = flat_solve(cfg["sigma"], np.zeros((3, 3)), **kw)
            eq = flat_solve(cfg["sigma"], T, **kw)
            dAB = 100 * (np.exp(eq["log_e_AB"] - base["log_e_AB"]) - 1)
            dAC = 100 * (np.exp(eq["log_e_AC"] - base["log_e_AC"]) - 1)
            pAB, pAC = published[(name, rn)]
            flag = "  <-- SIGN FLIP vs published" if dAC * pAC < 0 else ""
            print(f"    {name:4s} {rn}:  dAB {pAB:+6.2f} -> {dAB:+6.2f}   "
                  f"dAC {pAC:+6.2f} -> {dAC:+6.2f}{flag}")
    print("\nROW Regime 2 d e_AC flips sign under the corrected model, removing")
    print("one of the two directional successes claimed in the abstract.\n")


def section6_symbolic():
    print("=" * 76)
    print("6. SYMBOLIC DERIVATION OF THE THRESHOLD (sympy)")
    print("=" * 76)
    import sympy as sp
    nuB, nuC, t = sp.symbols("nu_B nu_C tau", real=True)
    aT, aD, eta, rho = sp.symbols("alpha_T alpha_D eta rho", positive=True)
    idx = ["A", "B", "C"]
    v = {"A": sp.Integer(1), "B": sp.exp(nuB), "C": sp.exp(nuC)}
    tau = {i: {j: sp.Integer(0) for j in idx} for i in idx}
    tau["A"]["B"] = t
    aM, beta = 1 - aD, sp.Rational(1, 2)
    p = {i: {j: (1 + tau[i][j]) * v[j] for j in idx} for i in idx}
    PM = {i: sp.Pow(sum(beta * p[i][j] ** (1 - rho) for j in idx if j != i),
                    1 / (1 - rho)) for i in idx}
    PT = {i: sp.Pow(aD * p[i][i] ** (1 - eta) + aM * PM[i] ** (1 - eta),
                    1 / (1 - eta)) for i in idx}
    sh = {}
    for i in idx:
        sh[i] = {i: aT * aD * p[i][i] ** (1 - eta) / PT[i] ** (1 - eta)}
        for j in idx:
            if j != i:
                sh[i][j] = (aT * aM * PM[i] ** (1 - eta) / PT[i] ** (1 - eta)
                            * beta * p[i][j] ** (1 - rho) / PM[i] ** (1 - rho))
    I = {i: v[i] / (1 - sum(tau[i][j] / (1 + tau[i][j]) * sh[i][j]
                            for j in idx if j != i)) for i in idx}
    E = {i: {j: sh[i][j] * I[i] for j in idx} for i in idx}
    TB = {i: (sum(E[k][i] / (1 + tau[k][i]) for k in idx if k != i)
              - sum(E[i][j] / (1 + tau[i][j]) for j in idx if j != i))
          for i in idx}
    F = sp.Matrix([TB["B"], TB["C"]])
    J = F.jacobian(sp.Matrix([nuB, nuC])).subs({nuB: 0, nuC: 0, t: 0})
    Ft = sp.Matrix([sp.diff(F[k], t) for k in range(2)]).subs({nuB: 0, nuC: 0, t: 0})
    dC = sp.simplify((-J.inv() * Ft)[1])
    num, den = sp.fraction(sp.cancel(sp.together(dC)))
    rs = sp.solve(sp.Eq(sp.expand(num), 0), rho)[0]
    print("    d log e_AC/d tau numerator  :", sp.factor(sp.expand(num)))
    print("    d log e_AC/d tau denominator:", sp.factor(sp.expand(den)))
    print("    rho* =", sp.simplify(rs))
    target = 3 * (1 + aD * (eta - 1) - aT * (1 - aD))
    assert sp.simplify(rs - target) == 0
    print("    matches 3[1 + aD(eta-1) - aT(1-aD)]  [OK]\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbolic", action="store_true",
                    help="also run the sympy derivation of rho*")
    args = ap.parse_args()
    np.seterr(all="ignore")
    section1()
    section2()
    section3()
    section4()
    section5()
    if args.symbolic:
        section6_symbolic()
    print("All checks passed.")
