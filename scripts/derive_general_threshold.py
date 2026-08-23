"""
Phase 1.1-1.2: symbolic derivation of the general-size threshold rho*.

Strategy
--------
The free-trade baseline with unequal sizes (L_B, L_C) has no closed form
for the wage vector, so we differentiate implicitly at a SYMBOLIC baseline
(v_B0, v_C0) that satisfies the two free-trade balanced-trade conditions,
and express d log e_AC / d tau in terms of baseline magnitudes. Setting the
numerator to zero and collecting in rho should give the threshold as the
root of a (at most) quadratic in rho, whose coefficients depend on baseline
expenditure shares -- i.e., on observables.

Validation: the resulting expression is evaluated at the numeric free-trade
baselines for the referee's size configurations and must reproduce the
brute-force thresholds rho* = 8.76 (Vietnam), 4.32 (EU), 4.24 (equal),
3.78 (ROW) at aD=.80, aT=.40, eta=1.5, L_B=1.21.

Run:  python scripts/derive_general_threshold.py
"""

import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_referee_claims import (  # noqa: E402
    d_log_eAC, nested_equilibrium, zero_tau,
)


def build_symbolic(free_baseline=False):
    """Symbolic nested model. If free_baseline, evaluate derivatives at a
    general baseline (vB0, vC0) instead of the symmetric point (1, 1)."""
    nuB, nuC, t = sp.symbols("nu_B nu_C tau", real=True)
    aT, aD, eta, rho = sp.symbols("alpha_T alpha_D eta rho", positive=True)
    b, c = sp.symbols("L_B L_C", positive=True)          # sizes
    vB0, vC0 = sp.symbols("v_B0 v_C0", positive=True)    # baseline wages

    idx = ["A", "B", "C"]
    v = {"A": sp.Integer(1), "B": sp.exp(nuB), "C": sp.exp(nuC)}
    L = {"A": sp.Integer(1), "B": b, "C": c}
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
    I = {i: v[i] * L[i] / (1 - sum(tau[i][j] / (1 + tau[i][j]) * sh[i][j]
                                   for j in idx if j != i)) for i in idx}
    E = {i: {j: sh[i][j] * I[i] for j in idx} for i in idx}
    TB = {i: (sum(E[k][i] / (1 + tau[k][i]) for k in idx if k != i)
              - sum(E[i][j] / (1 + tau[i][j]) for j in idx if j != i))
          for i in idx}

    F = sp.Matrix([TB["B"], TB["C"]])
    X = sp.Matrix([nuB, nuC])
    if free_baseline:
        base = {nuB: sp.log(vB0), nuC: sp.log(vC0), t: 0}
    else:
        base = {nuB: 0, nuC: 0, t: 0, b: 1, c: 1}
    J = F.jacobian(X).subs(base)
    Ft = sp.Matrix([sp.diff(F[k], t) for k in range(2)]).subs(base)

    syms = dict(nuB=nuB, nuC=nuC, t=t, aT=aT, aD=aD, eta=eta, rho=rho,
                b=b, c=c, vB0=vB0, vC0=vC0)
    return J, Ft, syms


def main():
    # ------------------------------------------------------------------
    # Step 1: equal sizes -- reproduce rho* = 3[1 + aD(eta-1) - aT(1-aD)]
    # ------------------------------------------------------------------
    print("Step 1: equal-size threshold (sanity)")
    J, Ft, s = build_symbolic(free_baseline=False)
    dC = sp.simplify((-J.inv() * Ft)[1])
    num, den = sp.fraction(sp.cancel(sp.together(dC)))
    rs = sp.solve(sp.Eq(sp.expand(num), 0), s["rho"])
    print("  rho* =", sp.simplify(rs[0]))
    target = 3 * (1 + s["aD"] * (s["eta"] - 1) - s["aT"] * (1 - s["aD"]))
    assert sp.simplify(rs[0] - target) == 0
    print("  matches 3[1 + aD(eta-1) - aT(1-aD)]  [OK]\n")

    # ------------------------------------------------------------------
    # Step 2: general sizes at a symbolic baseline (vB0, vC0)
    # ------------------------------------------------------------------
    print("Step 2: general-size numerator, collected in rho")
    J, Ft, s = build_symbolic(free_baseline=True)
    sol = -J.inv() * Ft                     # [d nuB/dt, d nuC/dt]
    dC = sp.together(sp.cancel(sp.together(sol[1])))
    num, den = sp.fraction(dC)
    num_poly = sp.Poly(sp.expand(num), s["rho"])
    print("  degree of numerator in rho:", num_poly.degree())

    coeffs = num_poly.all_coeffs()
    # Save the full expressions for later use (paper appendix)
    out = ROOT / "output" / "general_threshold_symbolic.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write("d log e_AC / d tau |_{tau=0} = N / D at baseline (vB0, vC0)\n\n")
        f.write("N (collected in rho, highest degree first):\n")
        for k, cf in enumerate(coeffs):
            f.write(f"\n-- coeff of rho^{num_poly.degree()-k} --\n")
            f.write(sp.sstr(sp.factor(sp.simplify(cf))) + "\n")
        f.write("\nD:\n" + sp.sstr(sp.simplify(den)) + "\n")
    print(f"  full coefficients written to {out}")

    # ------------------------------------------------------------------
    # Step 3: numeric validation against brute-force thresholds
    # ------------------------------------------------------------------
    print("\nStep 3: validate quadratic-root threshold against brute force")
    aD_v, aT_v, eta_v, LB_v = 0.80, 0.40, 1.5, 1.21
    lam_num = sp.lambdify(
        (s["rho"], s["aD"], s["aT"], s["eta"], s["b"], s["c"],
         s["vB0"], s["vC0"]),
        sp.expand(num), "numpy")

    configs = [("Vietnam", 0.055, (6, 14)), ("EU", 0.86, (2, 10)),
               ("equal", 1.00, (2, 10)), ("ROW", 3.51, (2, 10))]
    for lab, LC_v, (lo, hi) in configs:
        L = [1, LB_v, LC_v]

        def num_at(r):
            nu0 = nested_equilibrium(zero_tau(), aD_v, aT_v, eta_v, r, L)
            return lam_num(r, aD_v, aT_v, eta_v, LB_v, LC_v,
                           np.exp(nu0[0]), np.exp(nu0[1]))

        rs_sym = brentq(num_at, lo, hi, xtol=1e-8)
        rs_num = brentq(lambda r: d_log_eAC(r, aD_v, aT_v, eta_v, L), lo, hi)
        print(f"  {lab:8s} L_C={LC_v:5.3f}  symbolic-root rho* = {rs_sym:7.4f}"
              f"   brute-force = {rs_num:7.4f}   diff = {rs_sym-rs_num:+.2e}")
        assert abs(rs_sym - rs_num) < 1e-3

    print("\nAll validations passed.")


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
