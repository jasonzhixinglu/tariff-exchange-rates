"""
Regression tests for the corrected nested CD-CES model.

Context: the pre-revision code computed tariff revenue with the fixed
preference weights alpha_T[j] instead of the realized (price-dependent)
CES expenditure shares, and scaled tradable demand by income instead of
alpha_T_total * income. The first error shifted equilibria whenever
sigma != 1 and produced a spurious sign reversal in log e_AC; the second
violated the budget constraint (harmless for equilibria, wrong for
levels). See REVISION_PLAN.md sections 3.1 and 5 (Phase 0).

Reference values labelled "referee" are from the referee's independent
replication of the nested CD-CES model (report dated 2026-08-22), which
we have verified against our own re-implementation.
"""

import numpy as np
import pytest

from tariff_exchange_rates.economy import compute_allocation
from tariff_exchange_rates.equilibrium import solve_2country, solve_3country


def symmetric_params(sigma, n=3):
    """Symmetric baseline: L_i = A_i = P_T_i = 1, alpha_T_j = alpha_N = 1/(n+1)."""
    share = 1.0 / (n + 1)
    return {
        "productivity_T": np.ones(n),
        "productivity_N": np.ones(n),
        "labor":          np.ones(n),
        "alpha_T":        np.full(n, share),
        "alpha_N":        share,
        "sigma":          sigma,
        "prices_T":       np.ones(n),
    }


def isolated_tariff(tau=1.0):
    T = np.zeros((3, 3))
    T[0, 1] = tau
    return T


# ---------------------------------------------------------------------------
# Internal consistency
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sigma", [0.5, 1.0, 2.0, 8.0])
def test_budget_constraint_holds(sigma):
    """Total spending (tradables + nontradables) equals disposable income."""
    params = symmetric_params(sigma)
    alloc = compute_allocation(params, [0.8, 0.95], isolated_tariff())
    spend = (alloc["consumer_prices"] * alloc["demand_T"]).sum(axis=1) \
        + alloc["prices_N"] * alloc["demand_N"]
    np.testing.assert_allclose(spend, alloc["income"], rtol=1e-12)


def test_ces_branch_continuous_with_cd_branch():
    """sigma -> 1 limit of the CES branch equals the Cobb-Douglas branch.

    The pre-fix code was discontinuous at sigma = 1 by a factor
    1/alpha_T_total (4/3 at the symmetric baseline).
    """
    params_cd = symmetric_params(1.0)
    params_eps = symmetric_params(1.0 + 1e-7)
    T = isolated_tariff()
    a_cd = compute_allocation(params_cd, [0.8, 0.95], T)
    a_eps = compute_allocation(params_eps, [0.8, 0.95], T)
    np.testing.assert_allclose(a_eps["demand_T"], a_cd["demand_T"], rtol=1e-5)
    np.testing.assert_allclose(a_eps["price_level"], a_cd["price_level"], rtol=1e-5)


def test_price_index_homogeneous_degree_one():
    """Scaling all producer prices scales the aggregate price level
    one-for-one: the (normalized-weight) CES tradable index is HD1.
    The pre-fix index used unnormalized weights alpha_T[j]^sigma, which
    made it diverge as sigma -> 1."""
    params = symmetric_params(2.0)
    T = np.zeros((3, 3))
    a1 = compute_allocation(params, [1.0, 1.0], T)
    params_scaled = dict(params, prices_T=2.0 * np.ones(3))
    a3 = compute_allocation(params_scaled, [1.0, 1.0], T)
    np.testing.assert_allclose(
        a3["price_level"] / a1["price_level"],
        2.0 * np.ones(3), rtol=1e-12,
    )


def test_walras_law_at_equilibrium():
    """TB_A = 0 follows from TB_B = TB_C = 0."""
    result = solve_3country(symmetric_params(4.0), isolated_tariff())
    assert abs(result["allocation"]["trade_balance"][0]) < 1e-9


# ---------------------------------------------------------------------------
# Equilibrium values: sigma = 1 unchanged, sigma != 1 corrected
# ---------------------------------------------------------------------------

def test_sigma1_equilibrium_unchanged_by_fix():
    """At sigma = 1 the old and corrected income formulas coincide, so the
    paper's reported CD equilibrium must be reproduced exactly."""
    result = solve_3country(symmetric_params(1.0), isolated_tariff())
    assert result["log_e_AB"] == pytest.approx(-0.2719, abs=5e-5)
    assert result["log_e_AC"] == pytest.approx(-0.0488, abs=5e-5)


# (sigma, log e_AB, log e_AC) from the referee's nested-model replication.
REFEREE_REPLICATION = [
    (0.5, -0.3587, -0.1133),
    (1.0, -0.2719, -0.0488),
    (2.0, -0.2110, -0.0163),
    (5.0, -0.1286, -0.0013),
]


@pytest.mark.parametrize("sigma,ref_ab,ref_ac", REFEREE_REPLICATION)
def test_matches_referee_replication(sigma, ref_ab, ref_ac):
    """Corrected model reproduces the referee's independent replication of
    the nested CD-CES structure (isolated tariff tau_AB = 1)."""
    result = solve_3country(symmetric_params(sigma), isolated_tariff())
    assert result["log_e_AB"] == pytest.approx(ref_ab, abs=5e-5)
    assert result["log_e_AC"] == pytest.approx(ref_ac, abs=5e-5)


def test_no_sign_reversal_in_flat_ces():
    """Proposition 1 (numerical footing): in the single-elasticity model at
    the symmetric baseline, log e_AC < 0 for all sigma — it asymptotes to
    zero from below and never crosses. The pre-fix code crossed at
    sigma ~ 1.9, which was an artifact of the income-formula bug."""
    for sigma in [0.3, 0.5, 1.0, 1.9, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 50.0]:
        result = solve_3country(symmetric_params(sigma), isolated_tariff())
        assert result["log_e_AC"] <= 1e-8, (
            f"sign reversal at sigma={sigma}: log e_AC={result['log_e_AC']}"
        )


def test_flat_ces_local_slope_matches_analytic():
    """At the paper's symmetric calibration (alpha_D = 1/3, alpha_T = 3/4),
    the analytic local response is d log e_AC / d tau |_{tau=0} = -1/(12 sigma)
    (referee report section 5.3). Finite-difference check."""
    h = 1e-6
    for sigma in [0.5, 1.0, 2.0, 5.0]:
        base = solve_3country(symmetric_params(sigma), np.zeros((3, 3)))
        pert = solve_3country(symmetric_params(sigma), isolated_tariff(h))
        slope = (pert["log_e_AC"] - base["log_e_AC"]) / h
        assert slope == pytest.approx(-1.0 / (12.0 * sigma), rel=1e-3)


# ---------------------------------------------------------------------------
# Two-country benchmark
# ---------------------------------------------------------------------------

def test_two_country_closed_form():
    """Eq. (17) of the paper: e(tau) = 1/(1+tau) * 1/(1 - alpha_TB*tau/(1+tau))
    at the symmetric CD calibration (alpha_T_i = alpha_N = 1/3)."""
    params = {
        "productivity_T": np.ones(2), "productivity_N": np.ones(2),
        "labor": np.ones(2), "alpha_T": np.array([1/3, 1/3]),
        "alpha_N": 1/3, "sigma": 1.0, "prices_T": np.ones(2),
    }
    for tau in [0.0, 0.2, 0.5, 1.0, 1.45]:
        result = solve_2country(params, tau)
        closed = (1.0 / (1.0 + tau)) / (1.0 - (1/3) * tau / (1.0 + tau))
        assert result["e_AB"] == pytest.approx(closed, rel=1e-10)
