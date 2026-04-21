"""
Parameter builders and calibrated configurations.

All model parameters are stored as plain dicts with numpy array values.
The two builders enforce budget balance (shares must sum to 1) and set
sensible defaults (unit productivities and endowments, normalized prices).

Calibrated configurations (CALIBRATIONS, TARIFF_REGIMES) reproduce the
benchmark results from the 3c2s1f_CES_model_claude_2025_calibration notebook.
"""

import numpy as np
from .tariffs import make_tariff_matrix


def make_params_2country(
    alpha_T_A=1.0 / 3.0,
    alpha_T_B=1.0 / 3.0,
    alpha_N=1.0 / 3.0,
    productivity_T=(1.0, 1.0),
    productivity_N=(1.0, 1.0),
    labor=(1.0, 1.0),
    prices_T=(1.0, 1.0),
    sigma=1.0,
):
    """
    Build a parameter dict for the 2-country model.

    alpha_T_A + alpha_T_B + alpha_N must equal 1.

    Countries: 0 = A, 1 = B.
    """
    total = alpha_T_A + alpha_T_B + alpha_N
    assert abs(total - 1.0) < 1e-10, f"Expenditure shares must sum to 1, got {total:.6f}"

    return {
        "productivity_T": np.array(productivity_T, dtype=float),
        "productivity_N": np.array(productivity_N, dtype=float),
        "labor":          np.array(labor,          dtype=float),
        "alpha_T":        np.array([alpha_T_A, alpha_T_B], dtype=float),
        "alpha_N":        float(alpha_N),
        "sigma":          float(sigma),
        "prices_T":       np.array(prices_T, dtype=float),
    }


def make_params_3country(
    alpha_T_A=0.25,
    alpha_T_B=0.25,
    alpha_T_C=0.25,
    alpha_N=0.25,
    productivity_T=(1.0, 1.0, 1.0),
    productivity_N=(1.0, 1.0, 1.0),
    labor=(1.0, 1.0, 1.0),
    prices_T=(1.0, 1.0, 1.0),
    sigma=1.0,
):
    """
    Build a parameter dict for the 3-country model.

    alpha_T_A + alpha_T_B + alpha_T_C + alpha_N must equal 1.

    Countries: 0 = A, 1 = B, 2 = C.
    """
    total = alpha_T_A + alpha_T_B + alpha_T_C + alpha_N
    assert abs(total - 1.0) < 1e-10, f"Expenditure shares must sum to 1, got {total:.6f}"

    return {
        "productivity_T": np.array(productivity_T, dtype=float),
        "productivity_N": np.array(productivity_N, dtype=float),
        "labor":          np.array(labor,          dtype=float),
        "alpha_T":        np.array([alpha_T_A, alpha_T_B, alpha_T_C], dtype=float),
        "alpha_N":        float(alpha_N),
        "sigma":          float(sigma),
        "prices_T":       np.array(prices_T, dtype=float),
    }


# =============================================================================
# Calibrated configurations (Lu & Milkov 2026)
#
# Countries: 0 = US (A), 1 = China (B), 2 = third country (C)
# alpha_T_x  — expenditure weight on each country's tradable variety
# alpha_N    — expenditure weight on nontradables (= 0.60 across configs)
# labor      — relative labor endowments (US normalized to 1)
# sigma      — CES elasticity within the tradable bundle
# =============================================================================

CALIBRATIONS = {
    "US–China–EU": make_params_3country(
        alpha_T_A=0.097, alpha_T_B=0.165, alpha_T_C=0.138, alpha_N=0.600,
        labor=(1.0, 1.21, 0.86),
        sigma=6.0,
    ),
    "US–China–VNM": make_params_3country(
        alpha_T_A=0.138, alpha_T_B=0.236, alpha_T_C=0.026, alpha_N=0.600,
        labor=(1.0, 1.21, 0.055),
        sigma=8.0,
    ),
    "US–China–ROW": make_params_3country(
        alpha_T_A=0.034, alpha_T_B=0.057, alpha_T_C=0.309, alpha_N=0.600,
        labor=(1.0, 1.21, 3.51),
        sigma=2.0,
    ),
}

# Tariff regimes covering 2025 US–China trade escalation
# tau_AB = US tariff on Chinese goods, tau_BA = Chinese tariff on US goods
# tau_AC = US tariff on third-country goods
TARIFF_REGIMES = {
    "Regime 1 (Fentanyl)":       make_tariff_matrix(tau_AB=0.20),
    "Regime 2 (Peak trade war)": make_tariff_matrix(tau_AB=1.45, tau_BA=1.25, tau_AC=0.10),
}
