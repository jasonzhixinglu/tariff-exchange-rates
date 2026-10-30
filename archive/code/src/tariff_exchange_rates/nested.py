"""
Nested-CES three-country model: separate home-vs-import and cross-origin
elasticities (Phase 2 of the revision; referee report section 5).

Preference structure for country i (weights NOT raised to a power —
"plain weight" CES convention, matching the paper's revised notation):

  C_i   = C_Ti^alpha_T * C_Ni^(1 - alpha_T)          (Cobb-Douglas outer)
  C_Ti  = [ alpha_D * C_ii^((eta-1)/eta)
            + (1 - alpha_D) * M_i^((eta-1)/eta) ]^(eta/(eta-1))
  M_i   = [ sum_{j != i} beta[i,j] * C_ji^((rho-1)/rho) ]^(rho/(rho-1))

  eta : macro (home-vs-import) Armington elasticity
  rho : micro (cross-origin) elasticity across foreign suppliers

The flat single-elasticity model is the special case rho = eta (the nest
collapses to one CES over all varieties with weights
{alpha_D, (1-alpha_D) beta[i,j]}).

Key analytic result (equal sizes, symmetric weights beta = 1/2, tau -> 0):

  d log e_AC / d tau = (rho - rho*) / (3 [3 alpha_D (eta - 1) + rho + 1])
  rho* = 3 [1 + alpha_D (eta - 1) - alpha_T (1 - alpha_D)]

Country A's currency depreciates against the untariffed third country C
iff rho > rho*.  See scripts/verify_referee_claims.py and
scripts/derive_general_threshold.py for verification.
"""

import warnings

import numpy as np
from scipy.optimize import brentq, root


