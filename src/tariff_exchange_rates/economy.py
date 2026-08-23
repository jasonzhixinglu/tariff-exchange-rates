"""
Core general equilibrium allocation for an N-country, 2-sector, 1-factor model.

Sectors:  tradable (T) and nontradable (N).
Factor:   labor, mobile across sectors within a country but not across countries.
Utility:  nested CES — Cobb-Douglas outer layer (tradable bundle vs. nontradables),
          CES inner layer (substitution across tradable varieties). Cobb-Douglas is
          the sigma = 1 special case of the inner CES.

Exchange rate convention:
  E[i, j] = units of country i's currency per unit of country j's currency.
  The function takes n-1 "free" rates relative to country 0 (the numeraire):
    exchange_rates = [e_{0,1}, e_{0,2}, ..., e_{0,n-1}]
  All cross-rates are derived by no-arbitrage:
    E[i, j] = e_{0,j} / e_{0,i}
"""

import numpy as np
from scipy.special import logsumexp


def compute_allocation(params, exchange_rates, tariffs):
    """
    Compute full GE allocation given parameters, exchange rates, and tariffs.

    Parameters
    ----------
    params : dict
        Keys (all array-like unless noted):
          productivity_T  : shape (n,)  — tradable sector TFP
          productivity_N  : shape (n,)  — nontradable sector TFP
          labor           : shape (n,)  — labor endowments
          alpha_T         : shape (n,)  — expenditure weight on each country's tradable
          alpha_N         : float       — expenditure weight on nontradables
          sigma           : float       — CES elasticity of substitution (1.0 → CD)
          prices_T        : shape (n,)  — tradable good prices (normalize to 1)
    exchange_rates : array-like, shape (n-1,)
        Free bilateral rates [e_{01}, e_{02}, ...] relative to numeraire country 0.
    tariffs : array-like, shape (n, n)
        tariffs[i, j] = ad valorem rate imposed by country i on goods from country j.
        Diagonal entries must be zero.

    Returns
    -------
    dict with keys:
        exchange_matrix      : (n, n)  — full bilateral exchange rate matrix E
        wages                : (n,)    — nominal wages
        prices_N             : (n,)    — nontradable good prices
        consumer_prices      : (n, n)  — consumer prices Pc[i, j]
        income               : (n,)    — disposable income (with tariff rebate)
        demand_T             : (n, n)  — tradable demand: demand_T[i, j] = i's demand for j's good
        demand_N             : (n,)    — nontradable demand
        trade_balance        : (n,)    — exports minus imports in own currency
        price_level          : (n,)    — aggregate price index
        real_exchange_rate   : (n, n)  — bilateral real exchange rates RER[i, j]
    """
    productivity_T = np.asarray(params["productivity_T"], dtype=float)
    productivity_N = np.asarray(params["productivity_N"], dtype=float)
    labor          = np.asarray(params["labor"],          dtype=float)
    alpha_T        = np.asarray(params["alpha_T"],        dtype=float)
    alpha_N        = float(params["alpha_N"])
    sigma          = float(params["sigma"])
    prices_T       = np.asarray(params["prices_T"],       dtype=float)
    tariffs        = np.asarray(tariffs, dtype=float)

    n = len(productivity_T)
    free_rates = np.asarray(exchange_rates, dtype=float)
    assert len(free_rates) == n - 1, f"Expected {n-1} free rates, got {len(free_rates)}"

    # ------------------------------------------------------------------
    # Exchange rate matrix via no-arbitrage
    #   r[0] = 1 (numeraire), r[k] = e_{0,k}
    #   E[i, j] = r[j] / r[i]
    # ------------------------------------------------------------------
    r = np.concatenate([[1.0], free_rates])
    E = np.outer(1.0 / r, r)

    # ------------------------------------------------------------------
    # Wages and nontradable prices (competitive factor market)
    #   w_i = A_T_i * P_T_i
    #   P_N_i = w_i / A_N_i
    # ------------------------------------------------------------------
    wages    = productivity_T * prices_T
    prices_N = wages / productivity_N

    # ------------------------------------------------------------------
    # Consumer prices
    #   Pc[i, j] = (1 + tau[i, j]) * E[i, j] * P_T[j]
    # ------------------------------------------------------------------
    Pc = (1.0 + tariffs) * E * prices_T[np.newaxis, :]

    # ------------------------------------------------------------------
    # Realized within-tradable expenditure shares
    #
    #   shares_T[i, j] = share of country i's TRADABLE budget spent on
    #                    variety j (rows sum to 1):
    #
    #   CES:  shares_T[i,j] = alpha_T[j]^sigma * Pc[i,j]^(1-sigma)
    #                         / sum_k alpha_T[k]^sigma * Pc[i,k]^(1-sigma)
    #   CD (sigma=1): shares_T[i,j] = alpha_T[j] / alpha_T_total
    #
    # For sigma != 1 the shares are price-dependent. Computed in log
    # space to avoid overflow at high sigma or extreme prices.
    # ------------------------------------------------------------------
    alpha_T_total = alpha_T.sum()
    log_Pc      = np.log(Pc)
    log_alpha_T = np.log(alpha_T)
    if abs(sigma - 1.0) < 1e-10:
        shares_T = np.tile(alpha_T / alpha_T_total, (n, 1))
    else:
        log_share_terms = sigma * log_alpha_T[np.newaxis, :] + (1.0 - sigma) * log_Pc
        shares_T = np.exp(log_share_terms
                          - logsumexp(log_share_terms, axis=1)[:, np.newaxis])

    # ------------------------------------------------------------------
    # Disposable income with lump-sum tariff rebate
    #
    #   I_i = w_i L_i + sum_j tau[i,j]/(1+tau[i,j]) * (spending on j)
    #       = w_i L_i / (1 - alpha_T_total * sum_j shares_T[i,j] * tau[i,j]/(1+tau[i,j]))
    #
    # Spending on variety j is alpha_T_total * shares_T[i,j] * I_i: the
    # outer CD layer fixes the tradable budget at alpha_T_total * I_i and
    # the inner CES splits it by the realized shares. Shares depend only
    # on prices, not income, so the fixed point in I_i is still a single
    # division. NOTE: using the raw weights alpha_T[j] in the wedge here
    # (as in earlier versions of this code) is exact only at sigma = 1;
    # for sigma != 1 it mismeasures tariff revenue.
    # ------------------------------------------------------------------
    tariff_frac  = tariffs / (1.0 + tariffs)          # diagonal is zero
    tariff_wedge = alpha_T_total * (shares_T * tariff_frac).sum(axis=1)
    income = wages * labor / (1.0 - tariff_wedge)

    # ------------------------------------------------------------------
    # Tradable demand — nested CD-CES (Cobb-Douglas when sigma = 1)
    #
    #   spending:  Pc[i,j] * C_T[i,j] = alpha_T_total * shares_T[i,j] * I_i
    #   quantity:  C_T[i,j] = alpha_T_total * shares_T[i,j] * I_i / Pc[i,j]
    #
    # At sigma = 1 this reduces to C_T[i,j] = alpha_T[j] * I_i / Pc[i,j].
    # Total spending is alpha_T_total * I_i on tradables plus
    # alpha_N * I_i on nontradables, exhausting the budget.
    # ------------------------------------------------------------------
    demand_T = alpha_T_total * shares_T * income[:, np.newaxis] / Pc

    # ------------------------------------------------------------------
    # Nontradable demand
    #   C_N[i] = alpha_N * I_i / P_N_i
    # ------------------------------------------------------------------
    demand_N = alpha_N * income / prices_N

    # ------------------------------------------------------------------
    # Trade balance in own currency
    #
    # Exports of country i = sum over all k of k's demand for i's goods
    #   (valued at i's producer price P_T_i = 1, so unit = i's currency)
    # Imports of country i = sum over all j of i's spending on j's goods
    #   in i's currency = sum_j E[i,j] * C_T[i,j]
    #
    # TB[i] = sum_k demand_T[k,i] - sum_j E[i,j] * demand_T[i,j]
    #       = demand_T.sum(axis=0)[i] - (E * demand_T).sum(axis=1)[i]
    #
    # Domestic purchases (k=i term) cancel since E[i,i] = 1.
    # ------------------------------------------------------------------
    trade_balance = demand_T.sum(axis=0) - (E * demand_T).sum(axis=1)

    # ------------------------------------------------------------------
    # Aggregate price level (nested CD-CES)
    #
    # CES inner: P_T_agg[i] = (sum_j alpha_T[j]^sigma Pc[i,j]^(1-sigma))^(1/(1-sigma))
    # CD inner:  log P_T_agg[i] = sum_j alpha_T[j] log Pc[i,j]
    #
    # Outer CD:  P[i] = P_T_agg[i]^(sum alpha_T) * P_N[i]^alpha_N
    # ------------------------------------------------------------------
    # CES weights are normalized within the tradable bundle
    # (b_j = alpha_T[j]^sigma / sum_k alpha_T[k]^sigma) so that P_T_agg = 1
    # at unit prices and the sigma -> 1 limit is the CD index with weights
    # alpha_T / alpha_T_total. Normalization leaves shares_T unchanged.
    if abs(sigma - 1.0) < 1e-10:
        log_price_T_agg = ((alpha_T / alpha_T_total)[np.newaxis, :] * log_Pc).sum(axis=1)
    else:
        # Log-space aggregation to avoid overflow
        log_b = sigma * log_alpha_T - logsumexp(sigma * log_alpha_T)
        log_price_T_agg = logsumexp(
            log_b[np.newaxis, :] + (1.0 - sigma) * log_Pc, axis=1
        ) / (1.0 - sigma)
    price_T_agg = np.exp(log_price_T_agg)

    price_level = price_T_agg ** alpha_T_total * prices_N ** alpha_N

    # ------------------------------------------------------------------
    # Real exchange rates
    #   RER[i, j] = E[i, j] * P[j] / P[i]
    # ------------------------------------------------------------------
    real_exchange_rate = E * price_level[np.newaxis, :] / price_level[:, np.newaxis]

    return {
        "exchange_matrix":    E,
        "wages":              wages,
        "prices_N":           prices_N,
        "consumer_prices":    Pc,
        "income":             income,
        "demand_T":           demand_T,
        "demand_N":           demand_N,
        "trade_balance":      trade_balance,
        "price_level":        price_level,
        "real_exchange_rate": real_exchange_rate,
    }
