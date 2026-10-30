"""
Phase 1.2: general-size threshold rho* via share-based linearization.

Approach (hat algebra). At a free-trade baseline described entirely by
observables --

    y_i          income of country i in common currency (= v_i L_i)
    h_i          home share of country i's tradable expenditure
    b_ij         origin-j share of i's import bundle (sum_j b_ij = 1)
    alpha_T      tradable share of expenditure (CD outer layer)

-- totally differentiate the two balanced-trade conditions with respect to
(nu_B, nu_C, tau), where nu_j = log v_j and tau is A's tariff on B.
Nested-CES share responses are linear in (eta, rho), so

    d log e_AC / d tau |_{tau=0} = N(rho) / D(rho)

with N quadratic in rho. The reversal threshold is the relevant root of N.
The equal-size symmetric case (h_i = aD, b_ij = 1/2, y_i = 1) must reduce
to rho* = 3 [1 + aD (eta - 1) - aT (1 - aD)].

Validation targets (aD=.80, aT=.40, eta=1.5, L_B=1.21): brute-force
thresholds 8.76 (Vietnam), 4.32 (EU), 4.24 (equal), 3.78 (ROW).

Run:  python scripts/derive_general_threshold.py
"""

import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from tariff_exchange_rates.nested import (  # noqa: E402
    compute_allocation_nested, make_params_nested, rho_star_numeric,
    solve_3country_nested,
)

IDX = ["A", "B", "C"]


def build_linearization():
    """Return (system solution dnuC/dtau, symbols dict)."""
    eta, rho, aT = sp.symbols("eta rho alpha_T", positive=True)
    nB, nC, t = sp.symbols("dnu_B dnu_C dtau")          # differentials
    h = {i: sp.Symbol(f"h_{i}", positive=True) for i in IDX}
    y = {i: sp.Symbol(f"y_{i}", positive=True) for i in IDX}
    b = {}
    for i in IDX:
        foreign = [j for j in IDX if j != i]
        b[(i, foreign[0])] = sp.Symbol(f"b_{i}{foreign[0]}", positive=True)
        b[(i, foreign[1])] = 1 - b[(i, foreign[0])]

    dnu = {"A": sp.Integer(0), "B": nB, "C": nC}
    # d log p_ij = dnu_j + dtau for (i,j) = (A,B)
    dlp = {(i, j): dnu[j] + (t if (i, j) == ("A", "B") else 0)
           for i in IDX for j in IDX}

    # CES aggregates
    dlPM = {i: sum(b[(i, j)] * dlp[(i, j)] for j in IDX if j != i) for i in IDX}
    dlPT = {i: h[i] * dlp[(i, i)] + (1 - h[i]) * dlPM[i] for i in IDX}

    # Share log-changes
    dls = {}
    for i in IDX:
        dls[(i, i)] = (1 - eta) * (dlp[(i, i)] - dlPT[i])
        for j in IDX:
            if j != i:
                dls[(i, j)] = ((1 - rho) * (dlp[(i, j)] - dlPM[i])
                               + (1 - eta) * (dlPM[i] - dlPT[i]))

    # Income log-changes: rebate contributes s_AB * dtau for country A
    s = {(i, i): aT * h[i] for i in IDX}
    for i in IDX:
        for j in IDX:
            if j != i:
                s[(i, j)] = aT * (1 - h[i]) * b[(i, j)]
    dlI = {"A": dnu["A"] + s[("A", "B")] * t, "B": dnu["B"], "C": dnu["C"]}

    # d(TB_i): TB_i = sum_{k!=i} s_ki I_k/(1+tau_ki) - sum_{j!=i} s_ij I_i/(1+tau_ij)
    # At tau=0 the 1/(1+tau_AB) factor contributes -s_AB I_A dtau to B's exports.
    def dTB(i):
        expr = 0
        for k in IDX:
            if k != i:
                expr += s[(k, i)] * y[k] * (dls[(k, i)] + dlI[k])
                if (k, i) == ("A", "B"):
                    expr -= s[(k, i)] * y[k] * t
        for j in IDX:
            if j != i:
                expr -= s[(i, j)] * y[i] * (dls[(i, j)] + dlI[i])
        return expr

    # The system is linear in (nB, nC): solve the 2x2 by hand (Cramer),
    # which is orders of magnitude faster than sp.solve here.
    eqs = [sp.expand(dTB("B")), sp.expand(dTB("C"))]
    A_mat, rhs = sp.linear_eq_to_matrix(eqs, [nB, nC])
    det = sp.expand(A_mat[0, 0] * A_mat[1, 1] - A_mat[0, 1] * A_mat[1, 0])
    nC_sol = sp.expand(A_mat[0, 0] * rhs[1] - A_mat[1, 0] * rhs[0]) / det
    # rhs is proportional to t; divide it out exactly
    dnuC_dtau = sp.cancel(nC_sol / t)
    syms = dict(eta=eta, rho=rho, aT=aT, h=h, y=y, b=b)
    return dnuC_dtau, syms


def baseline_observables(alpha_T, alpha_D, eta, rho, labor):
    """Numeric free-trade baseline -> (y_i, h_i, b_ij) for validation."""
    p = make_params_nested(alpha_T, alpha_D, eta, rho, labor)
    eq = solve_3country_nested(p, np.zeros((3, 3)))
    a = eq["allocation"]
    shares = a["shares"]                            # currency-invariant
    # incomes converted to the common (country A) currency: y_i = e_Ai w_i L_i
    income = a["exchange_matrix"][0] * a["income"]
    vals = {}
    for i_ix, i in enumerate(IDX):
        vals[f"y_{i}"] = income[i_ix]
        vals[f"h_{i}"] = shares[i_ix, i_ix] / alpha_T
        foreign = [j for j in range(3) if j != i_ix]
        imp = shares[i_ix, foreign].sum()
        first = IDX[foreign[0]]
        vals[f"b_{i}{first}"] = shares[i_ix, foreign[0]] / imp
    return vals


