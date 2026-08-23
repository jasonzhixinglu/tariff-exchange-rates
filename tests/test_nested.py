"""
Tests for the nested (eta, rho) model — src/tariff_exchange_rates/nested.py.

Cross-checks:
  * collapse to the flat single-elasticity model when rho = eta
  * analytic threshold rho* and slope formula (referee report section 5.2)
  * referee's numeric results: rho* by third-country size (5.5), trade-war
    comparative statics (4.3), large-tariff thresholds (5.6)
"""

import numpy as np
import pytest

from tariff_exchange_rates.economy import compute_allocation
from tariff_exchange_rates.equilibrium import solve_3country
from tariff_exchange_rates.nested import (
    compute_allocation_nested,
    d_log_eAC_dtau,
    make_params_nested,
    rho_star_numeric,
    rho_star_symmetric,
    solve_3country_nested,
)


def isolated(tau=1.0):
    T = np.zeros((3, 3))
    T[0, 1] = tau
    return T


def trade_war(t_ab, t_ba=None):
    T = np.zeros((3, 3))
    T[0, 1] = t_ab
    T[1, 0] = t_ab if t_ba is None else t_ba
    return T


# ---------------------------------------------------------------------------
# Internal consistency
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("eta,rho", [(1.5, 4.0), (1.0, 1.0), (2.0, 8.0)])
def test_budget_constraint(eta, rho):
    p = make_params_nested(alpha_T=0.4, alpha_D=0.8, eta=eta, rho=rho)
    a = compute_allocation_nested(p, [0.85, 1.1], isolated(0.5))
    spend = (a["consumer_prices"] * a["demand_T"]).sum(axis=1) \
        + a["prices_N"] * a["demand_N"]
    np.testing.assert_allclose(spend, a["income"], rtol=1e-12)


def test_shares_sum_to_alpha_T():
    p = make_params_nested(alpha_T=0.4, alpha_D=0.8, eta=1.5, rho=4.0)
    a = compute_allocation_nested(p, [0.85, 1.1], isolated(0.5))
    np.testing.assert_allclose(a["shares"].sum(axis=1), 0.4, rtol=1e-12)


def test_walras():
    p = make_params_nested(alpha_T=0.4, alpha_D=0.8, eta=1.5, rho=4.0)
    eq = solve_3country_nested(p, isolated(1.0))
    assert abs(eq["allocation"]["trade_balance"][0]) < 1e-9


# ---------------------------------------------------------------------------
# Collapse to the flat single-elasticity model when rho = eta
#
# With rho = eta = sigma the nest is a flat CES over the three varieties
# with plain weights {aD, (1-aD)/2, (1-aD)/2}. The package flat model uses
# the alpha^sigma share convention, so set its weights to the sigma-th
# root of the plain weights (alpha_j = w_j^(1/sigma) up to normalization —
# shares and equilibria are invariant to common rescaling of weights).
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sigma", [0.5, 2.0, 5.0])
def test_collapse_to_flat_ces(sigma):
    aD, aT = 1.0 / 3.0, 0.75
    p_nest = make_params_nested(alpha_T=aT, alpha_D=aD, eta=sigma, rho=sigma)
    w = np.array([aD, (1 - aD) / 2, (1 - aD) / 2])   # plain weights
    alpha_flat = aT * w ** (1.0 / sigma) / (w ** (1.0 / sigma)).sum()
    p_flat = {
        "productivity_T": np.ones(3), "productivity_N": np.ones(3),
        "labor": np.ones(3), "alpha_T": alpha_flat,
        "alpha_N": 1 - aT, "sigma": sigma, "prices_T": np.ones(3),
    }
    eq_n = solve_3country_nested(p_nest, isolated(1.0))
    eq_f = solve_3country(p_flat, isolated(1.0))
    assert eq_n["log_e_AB"] == pytest.approx(eq_f["log_e_AB"], abs=1e-8)
    assert eq_n["log_e_AC"] == pytest.approx(eq_f["log_e_AC"], abs=1e-8)


def test_collapse_matches_symmetric_flat_baseline():
    """rho = eta = sigma with aD = 1/3, aT = 3/4 equals the paper's
    symmetric flat calibration (alpha_Tj = 1/4 each)."""
    p_nest = make_params_nested(alpha_T=0.75, alpha_D=1 / 3, eta=2.0, rho=2.0)
    eq = solve_3country_nested(p_nest, isolated(1.0))
    assert eq["log_e_AB"] == pytest.approx(-0.2110, abs=5e-5)
    assert eq["log_e_AC"] == pytest.approx(-0.0163, abs=5e-5)


