"""
Ricardo-Viner prototype (Phase 4.7 / decision D1 / memo M5).

Technology:  Y_Ti = A_Ti * L_Ti^gamma  (gamma <= 1; gamma < 1 = sector-specific
             fixed factor in tradables, earning rents (1-gamma) P_Ti Y_Ti that
             are distributed lump-sum to households).
             Y_Ni = A_Ni * L_Ni  (linear, so P_Ni = w_i / A_Ni).
Labor mobile across sectors within a country: w_i = gamma A_Ti L_Ti^(gamma-1)
(own currency, producer price P_Ti = 1). gamma = 1 reduces to the baseline.

Demand: the nested (eta, rho) system of the paper, CD outer at alpha_T.

Equilibrium unknowns: {L_TA, L_TB, L_TC, nu_B, nu_C} where nu_j = log e_Aj.
Equations: nontradable market clearing in each country (3) + balanced trade
for B and C (2); variety market clearing / TB_A follow by Walras (checked).

Question: how does the reversal threshold rho* move with gamma? The referee
(report 3.4) expects DRS in C's export sector to concentrate diverted demand
in C's price (= currency) rather than quantities, LOWERING rho*.

Run:  python scripts/rv_prototype.py
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, fsolve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

AD, AT, ETA = 0.80, 0.40, 1.5     # benchmark preferences
AN = 1.0 - AT


def rv_system(x, tau, gamma, rho, eta=ETA, aD=AD, aT=AT, L=(1.0, 1.0, 1.0)):
    """
    Residuals of the 5-equation system.

    x = [z_A, z_B, z_C, nu_B, nu_C] with L_Ti = L_i / (1 + exp(-z_i))
    (logistic transform keeps 0 < L_Ti < L_i).

    Returns [N-clearing_A, N-clearing_B, N-clearing_C, TB_B, TB_C]
    (all in A's currency for the TBs, own currency for N-clearing).
    """
    if abs(rho - 1) < 1e-8:
        rho = 1 + 1e-8
    if abs(eta - 1) < 1e-8:
        eta = 1 + 1e-8
    I3 = [0, 1, 2]
    L = np.asarray(L, dtype=float)
    LT = L / (1.0 + np.exp(-x[:3]))
    v = np.exp(np.r_[0.0, x[3], x[4]])            # e_Ai (A-currency price of i's good)
    aM = 1 - aD

    w_own = gamma * LT ** (gamma - 1.0)            # own-currency wage (A_Ti = 1)
    Y_T = LT ** gamma

    # A-currency consumer prices p[i][j] = (1 + tau_ij) v_j
    p = np.array([[(1 + tau[i][j]) * v[j] for j in I3] for i in I3])

    # nested expenditure shares of total income (rows sum to aT)
    sh = np.zeros((3, 3))
    for i in I3:
        f = [j for j in I3 if j != i]
        PM = sum(0.5 * p[i][j] ** (1 - rho) for j in f) ** (1 / (1 - rho))
        PT = (aD * p[i][i] ** (1 - eta) + aM * PM ** (1 - eta)) ** (1 / (1 - eta))
        sh[i][i] = aT * aD * p[i][i] ** (1 - eta) / PT ** (1 - eta)
        for j in f:
            sh[i][j] = (aT * aM * PM ** (1 - eta) / PT ** (1 - eta)
                        * 0.5 * p[i][j] ** (1 - rho) / PM ** (1 - rho))

    # income in A currency: wages + fixed-factor rents + tariff rebate
    base_inc = v * (w_own * L + (1 - gamma) * Y_T)
    wedge = np.array([sum(tau[i][j] / (1 + tau[i][j]) * sh[i][j]
                          for j in I3 if j != i) for i in I3])
    I_A = base_inc / (1 - wedge)

    # nontradable clearing (own currency): w_i (L_i - L_Ti) = alpha_N * I_i^own
    res_N = w_own * (L - LT) - (1 - aT) * I_A / v

    # trade balances (A currency, producer prices)
    E = np.array([[sh[i][j] * I_A[i] for j in I3] for i in I3])
    TB = np.array([sum(E[k][i] / (1 + tau[k][i]) for k in I3 if k != i)
                   - sum(E[i][j] / (1 + tau[i][j]) for j in I3 if j != i)
                   for i in I3])
    return np.r_[res_N, TB[1], TB[2]], TB, Y_T, sh, I_A, v


def free_trade_start(gamma, aT=AT, L=(1.0, 1.0, 1.0)):
    """Analytic symmetric free-trade allocation: at tau = 0 and equal wages,
    Y_T = aT * I and I = w L + (1-gamma) Y_T give
    L_T = gamma * aT * L / (1 - aT + gamma * aT)."""
    L = np.asarray(L, dtype=float)
    LT = gamma * aT * L / (1 - aT + gamma * aT)
    z = np.log(LT / (L - LT))
    return np.r_[z, 0.0, 0.0]


def solve_rv(tau, gamma, rho, x0=None, **kw):
    aT = kw.get("aT", AT)
    L = kw.get("L", (1.0, 1.0, 1.0))
    candidates = ([x0] if x0 is not None else []) + [free_trade_start(gamma, aT, L)]
    best, best_norm = None, np.inf
    for c in candidates:
        x, info, ier, _ = fsolve(lambda y: rv_system(y, tau, gamma, rho, **kw)[0],
                                 c, xtol=1e-12, full_output=True)
        norm = np.linalg.norm(info["fvec"])
        if norm < best_norm:
            best, best_norm = x, norm
        if norm < 1e-10:
            break
    assert best_norm < 1e-8, f"no convergence (residual {best_norm:.2e})"
    return best


def zero_tau():
    return [[0.0] * 3 for _ in range(3)]


def isolated(t):
    T = zero_tau()
    T[0][1] = t
    return T


def d_log_eAC(rho, gamma, h=1e-6, tau0=0.0, **kw):
    x0 = solve_rv(isolated(tau0), gamma, rho, **kw)
    x1 = solve_rv(isolated(tau0 + h), gamma, rho, x0=x0, **kw)
    return (x1[4] - x0[4]) / h


def rho_star(gamma, lo=1.2, hi=12.0, tau0=0.0, **kw):
    return brentq(lambda r: d_log_eAC(r, gamma, tau0=tau0, **kw), lo, hi,
                  xtol=1e-6)


def cum_change(rho, gamma, T, **kw):
    x0 = solve_rv(zero_tau(), gamma, rho, **kw)
    x1 = solve_rv(isolated(T), gamma, rho, x0=x0, **kw)
    return x1[4] - x0[4]


def rho_star_cum(gamma, T, lo=1.2, hi=12.0, **kw):
    return brentq(lambda r: cum_change(r, gamma, T, **kw), lo, hi, xtol=1e-6)


def main():
    # ------------------------------------------------------------------
    # Validation at gamma = 1: reduces to the baseline nested model
    # ------------------------------------------------------------------
    print("Validation, gamma = 1 (must reproduce baseline):")
    x = solve_rv(isolated(1.0), 1.0, 4.5)
    print(f"  isolated tau=1, rho=4.5: log e_AB={x[3]:+.4f}  log e_AC={x[4]:+.4f}")
    _, TB, Y_T, sh, I_A, v = rv_system(x, isolated(1.0), 1.0, 4.5)
    print(f"  Walras TB_A = {TB[0]:+.2e};  variety-clearing residuals:",
          np.max(np.abs(Y_T - (sh * I_A[:, None] / np.array(
              [[(1 + isolated(1.0)[i][j]) * v[j] for j in range(3)]
               for i in range(3)])).sum(axis=0))).round(12))
    rs1 = rho_star(1.0)
    print(f"  rho*(gamma=1) = {rs1:.4f}   (baseline nested: 3.9600)")
    assert abs(rs1 - 3.96) < 1e-3

    # ------------------------------------------------------------------
    # The threshold as a function of gamma
    # ------------------------------------------------------------------
    print("\nrho* by gamma (aD=.8, aT=.4, eta=1.5, equal sizes):")
    print(f"  {'gamma':>6} {'rho* (marginal)':>16} {'rho*_cum (tau=1.45)':>20}")
    for g in [1.0, 0.9, 0.8, 2 / 3, 0.5]:
        rs = rho_star(g)
        rc = rho_star_cum(g, 1.45)
        print(f"  {g:>6.3f} {rs:>16.4f} {rc:>20.4f}")

    # size configurations
    print("\nrho* by gamma and third-country size (L_B=1.21):")
    print(f"  {'gamma':>6} {'Vietnam .055':>14} {'EU .86':>10} {'ROW 3.51':>10}")
    for g in [1.0, 0.8, 2 / 3]:
        row = []
        for LC, lo, hi in [(0.055, 2, 14), (0.86, 1.5, 10), (3.51, 1.5, 10)]:
            row.append(rho_star(g, lo=lo, hi=hi, L=(1, 1.21, LC)))
        print(f"  {g:>6.3f} {row[0]:>14.3f} {row[1]:>10.3f} {row[2]:>10.3f}")


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
