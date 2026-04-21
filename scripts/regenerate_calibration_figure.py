"""
Regenerate calibration_results.pdf directly from the current model code
and save it to Exchange_Rate_Tariffs/ where the paper picks it up.
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tariff_exchange_rates import CALIBRATIONS, TARIFF_REGIMES, solve_3country, free_trade

# ---------------------------------------------------------------------------
# Realized exchange rate data (log-point changes x100 vs 2024 annual average)
# Source: paper Table 3; Regime 1 = March 2025, Regime 2 = April 2025
# Convention: positive = depreciation of first-named currency
# ---------------------------------------------------------------------------
REALIZED = {
    "EU":  {"R1": (-0.74, -0.05,  0.69), "R2": (-1.39,  3.75,  5.15)},
    "VNM": {"R1": (-0.74,  2.11,  2.85), "R2": (-1.39,  3.38,  4.77)},
    "ROW": {"R1": (-0.74, -1.05, -0.31), "R2": (-1.39,  2.18,  3.57)},
}

CFG_SHORT   = {"US\u2013China\u2013EU": "EU", "US\u2013China\u2013VNM": "VNM", "US\u2013China\u2013ROW": "ROW"}
REGIME_KEYS = {"Regime 1 (Fentanyl)": "R1", "Regime 2 (Peak trade war)": "R2"}
ER_LABELS   = [r"$\Delta e_{AB}$", r"$\Delta e_{AC}$", r"$\Delta e_{BC}$"]

# ---------------------------------------------------------------------------
# Solve equilibria
# ---------------------------------------------------------------------------
rows = []
for cfg_name, params in CALIBRATIONS.items():
    short = CFG_SHORT[cfg_name]
    eq_ft = solve_3country(params, free_trade())
    for regime_name, T in TARIFF_REGIMES.items():
        rkey = REGIME_KEYS[regime_name]
        eq   = solve_3country(params, T)
        m_ab = 100 * (eq["e_AB"] / eq_ft["e_AB"] - 1)
        m_ac = 100 * (eq["e_AC"] / eq_ft["e_AC"] - 1)
        m_bc = 100 * (eq["e_BC"] / eq_ft["e_BC"] - 1)
        d_ab, d_ac, d_bc = REALIZED[short][rkey]
        rows.append(dict(cfg=cfg_name, short=short, regime=rkey,
                         m_AB=m_ab, m_AC=m_ac, m_BC=m_bc,
                         d_AB=d_ab, d_AC=d_ac, d_BC=d_bc))

# ---------------------------------------------------------------------------
# Figure: both regimes, side by side per configuration
# ---------------------------------------------------------------------------
CFG_ORDER    = ["US\u2013China\u2013EU", "US\u2013China\u2013VNM", "US\u2013China\u2013ROW"]
CFG_LABELS   = ["US\u2013China\u2013EU  (\u03c3=8)", "US\u2013China\u2013VNM  (\u03c3=8)", "US\u2013China\u2013ROW  (\u03c3=2)"]
REGIME_ORDER = ["R1", "R2"]
REGIME_TITLES = {"R1": "Regime 1 \u2014 Fentanyl tariffs", "R2": "Regime 2 \u2014 Peak escalation"}

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})

fig, axes = plt.subplots(2, 3, figsize=(11, 6.5), sharey=False)
fig.subplots_adjust(hspace=0.45, wspace=0.35)

MODEL_COLOR = "#2166ac"
DATA_COLOR  = "#d6604d"
x = np.arange(3)
w = 0.33

for col, (cfg_name, cfg_label) in enumerate(zip(CFG_ORDER, CFG_LABELS)):
    for row_idx, rkey in enumerate(REGIME_ORDER):
        ax = axes[row_idx][col]
        rec = next(r for r in rows if r["cfg"] == cfg_name and r["regime"] == rkey)

        model_vals = [rec["m_AB"], rec["m_AC"], rec["m_BC"]]
        data_vals  = [rec["d_AB"], rec["d_AC"], rec["d_BC"]]

        bars_m = ax.bar(x - w/2, model_vals, w, color=MODEL_COLOR, alpha=0.85, label="Model")
        bars_d = ax.bar(x + w/2, data_vals,  w, color=DATA_COLOR,  alpha=0.85, label="Data")
        ax.axhline(0, color="black", lw=0.6, ls="--", zorder=0)

        # Value labels on bars
        all_vals = model_vals + data_vals
        y_range  = max(abs(v) for v in all_vals if v is not None) or 1
        pad      = y_range * 0.06

        def _label_bars(bars, vals):
            for bar, val in zip(bars, vals):
                if val is None:
                    continue
                xc = bar.get_x() + bar.get_width() / 2
                sign = "+" if val >= 0 else ""
                if val >= 0:
                    ax.text(xc, val + pad, f"{sign}{val:.1f}",
                            ha="center", va="bottom", fontsize=7.5,
                            color="black", fontweight="medium")
                else:
                    ax.text(xc, val - pad, f"{val:.1f}",
                            ha="center", va="top", fontsize=7.5,
                            color="black", fontweight="medium")

        _label_bars(bars_m, model_vals)
        _label_bars(bars_d, data_vals)

        # Extra vertical room for labels
        lo, hi = ax.get_ylim()
        ax.set_ylim(lo - y_range * 0.15, hi + y_range * 0.15)

        ax.set_xticks(x)
        ax.set_xticklabels(ER_LABELS, fontsize=8.5)
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f"))
        ax.tick_params(axis="y", labelsize=8)

        if col == 0:
            ax.set_ylabel(REGIME_TITLES[rkey] + "\n% change", fontsize=8.5, labelpad=4)
        if row_idx == 0:
            ax.set_title(cfg_label, fontsize=9, fontweight="bold", pad=6)

# Legend
handles, lbls = axes[0][0].get_legend_handles_labels()
fig.legend(handles, lbls, loc="lower center", ncol=2, fontsize=9,
           frameon=False, bbox_to_anchor=(0.5, -0.02))

fig.suptitle(
    "Model-implied vs. realized exchange rate changes by configuration and regime\n"
    r"Positive values $=$ depreciation of first-named currency",
    fontsize=9.5, y=1.01,
)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
import shutil

# Always save to output/ first
out_copy = ROOT / "output" / "calibration_results.pdf"
out_copy.parent.mkdir(exist_ok=True)
fig.savefig(out_copy, bbox_inches="tight")
print(f"Saved: {out_copy}")

# Copy to paper directory (will fail gracefully if file is locked)
out_path = ROOT / "Exchange_Rate_Tariffs" / "calibration_results.pdf"
try:
    shutil.copy2(out_copy, out_path)
    print(f"Copied to: {out_path}")
except PermissionError:
    print(f"NOTE: Could not write {out_path} — close the PDF in your viewer, then run:")
    print(f"  copy \"{out_copy}\" \"{out_path}\"")