def compute_allocation_nested(params, exchange_rates, tariffs):
    """
    Full GE allocation of the nested model given exchange rates and tariffs.

    Parameters
    ----------
    params : dict with keys
        productivity_T : (n,)   tradable TFP
        productivity_N : (n,)   nontradable TFP
        labor          : (n,)   labor endowments
        alpha_T        : float  expenditure share of the tradable bundle
        alpha_D        : (n,) or float  home share within tradables, per country
        beta           : (n, n) import weights within the import bundle;
                         beta[i, j] = weight country i puts on origin j != i,
                         rows sum to 1 over j != i (diagonal ignored).
                         Default: equal weights 1/(n-1).
        eta            : float  home-vs-import elasticity
        rho            : float  cross-origin elasticity
        prices_T       : (n,)   producer prices (normalize to 1)
    exchange_rates : (n-1,) free rates [e_{01}, ...] relative to country 0.
    tariffs : (n, n) ad valorem rates, tariffs[i, j] = i's tariff on j.

    Returns
    -------
    dict with the same keys as economy.compute_allocation, plus
    "shares" (n, n): realized expenditure share of TOTAL income on each
    variety (rows sum to alpha_T).
    """
    productivity_T = np.asarray(params["productivity_T"], dtype=float)
    productivity_N = np.asarray(params["productivity_N"], dtype=float)
    labor          = np.asarray(params["labor"],          dtype=float)
    alpha_T        = float(params["alpha_T"])
    eta            = float(params["eta"])
    rho            = float(params["rho"])
    prices_T       = np.asarray(params["prices_T"],       dtype=float)
    tariffs        = np.asarray(tariffs, dtype=float)

    n = len(productivity_T)
    alpha_D = np.broadcast_to(
        np.asarray(params["alpha_D"], dtype=float), (n,)).copy()
    beta = params.get("beta")
    if beta is None:
        beta = np.full((n, n), 1.0 / (n - 1))
    beta = np.asarray(beta, dtype=float).copy()
    np.fill_diagonal(beta, 0.0)
    row_sums = beta.sum(axis=1)
    if not np.allclose(row_sums, 1.0):
        raise ValueError(f"beta rows must sum to 1 over j != i, got {row_sums}")

    # Avoid the removable singularities at eta = 1 or rho = 1
    if abs(eta - 1.0) < 1e-8:
        eta = 1.0 + 1e-8
    if abs(rho - 1.0) < 1e-8:
        rho = 1.0 + 1e-8

    # Exchange rate matrix via no-arbitrage
    free_rates = np.asarray(exchange_rates, dtype=float)
    assert len(free_rates) == n - 1
    r = np.concatenate([[1.0], free_rates])
    E = np.outer(1.0 / r, r)

    wages    = productivity_T * prices_T
    prices_N = wages / productivity_N

    # Consumer prices Pc[i, j] = (1 + tau[i,j]) E[i,j] P_T[j]
    Pc = (1.0 + tariffs) * E * prices_T[np.newaxis, :]

    # ------------------------------------------------------------------
    # Price indices and realized expenditure shares
    #   P_M[i]  = [sum_{j != i} beta[i,j] Pc[i,j]^(1-rho)]^(1/(1-rho))
    #   P_T[i]  = [aD[i] Pc[i,i]^(1-eta) + (1-aD[i]) P_M[i]^(1-eta)]^(1/(1-eta))
    #   share of TOTAL income on home variety:
    #       s[i,i] = alpha_T * aD[i] (Pc[i,i]/P_T[i])^(1-eta)
    #   on foreign variety j:
    #       s[i,j] = alpha_T * (1-aD[i]) (P_M[i]/P_T[i])^(1-eta)
    #                * beta[i,j] (Pc[i,j]/P_M[i])^(1-rho)
    # ------------------------------------------------------------------
    off = ~np.eye(n, dtype=bool)
    PM_pow = np.where(off, beta * Pc ** (1.0 - rho), 0.0).sum(axis=1)
    P_M = PM_pow ** (1.0 / (1.0 - rho))
    home_p = np.diag(Pc)
    PT_pow = alpha_D * home_p ** (1.0 - eta) + (1.0 - alpha_D) * P_M ** (1.0 - eta)
    P_T_agg = PT_pow ** (1.0 / (1.0 - eta))

    shares = np.where(
        off,
        alpha_T
        * ((1.0 - alpha_D) * (P_M / P_T_agg) ** (1.0 - eta))[:, np.newaxis]
        * beta * (Pc / P_M[:, np.newaxis]) ** (1.0 - rho),
        0.0,
    )
    np.fill_diagonal(
        shares, alpha_T * alpha_D * (home_p / P_T_agg) ** (1.0 - eta))

    # ------------------------------------------------------------------
    # Disposable income with lump-sum rebate (realized shares; shares are
    # price-only, so the fixed point is a single division)
    # ------------------------------------------------------------------
    tariff_frac = tariffs / (1.0 + tariffs)
    income = wages * labor / (1.0 - (shares * tariff_frac).sum(axis=1))

    # Demands
    demand_T = shares * income[:, np.newaxis] / Pc
    demand_N = (1.0 - alpha_T) * income / prices_N

    # Trade balance in own currency (domestic terms cancel: E[i,i] = 1)
    trade_balance = demand_T.sum(axis=0) - (E * demand_T).sum(axis=1)

    price_level = P_T_agg ** alpha_T * prices_N ** (1.0 - alpha_T)
    real_exchange_rate = E * price_level[np.newaxis, :] / price_level[:, np.newaxis]

    return {
        "exchange_matrix":    E,
        "wages":              wages,
        "prices_N":           prices_N,
        "consumer_prices":    Pc,
        "income":             income,
        "shares":             shares,
        "demand_T":           demand_T,
        "demand_N":           demand_N,
        "trade_balance":      trade_balance,
        "price_level":        price_level,
        "real_exchange_rate": real_exchange_rate,
    }


