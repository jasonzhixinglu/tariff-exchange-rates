"""
Precompute equilibrium exchange rates over a 4^6 × 3 grid for the
interactive theory panel of the dashboard.

Grid axes:
  tau_AB, tau_BA, tau_AC, tau_CA, tau_BC, tau_CB  in [0, 0.25, 0.75, 1.5]  (4 pts)
  sigma                                            in [1, 2, 8]              (3 pts)
  Total: 4^6 * 3 = 12,288 points

Parameters held fixed (symmetric baseline):
  alpha_T_A = alpha_T_B = alpha_T_C = 0.25, alpha_N = 0.25
  labor_A = labor_B = labor_C = 1.0
  All productivities = 1.0, all producer prices = 1.0

Output: data/theory_grid.json
"""

import json
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np

# Allow running from repo root without installing the package
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tariff_exchange_rates import solve_3country
from tariff_exchange_rates.parameters import make_params_3country
from tariff_exchange_rates.tariffs import make_tariff_matrix

# ---------------------------------------------------------------------------
# Grid definition
# ---------------------------------------------------------------------------

TAU_VALS   = [0.0, 0.25, 0.75, 1.5]  # 4 points for each tariff rate
SIGMA_VALS = [1.0, 2.0,  8.0]    # Cobb-Douglas, moderate CES, high substitutability

TAU_KEYS = ["tau_AB", "tau_BA", "tau_AC", "tau_CA", "tau_BC", "tau_CB"]

# Symmetric baseline params (fixed throughout)
BASE_PARAMS_TEMPLATE = dict(
    alpha_T_A=0.25, alpha_T_B=0.25, alpha_T_C=0.25, alpha_N=0.25,
    labor=(1.0, 1.0, 1.0),
)

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run():
    out_path = ROOT / "data" / "theory_grid.json"
    out_path.parent.mkdir(exist_ok=True)

    grid_axes = {
        "tau_AB": TAU_VALS,
        "tau_BA": TAU_VALS,
        "tau_AC": TAU_VALS,
        "tau_CA": TAU_VALS,
        "tau_BC": TAU_VALS,
        "tau_CB": TAU_VALS,
        "sigma":  SIGMA_VALS,
    }

    combos = list(product(TAU_VALS, TAU_VALS, TAU_VALS, TAU_VALS, TAU_VALS, TAU_VALS, SIGMA_VALS))
    total  = len(combos)
    print(f"Computing {total} grid points …")

    records = []
    failures = 0
    t0 = time.time()

    for idx, (t_AB, t_BA, t_AC, t_CA, t_BC, t_CB, sigma) in enumerate(combos):
        params = make_params_3country(**BASE_PARAMS_TEMPLATE, sigma=sigma)
        tariffs = make_tariff_matrix(
            tau_AB=t_AB, tau_BA=t_BA,
            tau_AC=t_AC, tau_CA=t_CA,
            tau_BC=t_BC, tau_CB=t_CB,
        )

        try:
            eq = solve_3country(params, tariffs)
            record = {
                "tau_AB": t_AB, "tau_BA": t_BA,
                "tau_AC": t_AC, "tau_CA": t_CA,
                "tau_BC": t_BC, "tau_CB": t_CB,
                "sigma":  sigma,
                "e_AB":   round(eq["e_AB"], 8),
                "e_AC":   round(eq["e_AC"], 8),
                "e_BC":   round(eq["e_BC"], 8),
            }
        except Exception as exc:
            failures += 1
            record = {
                "tau_AB": t_AB, "tau_BA": t_BA,
                "tau_AC": t_AC, "tau_CA": t_CA,
                "tau_BC": t_BC, "tau_CB": t_CB,
                "sigma":  sigma,
                "e_AB":   None, "e_AC": None, "e_BC": None,
                "error":  str(exc),
            }

        records.append(record)

        if (idx + 1) % 200 == 0 or (idx + 1) == total:
            elapsed = time.time() - t0
            rate = (idx + 1) / elapsed
            eta  = (total - idx - 1) / rate
            print(f"  {idx+1:>4}/{total}  failures={failures}  {elapsed:.1f}s elapsed  ETA {eta:.1f}s")

    payload = {
        "meta": {
            "description": "Theory grid: symmetric 3-country model, 4^6 x 3 = 12288 parameter points",
            "axes": grid_axes,
            "fixed_params": {
                "alpha_T_A": 0.25, "alpha_T_B": 0.25, "alpha_T_C": 0.25, "alpha_N": 0.25,
                "labor_A": 1.0, "labor_B": 1.0, "labor_C": 1.0,
            },
            "n_points": total,
            "n_failures": failures,
        },
        "grid": records,
    }

    with open(out_path, "w") as f:
        json.dump(payload, f, separators=(",", ":"))

    size_kb = out_path.stat().st_size / 1024
    print(f"\nDone. {total - failures}/{total} succeeded. Written to {out_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    run()
