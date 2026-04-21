"""
Precompute equilibrium exchange rates for the pre-calibrated country panel.

For each of 8 third-country (C) configurations, we solve the model under
Regime 1 (fentanyl tariffs) and Regime 2 (peak escalation). Parameters are
fixed from standard data sources; sigma is set once per country based on
the nature of the bilateral trade relationship and is not a free parameter.

Countries A = US, B = China throughout.

Third-country candidates:
  EU, Japan, South Korea, Mexico, Canada, Vietnam, Taiwan, India

Data sources
------------
  Labor endowments  : IMF World Economic Outlook, October 2024 (PPP GDP, 2024)
  Expenditure shares: WTO Merchandise Trade Statistics, 2024 goods export shares
  Tariff rates      : USTR executive orders / Federal Register notices (2025)
  Sigma             : Broda & Weinstein (2006) for manufactured goods (sigma=8);
                      Feenstra et al. (2018) for aggregate/mixed blocs (sigma=2–4)

Output: data/calibration_panel.json
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tariff_exchange_rates import solve_3country
from tariff_exchange_rates.parameters import make_params_3country
from tariff_exchange_rates.tariffs import make_tariff_matrix, free_trade

# ---------------------------------------------------------------------------
# Country-C configurations
# ---------------------------------------------------------------------------
# GDP PPP 2024 (trillion international dollars, IMF WEO Oct 2024)
#   US: 29.2,  China: 35.3
#   EU: 25.1,  Japan: 6.6,   Korea: 3.0,   Mexico: 3.3,
#   Canada: 2.5, Vietnam: 1.6, Taiwan: 1.7,  India: 14.5
#
# World goods export shares 2024 (WTO):
#   US: 8.4%,  China: 14.3%
#   EU: 12.0%, Japan: 3.3%,  Korea: 2.7%,  Mexico: 2.8%,
#   Canada: 2.4%, Vietnam: 1.6%, Taiwan: 2.2%, India: 1.9%
#
# alpha_T_j = 0.40 * s_j / (s_A + s_B + s_C)   [nontradable share fixed at 0.60]
# L_C = PPP_GDP_C / PPP_GDP_US  (normalized to L_A = 1)
#
# Sigma choices:
#   8  — manufactured goods heavily integrated with Chinese supply chains
#        (Broda & Weinstein 2006 disaggregated estimates)
#   5  — significant but partial overlap (electronics, autos)
#   3  — moderate overlap; aggregate estimates apply
#   2  — commodity-heavy or heterogeneous bloc; Feenstra et al. 2018

S_A = 0.084   # US world goods export share
S_B = 0.143   # China world goods export share
L_A = 1.0
L_B = 1.21    # China PPP GDP / US PPP GDP = 35.3 / 29.2

def make_alpha(s_C):
    """Compute tradable expenditure shares given third-country export share.
    alpha_T_C is derived residually so shares sum exactly to 1."""
    denom = S_A + S_B + s_C
    a_A = 0.40 * S_A / denom
    a_B = 0.40 * S_B / denom
    a_C = 0.40 - a_A - a_B   # exact residual — no rounding
    return {"alpha_T_A": a_A, "alpha_T_B": a_B, "alpha_T_C": a_C, "alpha_N": 0.60}

COUNTRY_CONFIGS = {
    "EU": {
        "label": "European Union",
        "currency": "EUR",
        "s_C": 0.120,
        "L_C": 25.1 / 29.2,    # 0.860
        "sigma": 6,
        "sigma_note": "Moderate-to-high manufacturing competition; China Shock 2.0 narrative. "
                      "Intermediate between Vietnam/Korea and ROW given EU's product differentiation.",
        "flag": "🇪🇺",
    },
    "JPN": {
        "label": "Japan",
        "currency": "JPY",
        "s_C": 0.033,
        "L_C": 6.6 / 29.2,     # 0.226
        "sigma": 4,
        "sigma_note": "Advanced manufactures (autos, machinery) with limited overlap "
                      "with Chinese exports; Feenstra et al. 2018 aggregate estimate.",
        "flag": "🇯🇵",
    },
    "KOR": {
        "label": "South Korea",
        "currency": "KRW",
        "s_C": 0.027,
        "L_C": 3.0 / 29.2,     # 0.103
        "sigma": 5,
        "sigma_note": "Electronics and semiconductors create meaningful overlap with "
                      "Chinese exports; between disaggregated and aggregate estimates.",
        "flag": "🇰🇷",
    },
    "MEX": {
        "label": "Mexico",
        "currency": "MXN",
        "s_C": 0.028,
        "L_C": 3.3 / 29.2,     # 0.113
        "sigma": 5,
        "sigma_note": "Nearshoring beneficiary; manufacturing overlap with China in "
                      "autos and electronics. USMCA integration complicates but "
                      "product-level substitutability is meaningful.",
        "flag": "🇲🇽",
    },
    "CAN": {
        "label": "Canada",
        "currency": "CAD",
        "s_C": 0.024,
        "L_C": 2.5 / 29.2,     # 0.086
        "sigma": 2,
        "sigma_note": "Commodity-heavy export basket (energy, mining, agriculture) "
                      "with low substitutability for Chinese manufactures; "
                      "Feenstra et al. 2018 aggregate lower bound.",
        "flag": "🇨🇦",
    },
    "VNM": {
        "label": "Vietnam",
        "currency": "VND",
        "s_C": 0.016,
        "L_C": 1.6 / 29.2,     # 0.055
        "sigma": 8,
        "sigma_note": "Assembly and re-export hub deeply integrated in Chinese supply "
                      "chains; Vietnamese and Chinese exports to the US are close "
                      "substitutes at the product level (Broda & Weinstein 2006).",
        "flag": "🇻🇳",
    },
    "TWN": {
        "label": "Taiwan",
        "currency": "TWD",
        "s_C": 0.022,
        "L_C": 1.7 / 29.2,     # 0.058
        "sigma": 3,
        "sigma_note": "Semiconductor dominance means Taiwanese exports are largely "
                      "non-substitutable with Chinese goods at the aggregate level; "
                      "low sigma despite product-level integration in other categories.",
        "flag": "🇹🇼",
    },
    "IND": {
        "label": "India",
        "currency": "INR",
        "s_C": 0.019,
        "L_C": 14.5 / 29.2,    # 0.497
        "sigma": 3,
        "sigma_note": "Emerging manufacturing base with growing but currently limited "
                      "overlap with Chinese export categories; aggregate estimate "
                      "appropriate given product heterogeneity (Feenstra et al. 2018).",
        "flag": "🇮🇳",
    },
}

# ---------------------------------------------------------------------------
# Tariff regimes (incremental above pre-2025 baseline = free trade)
# ---------------------------------------------------------------------------
# Regime 1: Feb–Mar 2025 fentanyl-related tariffs on China only
#   tau_AB = 0.20 (US on China), tau_BA = 0 (no retaliation yet), tau_AC = 0
#
# Regime 2: Post-Liberation Day peak escalation (April 2025)
#   tau_AB = 1.45 (US on China: 34% LD reciprocal + 20% fentanyl + 91% escalation)
#   tau_BA = 1.25 (China on US: cumulative retaliation)
#   tau_AC = 0.10 (universal 10% baseline left in place after April 9 pause)
#   tau_CA = 0    (no C retaliation on US during this window)

REGIMES = {
    "regime1": {
        "label": "Regime 1 — Fentanyl tariffs (Feb–Mar 2025)",
        "tariff_kwargs": {"tau_AB": 0.20},
    },
    "regime2": {
        "label": "Regime 2 — Peak escalation (April 2025)",
        "tariff_kwargs": {"tau_AB": 1.45, "tau_BA": 1.25, "tau_AC": 0.10},
    },
}

# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

def solve_one(country_key, regime_key):
    cfg    = COUNTRY_CONFIGS[country_key]
    regime = REGIMES[regime_key]

    alpha  = make_alpha(cfg["s_C"])
    params = make_params_3country(
        **alpha,
        labor=(L_A, L_B, cfg["L_C"]),
        sigma=cfg["sigma"],
    )

    # Free-trade baseline
    eq_ft = solve_3country(params, free_trade())

    # Tariff equilibrium
    tariffs = make_tariff_matrix(**regime["tariff_kwargs"])
    eq      = solve_3country(params, tariffs, init=[eq_ft["log_e_AB"], eq_ft["log_e_AC"]])

    # Percent changes relative to free trade (positive = depreciation of first currency)
    pct = lambda new, base: round(100.0 * (new / base - 1.0), 4)

    return {
        "e_AB_ft":  round(eq_ft["e_AB"], 8),
        "e_AC_ft":  round(eq_ft["e_AC"], 8),
        "e_BC_ft":  round(eq_ft["e_BC"], 8),
        "e_AB":     round(eq["e_AB"], 8),
        "e_AC":     round(eq["e_AC"], 8),
        "e_BC":     round(eq["e_BC"], 8),
        "delta_e_AB": pct(eq["e_AB"], eq_ft["e_AB"]),
        "delta_e_AC": pct(eq["e_AC"], eq_ft["e_AC"]),
        "delta_e_BC": pct(eq["e_BC"], eq_ft["e_BC"]),
    }


def run():
    out_path = ROOT / "data" / "calibration_panel.json"
    out_path.parent.mkdir(exist_ok=True)

    results = {}
    for ckey, cfg in COUNTRY_CONFIGS.items():
        results[ckey] = {
            "meta": {
                "label":      cfg["label"],
                "currency":   cfg["currency"],
                "flag":       cfg["flag"],
                "sigma":      cfg["sigma"],
                "sigma_note": cfg["sigma_note"],
                "alpha_T_A":  round(make_alpha(cfg["s_C"])["alpha_T_A"], 4),
                "alpha_T_B":  round(make_alpha(cfg["s_C"])["alpha_T_B"], 4),
                "alpha_T_C":  round(make_alpha(cfg["s_C"])["alpha_T_C"], 4),
                "alpha_N":    0.60,
                "L_C":        round(cfg["L_C"], 4),
                "s_C":        cfg["s_C"],
            },
            "regimes": {},
        }
        for rkey, regime in REGIMES.items():
            print(f"  Solving {ckey} / {rkey} … ", end="", flush=True)
            try:
                res = solve_one(ckey, rkey)
                results[ckey]["regimes"][rkey] = {**regime, **res, "error": None}
            except Exception as exc:
                res = None
                results[ckey]["regimes"][rkey] = {**regime, "error": str(exc)}
            if res is not None:
                print(f"delta_e_AC = {res['delta_e_AC']:+.2f}%")
            else:
                print(f"FAILED: {results[ckey]['regimes'][rkey]['error']}")

    payload = {
        "meta": {
            "description": "Pre-calibrated panel: US (A) vs China (B) vs 8 third countries (C)",
            "countries_A_B": {"A": "US", "B": "China"},
            "data_sources": {
                "labor":   "IMF WEO October 2024 (PPP GDP, normalized to US = 1)",
                "shares":  "WTO Merchandise Trade Statistics 2024 (world goods export shares)",
                "tariffs": "USTR executive orders and Federal Register notices (2025)",
                "sigma":   "Broda & Weinstein (2006) and Feenstra et al. (2018)",
            },
            "convention": "delta_e_XY > 0 means depreciation of X's currency against Y",
        },
        "countries": results,
    }

    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"\nWritten to {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    run()