def solve_3country_nested(params, tariffs, init=None):
    """
    Equilibrium (e_AB, e_AC) of the nested three-country model:
    TB_B = TB_C = 0 (TB_A = 0 by Walras). Same return structure as
    equilibrium.solve_3country.
    """
    tariffs_arr = np.asarray(tariffs, dtype=float)

    def _residuals(log_e):
        alloc = compute_allocation_nested(params, np.exp(log_e), tariffs_arr)
        return [alloc["trade_balance"][1], alloc["trade_balance"][2]]

    labor = np.asarray(params["labor"], dtype=float)
    candidates = []
    if init is not None:
        candidates.append(np.asarray(init, dtype=float))
    # Size-aware default start (free-trade wages scale with size) + coarse grid
    candidates.append(np.log(labor[1:] / labor[0]))
    for a in (-0.5, 0.0, 0.5):
        for b in (-0.5, 0.0, 0.5):
            candidates.append(np.array([a, b]))

    best_sol, best_norm = None, np.inf
    for x0 in candidates:
        try:
            sol = root(_residuals, x0, method="hybr", options={"xtol": 1e-12})
            norm = np.linalg.norm(sol.fun)
            if norm < best_norm:
                best_sol, best_norm = sol, norm
        except Exception:
            continue

    if best_norm > 1e-6:
        warnings.warn(
            f"solve_3country_nested: solver may not have converged "
            f"(residual norm = {best_norm:.2e})")

    log_e_AB, log_e_AC = best_sol.x
    e_AB, e_AC = np.exp(log_e_AB), np.exp(log_e_AC)
    e_BC = e_AC / e_AB
    alloc = compute_allocation_nested(params, [e_AB, e_AC], tariffs_arr)
    P = alloc["price_level"]

    return {
        "e_AB": e_AB, "e_AC": e_AC, "e_BC": e_BC,
        "log_e_AB": log_e_AB, "log_e_AC": log_e_AC, "log_e_BC": np.log(e_BC),
        "log_q_AB": np.log(e_AB * P[1] / P[0]),
        "log_q_AC": np.log(e_AC * P[2] / P[0]),
        "log_q_BC": np.log(e_BC * P[2] / P[1]),
        "allocation": alloc,
        "residual_norm": best_norm,
    }


# ---------------------------------------------------------------------------
# Threshold utilities
# ---------------------------------------------------------------------------

def rho_star_symmetric(alpha_D, alpha_T, eta):
    """Analytic reversal threshold at the symmetric point (equal sizes,
    beta = 1/2, tau -> 0): rho* = 3 [1 + aD (eta-1) - aT (1-aD)].
    A's currency depreciates against untariffed C iff rho > rho*."""
    return 3.0 * (1.0 + alpha_D * (eta - 1.0) - alpha_T * (1.0 - alpha_D))


def make_params_nested(alpha_T, alpha_D, eta, rho, labor=(1.0, 1.0, 1.0),
                       beta=None, productivity_T=None, productivity_N=None):
    """Convenience constructor for the 3-country nested model."""
    n = len(labor)
    return {
        "productivity_T": np.ones(n) if productivity_T is None else np.asarray(productivity_T, float),
        "productivity_N": np.ones(n) if productivity_N is None else np.asarray(productivity_N, float),
        "labor":    np.asarray(labor, dtype=float),
        "alpha_T":  alpha_T,
        "alpha_D":  alpha_D,
        "beta":     beta,
        "eta":      eta,
        "rho":      rho,
        "prices_T": np.ones(n),
    }


def d_log_eAC_dtau(params, tau0=0.0, h=1e-6):
    """Numerical d log e_AC / d tau at tau = tau0 (isolated tariff by A on B)."""
    T0 = np.zeros((3, 3))
    T0[0, 1] = tau0
    T1 = T0.copy()
    T1[0, 1] = tau0 + h
    eq0 = solve_3country_nested(params, T0)
    eq1 = solve_3country_nested(params, T1,
                                init=[eq0["log_e_AB"], eq0["log_e_AC"]])
    return (eq1["log_e_AC"] - eq0["log_e_AC"]) / h


def rho_star_numeric(alpha_T, alpha_D, eta, labor=(1.0, 1.0, 1.0), beta=None,
                     tau0=0.0, cumulative=False, lo=1.05, hi=20.0):
    """
    General reversal threshold by root-finding in rho.

    cumulative=False: rho s.t. the marginal response d log e_AC/d tau = 0
                      at tau = tau0.
    cumulative=True:  rho s.t. the TOTAL change log e_AC(tau0) - log e_AC(0)
                      = 0 (requires tau0 > 0); the policy-relevant threshold
                      for a discrete tariff.
    """
    def crit(rho):
        p = make_params_nested(alpha_T, alpha_D, eta, rho, labor, beta)
        if cumulative:
            if tau0 <= 0:
                raise ValueError("cumulative threshold needs tau0 > 0")
            T = np.zeros((3, 3))
            T[0, 1] = tau0
            eq0 = solve_3country_nested(p, np.zeros((3, 3)))
            eq1 = solve_3country_nested(p, T,
                                        init=[eq0["log_e_AB"], eq0["log_e_AC"]])
            return eq1["log_e_AC"] - eq0["log_e_AC"]
        return d_log_eAC_dtau(p, tau0=tau0)

    return brentq(crit, lo, hi, xtol=1e-6)