# ---------------------------------------------------------------------------
# Analytic threshold and slope (referee 5.2) — completes test 0.3(iii)
# ---------------------------------------------------------------------------

def test_rho_star_symmetric_values():
    assert rho_star_symmetric(0.8, 0.4, 1.5) == pytest.approx(3.96)
    assert rho_star_symmetric(1 / 3, 0.75, 2.0) == pytest.approx(2.50)
    # flat-CES gap: rho*(sigma) - sigma = +0.50 at the paper's calibration
    for s in [0.5, 1.0, 5.0]:
        assert rho_star_symmetric(1 / 3, 0.75, s) - s == pytest.approx(0.50)


@pytest.mark.parametrize("aD,aT,eta,rho", [
    (0.8, 0.4, 1.5, 4.5), (0.8, 0.4, 1.5, 3.0),
    (1 / 3, 0.75, 2.0, 2.0), (0.7, 0.4, 2.0, 6.0),
])
def test_analytic_slope_matches_numeric(aD, aT, eta, rho):
    """d log e_AC/d tau|_0 = (rho - rho*) / (3 [3 aD (eta-1) + rho + 1])."""
    p = make_params_nested(alpha_T=aT, alpha_D=aD, eta=eta, rho=rho)
    analytic = (rho - rho_star_symmetric(aD, aT, eta)) \
        / (3 * (3 * aD * (eta - 1) + rho + 1))
    numeric = d_log_eAC_dtau(p)
    assert numeric == pytest.approx(analytic, abs=1e-6)


def test_sign_reversal_exists_above_threshold():
    """At US-realistic parameters (rho* = 3.96), rho = 4.5 gives genuine
    depreciation of A against untariffed C — the paper's headline case."""
    p = make_params_nested(alpha_T=0.4, alpha_D=0.8, eta=1.5, rho=4.5)
    eq = solve_3country_nested(p, isolated(0.2))
    assert eq["log_e_AC"] > 0          # A depreciates against C
    eq_b = solve_3country_nested(p, isolated(0.2))
    assert eq_b["log_e_AB"] < 0        # while appreciating against B


# ---------------------------------------------------------------------------
# Referee numeric tables
# ---------------------------------------------------------------------------

def test_rho_star_by_size():
    """Referee 5.5: rho* decreasing in L_C (aD=.8, aT=.4, eta=1.5, L_B=1.21)."""
    expected = {0.055: 8.76, 0.86: 4.32, 1.00: 4.24, 3.51: 3.78}
    for LC, ref in expected.items():
        lo, hi = (6, 14) if LC < 0.1 else (2, 10)
        rs = rho_star_numeric(0.4, 0.8, 1.5, labor=(1, 1.21, LC), lo=lo, hi=hi)
        assert rs == pytest.approx(ref, abs=0.01)


def test_large_tariff_thresholds():
    """Referee 5.6 (cumulative definition): rho* falls with tariff size."""
    expected = {0.5: 3.19, 1.45: 2.70}
    for tau, ref in expected.items():
        rs = rho_star_numeric(0.4, 0.8, 1.5, tau0=tau, cumulative=True,
                              lo=1.5, hi=8.0)
        assert rs == pytest.approx(ref, abs=0.01)


def test_trade_war_increasing_in_rho():
    """Referee 4.3: joint depreciation vs C increasing in rho in the nest."""
    prev = -np.inf
    for rho in [1.5, 3.0, 6.0, 10.0]:
        p = make_params_nested(alpha_T=0.4, alpha_D=0.8, eta=1.5, rho=rho)
        eq = solve_3country_nested(p, trade_war(0.5))
        assert eq["log_e_AC"] > 0 and eq["log_e_AC"] > prev
        prev = eq["log_e_AC"]
    # spot value from the referee's table
    p = make_params_nested(alpha_T=0.4, alpha_D=0.8, eta=1.5, rho=6.0)
    eq = solve_3country_nested(p, trade_war(0.5))
    assert eq["log_e_AC"] == pytest.approx(0.2006, abs=5e-4)
