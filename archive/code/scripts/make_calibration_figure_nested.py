"""
Section 4 results figure for the rebuilt (nested, import-share) calibration.

Three panels (EU, Vietnam-adjusted, ROW). Each: model Regime-2 changes in
e_AB (USD/RMB, dashed) and e_AC (USD/C, solid) as functions of the
cross-origin elasticity rho, with observed values at the April 2025 window
and the extended December 2025 window drawn as horizontal lines. The
empirically supported rho range (~2-4, FLOR / Broda-Weinstein /
Li et al. ratio) is shaded.

Inputs: data/calibration_nested.json, data/fx_data.json.
Output: output/calibration_nested_results.pdf (+ png preview), copied to
Exchange_Rate_Tariffs/.
"""

import json
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

CFGS = [("EU", "US–China–EU", "EU"), ("VNM_adj", "US–China–Vietnam (adj.)", "VNM"),
        ("ROW", "US–China–ROW (matched index)", "ROW")]

C_AB, C_AC = "#c23b22", "#2166ac"


def main():
    cal = json.load(open(ROOT / "data" / "calibration_nested.json"))
    fx = json.load(open(ROOT / "data" / "fx_data.json"))["rates"]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharex=True)
    for ax, (key, title, fxkey) in zip(axes, CFGS):
        cfg = cal["configs"][key]
        keys = sorted(cfg["rho_results"], key=float); rhos = [float(k) for k in keys]
        ab = [cfg["rho_results"][k]["regime2"]["de_AB"] for k in keys]
        ac = [cfg["rho_results"][k]["regime2"]["de_AC"] for k in keys]

        ax.axvspan(2.0, 4.0, color="#c8e0c8", alpha=0.45, zorder=0)
        ax.plot(rhos, ab, color=C_AB, ls="--", lw=2,
                label=r"model $\Delta e_{AB}$ (USD/RMB)")
        ax.plot(rhos, ac, color=C_AC, lw=2,
                label=r"model $\Delta e_{AC}$ (USD/$C$)")

        # April data only: each window is compared to its own tariff regime,
        # and this figure is the April window vs the Regime-2 rates.
        d = fx[fxkey]["pct_changes"]
        drmb = fx["RMB"]["pct_changes"]
        if d.get("regime2") is not None:
            ax.axhline(d["regime2"], color=C_AC, ls=":", lw=1.4)
        if drmb.get("regime2") is not None:
            ax.axhline(drmb["regime2"], color=C_AB, ls=":", lw=1.4)
        if key == "EU":
            ax.annotate("data Apr-25 (USD/EUR)", xy=(5.2, d["regime2"] + 0.5),
                        color=C_AC, fontsize=8)
            ax.annotate("data Apr-25 (USD/RMB)", xy=(5.2, drmb["regime2"] - 1.3),
                        color=C_AB, fontsize=8)

        rs = cfg["rho_star"]["cum_tau145"]
        if rs:
            ax.axvline(rs, color="gray", ls=":", lw=1.1)
            ax.annotate(rf"$\rho^*_{{\tau=1.45}}={rs:.2f}$",
                        xy=(rs + 0.1, ax.get_ylim()[0]), fontsize=8,
                        color="gray", rotation=90, va="bottom")
        ax.axhline(0, color="gray", lw=0.7)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(r"cross-origin elasticity $\rho$", fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)

    axes[0].set_ylabel("Regime 2: % change vs free trade\n(positive = USD depreciation)",
                       fontsize=10)
    axes[0].legend(fontsize=8, loc="upper left", frameon=False)
    # Vietnam panel needs its own scale note
    axes[1].annotate("note scale:\nsingle-bystander\nupper bound",
                     xy=(0.62, 0.08), xycoords="axes fraction", fontsize=8,
                     color="#666666")

    fig.tight_layout()
    out = ROOT / "output" / "calibration_nested_results.pdf"
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=110, bbox_inches="tight")
    shutil.copy2(out, ROOT / "Exchange_Rate_Tariffs" / out.name)
    print(f"Saved: {out} (+png, + paper copy)")


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