def main():
    print("Building share-based linearization ...")
    dnuC, s = build_linearization()
    num, den = sp.fraction(dnuC)
    num_poly = sp.Poly(sp.expand(num), s["rho"])
    print(f"  numerator degree in rho: {num_poly.degree()}")
    assert num_poly.degree() == 2, "expected quadratic in rho"

    # ------------------------------------------------------------------
    # Symmetric reduction: h_i = aD, b_ij = 1/2, y_i = 1
    # ------------------------------------------------------------------
    aD = sp.Symbol("alpha_D", positive=True)
    sym_subs = {}
    for i in IDX:
        sym_subs[s["h"][i]] = aD
        sym_subs[s["y"][i]] = 1
    for (i, j), expr in s["b"].items():
        if isinstance(expr, sp.Symbol):
            sym_subs[expr] = sp.Rational(1, 2)
    dnuC_sym = sp.cancel(sp.together(dnuC.subs(sym_subs)))
    target = (s["rho"] - 3 * (1 + aD * (s["eta"] - 1)
                              - s["aT"] * (1 - aD))) \
        / (3 * (3 * aD * (s["eta"] - 1) + s["rho"] + 1))
    diff = sp.cancel(sp.together(dnuC_sym - target))
    ok = sp.simplify(diff) == 0
    print("  symmetric reduction matches (rho - rho*)/(3[3 aD(eta-1)+rho+1]):", ok)
    assert ok

    # ------------------------------------------------------------------
    # Quadratic coefficients (general case) -> save for the paper appendix
    # ------------------------------------------------------------------
    c2, c1, c0 = [sp.factor(c) for c in num_poly.all_coeffs()]
    # Verified structure: c2 = b_AB b_AC b_CA b_CB (1-h_A)(1-h_C) y_A y_C > 0,
    # so N is an upward parabola, rho* is its larger root, and "reversal iff
    # rho > rho*" holds at any baseline. All three coefficients share the
    # factor b_AB (1-h_A) y_A -- A's import exposure to B.
    h, y, b = s["h"], s["y"], s["b"]
    conj_c2 = (b[("A", "B")] * (1 - b[("A", "B")])
               * b[("C", "A")] * (1 - b[("C", "A")])
               * (1 - h["A"]) * (1 - h["C"]) * y["A"] * y["C"])
    assert sp.expand(c2 - conj_c2) == 0
    out = ROOT / "output" / "general_threshold_symbolic.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(
            "d log e_AC / d tau |_{tau=0} = N(rho)/D(rho), hat-algebra form.\n"
            "Baseline observables: y_i incomes (common currency), h_i home\n"
            "shares of tradable expenditure, b_ij import-bundle origin\n"
            "shares, alpha_T tradable expenditure share.\n\n"
            "N(rho) = c2 rho^2 + c1 rho + c0; reversal iff N(rho) > 0 at the\n"
            "stable equilibrium (D > 0). Threshold rho* = larger root of N.\n\n")
        for name, c in [("c2", c2), ("c1", c1), ("c0", c0)]:
            f.write(f"-- {name} --\n{sp.sstr(c)}\n\n")
        f.write(f"-- D --\n{sp.sstr(sp.factor(sp.simplify(den)))}\n")
    print(f"  quadratic coefficients written to {out}")

    # ------------------------------------------------------------------
    # Numeric validation against brute-force thresholds
    # ------------------------------------------------------------------
    print("\nValidation against brute-force thresholds "
          "(aD=.80, aT=.40, eta=1.5, L_B=1.21):")
    aD_v, aT_v, eta_v, LB_v = 0.80, 0.40, 1.5, 1.21
    free_syms = sorted(num.free_symbols, key=lambda x: x.name)
    lam = sp.lambdify(free_syms, num, "numpy")

    for lab, LC_v, (lo, hi) in [("Vietnam", 0.055, (6, 14)), ("EU", 0.86, (2, 10)),
                                ("equal", 1.00, (2, 10)), ("ROW", 3.51, (2, 10))]:
        labor = (1.0, LB_v, LC_v)

        def N_of_rho(r):
            obs = baseline_observables(aT_v, aD_v, eta_v, r, labor)
            vals = []
            for sym in free_syms:
                nm = sym.name
                if nm == "rho":
                    vals.append(r)
                elif nm == "eta":
                    vals.append(eta_v)
                elif nm == "alpha_T":
                    vals.append(aT_v)
                else:
                    vals.append(obs[nm])
            return lam(*vals)

        rs_sym = brentq(N_of_rho, lo, hi, xtol=1e-7)
        rs_bf = rho_star_numeric(aT_v, aD_v, eta_v, labor=labor, lo=lo, hi=hi)
        print(f"  {lab:8s} L_C={LC_v:5.3f}  hat-algebra rho* = {rs_sym:7.4f}"
              f"   brute-force = {rs_bf:7.4f}   diff = {rs_sym - rs_bf:+.2e}")
        assert abs(rs_sym - rs_bf) < 2e-3

    print("\nAll validations passed.")


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
