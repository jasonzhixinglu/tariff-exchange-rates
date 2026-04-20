"""
Equilibrium solvers for 2-country and 3-country trade models.

Both solvers search in log exchange rate space for better numerical behaviour.

2-country: one free rate (e_AB); solved with Brent's scalar root-finder.
3-country: two free rates (e_AB, e_AC); solved with a multi-start 2D root-finder.
           e_BC is fully determined by no-arbitrage once e_AB and e_AC are known.
"""

import warnings
import numpy as np
from scipy.optimize import brentq, root

from .economy import compute_allocation


def solve_2country(params, tau=0.0, log_e_bounds=(-3.0, 3.0)):
    """
    Solve for the equilibrium exchange rate in the 2-country model.

    Country A imposes ad valorem tariff tau on imports from B. All other
    bilateral tariffs are zero. Uses Brent's method on country A's trade
    balance over the log exchange rate.

    Parameters
    ----------
    params       : dict  — model parameters (see economy.compute_allocation)
    tau          : float — A's tariff on B's goods (0.0 = free trade)
    log_e_bounds : tuple — (lower, upper) bounds for log(e_AB) in Brent search

    Returns
    -------
    dict with keys:
        e_AB       : float  — equilibrium nominal exchange rate
        log_e_AB   : float  — log of e_AB
        tau        : float  — tariff used
        allocation : dict   — full allocation at equilibrium (see economy.py)
    """
    tariffs = np.array([[0.0, tau], [0.0, 0.0]])

    def _trade_balance_A(log_e):
        alloc = compute_allocation(params, [np.exp(log_e)], tariffs)
        return alloc["trade_balance"][0]

    log_e_star = brentq(_trade_balance_A, *log_e_bounds)
    e_star     = np.exp(log_e_star)
    alloc      = compute_allocation(params, [e_star], tariffs)

    return {
        "e_AB":      e_star,
        "log_e_AB":  log_e_star,
        "tau":       tau,
        "allocation": alloc,
    }


def solve_3country(params, tariffs, n_starts=9, init=None):
    """
    Solve for equilibrium exchange rates in the 3-country model.

    Finds (e_AB, e_AC) such that TB_B = TB_C = 0. By Walras' law TB_A = 0
    follows. Searches in log space with multiple starting points for
    robustness at high sigma or asymmetric calibrations.

    Parameters
    ----------
    params   : dict          — model parameters (see economy.compute_allocation)
    tariffs  : array (3, 3)  — tariff matrix (see tariffs.py)
    n_starts : int           — number of starting points to try (default 9)
    init     : array (2,)    — preferred initial guess for [log_e_AB, log_e_AC]
                               (default [0, 0], i.e. e_AB = e_AC = 1)

    Returns
    -------
    dict with keys:
        e_AB, e_AC, e_BC          : float  — equilibrium nominal exchange rates
        log_e_AB, log_e_AC, log_e_BC : float
        log_q_AB, log_q_AC, log_q_BC : float — log real exchange rates
        allocation                 : dict   — full allocation at equilibrium
        residual_norm              : float  — solver residual (TB_B^2 + TB_C^2)^0.5
    """
    tariffs_arr = np.asarray(tariffs, dtype=float)

    def _residuals(log_e):
        e_AB, e_AC = np.exp(log_e)
        alloc = compute_allocation(params, [e_AB, e_AC], tariffs_arr)
        return [alloc["trade_balance"][1], alloc["trade_balance"][2]]

    # Build starting points: user-supplied init + a 3x3 coarse grid
    candidates = [np.asarray(init if init is not None else [0.0, 0.0])]
    for a in (-0.5, 0.0, 0.5):
        for b in (-0.5, 0.0, 0.5):
            candidates.append(np.array([a, b]))
    candidates = candidates[:n_starts]

    best_sol, best_norm = None, np.inf
    for x0 in candidates:
        try:
            sol  = root(_residuals, x0, method="hybr", options={"xtol": 1e-12})
            norm = np.linalg.norm(sol.fun)
            if norm < best_norm:
                best_sol  = sol
                best_norm = norm
        except Exception:
            continue

    if best_norm > 1e-6:
        warnings.warn(
            f"solve_3country: solver may not have converged "
            f"(residual norm = {best_norm:.2e})"
        )

    log_e_AB, log_e_AC = best_sol.x
    e_AB = np.exp(log_e_AB)
    e_AC = np.exp(log_e_AC)
    e_BC = e_AC / e_AB          # no-arbitrage: E[1,2] = r[2]/r[1] = e_AC/e_AB

    alloc = compute_allocation(params, [e_AB, e_AC], tariffs_arr)
    P     = alloc["price_level"]

    return {
        "e_AB":      e_AB,
        "e_AC":      e_AC,
        "e_BC":      e_BC,
        "log_e_AB":  log_e_AB,
        "log_e_AC":  log_e_AC,
        "log_e_BC":  np.log(e_BC),
        "log_q_AB":  np.log(e_AB * P[1] / P[0]),
        "log_q_AC":  np.log(e_AC * P[2] / P[0]),
        "log_q_BC":  np.log(e_BC * P[2] / P[1]),
        "allocation": alloc,
        "residual_norm": best_norm,
    }
