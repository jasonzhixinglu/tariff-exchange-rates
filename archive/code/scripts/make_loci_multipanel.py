"""
Compress the six Section-3 locus figures into one 2x3 multi-panel figure
(referee item: 'compress Figures 2-7 into one multi-panel figure plus a
threshold plot').

Panels (symmetric baseline, alpha_Tj = alpha_N = 1/4):
 (a) free trade                          (d) isolated tariff, sigma = 0.5
 (b) uniform tariff tau = 1 (sigma = 1)  (e) isolated tariff, sigma = 2
 (c) isolated tariff tau = 1 (sigma = 1) (f) trade war (sigma = 1),
                                             in (e_AC, e_BC) space

Output: output/loci_multipanel.pdf (+png), copied to Exchange_Rate_Tariffs/.
"""

import shutil
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tariff_exchange_rates import (  # noqa: E402
    free_trade, isolated_tariff, make_params_3country, solve_3country,
    trade_war, uniform_tariff,
)
from tariff_exchange_rates.plotting import _compute_tb_grid  # noqa: E402

C_B, C_C = "#c23b22", "#2166ac"


def params(sigma):
    return make_params_3country(alpha_T_A=0.25, alpha_T_B=0.25,
                                alpha_T_C=0.25, alpha_N=0.25, sigma=sigma)


def draw(ax, p, scenarios, coords="AB_AC", rng=(-0.7, 0.7), n=60):
    """Draw TB_B=0 / TB_C=0 (or TB_A/TB_B for the war panel) loci and
    equilibria for {label: (tariffs, linestyle)}."""
    v = np.linspace(*rng, n)
    for label, (T, ls) in scenarios.items():
        grids = _compute_tb_grid(p, T, v, v)
        if coords == "AB_AC":
            gx, gy = grids["log_EAB"], grids["log_EAC"]
            zi, zj = grids["TB_B"], grids["TB_C"]
        else:                                    # war panel: (e_AC, e_BC)
            gx = grids["log_EAC"]
            gy = grids["log_EAC"] - grids["log_EAB"]   # log e_BC
            zi, zj = grids["TB_A"], grids["TB_B"]
        ax.contour(gx, gy, zi, levels=[0], colors=C_B,
                   linestyles=ls, linewidths=1.6)
        ax.contour(gx, gy, zj, levels=[0], colors=C_C,
                   linestyles=ls, linewidths=1.6)
        eq = solve_3country(p, T)
        if coords == "AB_AC":
            ax.plot(eq["log_e_AB"], eq["log_e_AC"], "o", color="black", ms=5)
        else:
            ax.plot(eq["log_e_AC"], eq["log_e_BC"], "o", color="black", ms=5)
    ax.axhline(0, color="gray", lw=0.5)
    ax.axvline(0, color="gray", lw=0.5)
    ax.set_xlim(rng); ax.set_ylim(rng)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=8)


def main():
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    ft = free_trade()

    specs = [
        (axes[0, 0], params(1.0), {"free trade": (ft, "solid")},
         "AB_AC", "(a) free trade ($\\sigma=1$)"),
        (axes[0, 1], params(1.0), {"free trade": (ft, "solid"),
                                   "uniform": (uniform_tariff(1.0), "dashed")},
         "AB_AC", "(b) uniform tariff $\\tau=1$"),
        (axes[0, 2], params(1.0), {"free trade": (ft, "solid"),
                                   "isolated": (isolated_tariff(1.0), "dashed")},
         "AB_AC", "(c) isolated tariff $\\tau_{AB}=1$ ($\\sigma=1$)"),
        (axes[1, 0], params(0.5), {"free trade": (ft, "solid"),
                                   "isolated": (isolated_tariff(1.0), "dashed")},
         "AB_AC", "(d) isolated tariff ($\\sigma=0.5$)"),
        (axes[1, 1], params(2.0), {"free trade": (ft, "solid"),
                                   "isolated": (isolated_tariff(1.0), "dashed")},
         "AB_AC", "(e) isolated tariff ($\\sigma=2$)"),
        (axes[1, 2], params(1.0), {"free trade": (ft, "solid"),
                                   "war": (trade_war(1.0), "dashed")},
         "AC_BC", "(f) trade war $\\tau_{AB}=\\tau_{BA}=1$"),
    ]
    for ax, p, sc, coords, title in specs:
        draw(ax, p, sc, coords)
        ax.set_title(title, fontsize=10)
        if coords == "AB_AC":
            ax.set_xlabel(r"$\log e_{AB}$", fontsize=9)
            ax.set_ylabel(r"$\log e_{AC}$", fontsize=9)
        else:
            ax.set_xlabel(r"$\log e_{AC}$", fontsize=9)
            ax.set_ylabel(r"$\log e_{BC}$", fontsize=9)

    # one shared legend
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=C_B, lw=1.6, label=r"$TB$ locus (red pair: $B$; panel f: $A$)"),
               Line2D([], [], color=C_C, lw=1.6, label=r"$TB$ locus (blue pair: $C$; panel f: $B$)"),
               Line2D([], [], color="gray", lw=1.6, ls="solid", label="free trade"),
               Line2D([], [], color="gray", lw=1.6, ls="dashed", label="with tariff"),
               Line2D([], [], color="black", marker="o", lw=0, label="equilibrium")]
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=9,
               frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.03, 1, 1))

    out = ROOT / "output" / "loci_multipanel.pdf"
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=100, bbox_inches="tight")
    shutil.copy2(out, ROOT / "Exchange_Rate_Tariffs" / out.name)
    print(f"Saved: {out} (+png, + paper copy)")


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
