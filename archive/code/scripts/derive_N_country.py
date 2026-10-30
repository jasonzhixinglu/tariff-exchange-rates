"""
Symmetric N-country threshold: derive rho*(N) in closed form.

Setup: N countries, one tariffer A, one target B, k = N-2 identical
bystanders (representative c); n = N-1 foreign partners per country,
symmetric origin weights 1/n, home share aD, tradable share aT.
By symmetry the linearized system has two unknowns (nu_B, nu_C).

Outputs: d nu_C / d tau at tau=0, its root rho*(N), checks that N=3
reproduces rho* = 3[1 + aD(eta-1) - aT(1-aD)], and a numerical
verification at N=4 against the nonlinear model.

Run:  python scripts/derive_N_country.py
"""

import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq, fsolve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def symbolic_N():
    nuB, nuC, t = sp.symbols("nu_B nu_C tau", real=True)
    aT, aD, eta, rho = sp.symbols("alpha_T alpha_D eta rho", positive=True)
    k = sp.symbols("k", positive=True)          # number of bystanders, N-2
    n = k + 1                                    # foreign partners, N-1

    vB, vC = sp.exp(nuB), sp.exp(nuC)
    aM = 1 - aD

    def shares(p_home, foreign):
        """foreign: list of (multiplicity, price). Returns (P_M, P_T, dict of
        per-origin income shares s_j given weight 1/n each)."""
        PMpow = sum(m * p ** (1 - rho) for m, p in foreign) / n
        PM = PMpow ** (1 / (1 - rho))
        PTpow = aD * p_home ** (1 - eta) + aM * PM ** (1 - eta)
        PT = PTpow ** (1 / (1 - eta))
        outer = aT * aM * (PM / PT) ** (1 - eta)
        s = [outer * (p ** (1 - rho) / (n * PMpow)) for m, p in foreign]
        return s

    # A: foreign = {B at (1+t)vB, k bystanders at vC}
    sA = shares(sp.Integer(1), [(1, (1 + t) * vB), (k, vC)])
    s_AB, s_Ac = sA[0], sA[1]
    # B: foreign = {A at 1, k bystanders at vC}
    sB = shares(vB, [(1, sp.Integer(1)), (k, vC)])
    s_BA, s_Bc = sB[0], sB[1]
    # bystander c: foreign = {A at 1, B at vB, k-1 others at vC}
    sc = shares(vC, [(1, sp.Integer(1)), (1, vB), (k - 1, vC)])
    s_cA, s_cB = sc[0], sc[1]

    I_A = 1 / (1 - (t / (1 + t)) * s_AB)
    I_B, I_c = vB, vC

    TB_B = s_AB * I_A / (1 + t) + k * s_cB * I_c - (s_BA + k * s_Bc) * I_B
    TB_c = s_Ac * I_A + s_Bc * I_B - (s_cA + s_cB) * I_c

    F = sp.Matrix([TB_B, TB_c])
    base = {nuB: 0, nuC: 0, t: 0}
    J = sp.simplify(F.jacobian(sp.Matrix([nuB, nuC])).subs(base))
    Ft = sp.simplify(sp.Matrix([sp.diff(F[i], t) for i in range(2)]).subs(base))
    sol = sp.simplify(-J.inv() * Ft)
    dnuB, dnuC = sp.cancel(sp.together(sol[0])), sp.cancel(sp.together(sol[1]))
    return dnuB, dnuC, dict(aT=aT, aD=aD, eta=eta, rho=rho, k=k)


