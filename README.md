# Trade Tariffs and Exchange Rates

Replication code for *Trade Tariffs and Exchange Rates: Revisiting Conventional Wisdom in a Three-Country Framework* (Lu & Milkov 2026).

## Overview

The paper develops a three-country, two-sector, one-factor general equilibrium model to study how tariffs affect bilateral exchange rates. The key result is that a bilateral trade war — unlike a unilateral tariff — unambiguously depreciates the dollar against uninvolved third-country currencies, reversing the conventional two-country appreciation result.

## Structure

```
src/tariff_exchange_rates/   # Core package
    economy.py               # Allocation and price-index functions
    equilibrium.py           # Solvers: solve_2country, solve_3country
    tariffs.py               # Tariff matrix constructors
    parameters.py            # Calibrated configurations (CALIBRATIONS, TARIFF_REGIMES)
    plotting.py              # Figure helpers

notebooks/
    section3_two_country_model.ipynb    # Two-country benchmark
    section4_three_country_model.ipynb  # Three-country results and figures
    section5_calibration.ipynb          # Calibration and model-data comparison

Exchange_Rate_Tariffs/       # LaTeX paper source
```

## Calibration (Section 5)

Three configurations vary the identity of the third country *C*. Parameters are calibrated as follows:

| Parameter | Source |
|---|---|
| Expenditure shares $\alpha_{T_j}$ | 2024 world goods export shares (WTO), tradable budget fixed at 0.40 |
| Labor endowments $L_i$ | 2024 PPP GDP (IMF WEO), normalised to $L_A = 1$ (US) |
| $\sigma$ (EU, VNM) | 8 — consistent with Broda & Weinstein (2006) manufactured-goods estimates; motivated by the China Shock 2.0 narrative for EU and by Vietnam's role as a China re-export hub |
| $\sigma$ (ROW) | 2 — aggregate rest-of-world, low substitutability by construction |

Two tariff regimes:

| Regime | $\tau_{AB}$ | $\tau_{BA}$ | $\tau_{AC}$ | Data reference |
|---|---|---|---|---|
| 1 — Fentanyl | 20% | 0% | 0% | March 2025 |
| 2 — Peak escalation | 145% | 125% | 10% | April 2025 |

## Installation

```bash
pip install -e .
```

## Usage

```python
from tariff_exchange_rates import (
    CALIBRATIONS, TARIFF_REGIMES,
    solve_3country, free_trade,
)

params = CALIBRATIONS["US–China–EU"]
eq_ft  = solve_3country(params, free_trade())
eq_r2  = solve_3country(params, TARIFF_REGIMES["Regime 2 (Peak trade war)"])

e_AC_pct = 100 * (eq_r2["e_AC"] / eq_ft["e_AC"] - 1)
print(f"USD/EUR change under peak trade war: {e_AC_pct:+.2f}%")
```