def main():
    dnuB, dnuC, s = symbolic_N()
    aT, aD, eta, rho, k = (s[x] for x in ("aT", "aD", "eta", "rho", "k"))

    num, den = sp.fraction(dnuC)
    rho_star_N = sp.solve(sp.Eq(sp.expand(num), 0), rho)
    rsN = sp.simplify(rho_star_N[0])
    print("d nu_C / d tau numerator (factored):", sp.factor(sp.expand(num)))
    print("d nu_C / d tau denominator (factored):", sp.factor(sp.expand(den)))
    print()
    print("rho*(N) =", sp.simplify(rsN))
    print("rho*(N) factored:", sp.factor(rsN))

    # N = 3 check (k = 1)
    rs3 = sp.simplify(rsN.subs(k, 1))
    target = 3 * (1 + aD * (eta - 1) - aT * (1 - aD))
    print("\nN=3 (k=1):", rs3, " -> matches 3[1+aD(eta-1)-aT(1-aD)]:",
          sp.simplify(rs3 - target) == 0)

    # limits
    print("k -> oo limit of rho*(N):", sp.limit(rsN, k, sp.oo))

    # also dnuB at N=3 check
    rsB3 = sp.simplify(dnuB.subs(k, 1))
    print("d nu_B/d tau at N=3:", sp.simplify(rsB3))

    # ------------------------------------------------------------------
    # Numerical verification at N = 4 (k = 2)
    # ------------------------------------------------------------------
    aD_v, aT_v, eta_v = 0.8, 0.4, 1.5
    rs4_expr = rsN.subs({k: 2, aD: aD_v, aT: aT_v, eta: eta_v})
    rs4 = float(rs4_expr)

    def alloc4(nu, tauAB, rho_v):
        N4 = 4
        I = range(N4)
        v = np.exp(np.r_[0.0, nu])          # nu = (nuB, nuC1, nuC2)
        aM = 1 - aD_v
        r = rho_v
        e = eta_v
        tau = np.zeros((N4, N4)); tau[0, 1] = tauAB
        p = np.array([[(1 + tau[i][j]) * v[j] for j in I] for i in I])
        beta = np.full((N4, N4), 1 / 3.); np.fill_diagonal(beta, 0)
        sh = np.zeros((N4, N4))
        for i in I:
            f = [j for j in I if j != i]
            PM = sum(beta[i][j] * p[i][j] ** (1 - r) for j in f) ** (1 / (1 - r))
            PT = (aD_v * p[i][i] ** (1 - e) + aM * PM ** (1 - e)) ** (1 / (1 - e))
            sh[i][i] = aT_v * aD_v * p[i][i] ** (1 - e) / PT ** (1 - e)
            for j in f:
                sh[i][j] = (aT_v * aM * PM ** (1 - e) / PT ** (1 - e)
                            * beta[i][j] * p[i][j] ** (1 - r) / PM ** (1 - r))
        inc = np.array([v[i] / (1 - sum(tau[i][j] / (1 + tau[i][j]) * sh[i][j]
                                        for j in I if j != i)) for i in I])
        E = np.array([[sh[i][j] * inc[i] for j in I] for i in I])
        return np.array([sum(E[m][i] / (1 + tau[m][i]) for m in I if m != i)
                         - sum(E[i][j] / (1 + tau[i][j]) for j in I if j != i)
                         for i in I])

    def slope4(rho_v, h=1e-6):
        g = lambda tt: fsolve(lambda x: alloc4(x, tt, rho_v)[1:],
                              np.zeros(3), xtol=1e-12)
        return (g(h)[1] - g(0.0)[1]) / h        # bystander response

    rs4_num = brentq(lambda r_: slope4(r_), 1.5, 12.0, xtol=1e-6)
    print(f"\nN=4 check (aD=.8, aT=.4, eta=1.5): formula rho*(4) = {rs4:.4f}, "
          f"numeric = {rs4_num:.4f}, diff = {rs4 - rs4_num:+.2e}")
    assert abs(rs4 - rs4_num) < 1e-3

    # war threshold: nu_C^war = 2 nu_C - nu_B; root in rho at N=3 and N=4
    war = sp.cancel(sp.together(2 * dnuC - dnuB))
    wnum = sp.fraction(war)[0]
    for kk in (1, 2):
        wt = sp.solve(sp.Eq(sp.expand(wnum.subs(k, kk)), 0), rho)
        print(f"war threshold, k={kk}:", [sp.simplify(x) for x in wt])

    print("\nAll checks passed.")


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
