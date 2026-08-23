"""
Generate the two-panel threshold figure for Section 3.3 of the paper.

Panel (a): equilibrium response of log e_AC to an isolated tariff
           (tau_AB = 0.2) as a function of the cross-origin elasticity rho,
           for three values of the macro elasticity eta, with the analytic
           thresholds rho*(eta) marked. Flat-CES path (rho = eta = sigma)
           overlaid to show the asymptote that never crosses.
Panel (b): the threshold rho* = 3[1 + aD(eta-1) - aT(1-aD)] as a function
           of home bias aD for the same eta values, with the measured
           cross-origin elasticity range shaded.

Output: output/threshold_figure.pdf, copied to Exchange_Rate_Tariffs/.
"""

import shutil
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tariff_exchange_rates.nested import (  # noqa: E402
    make_params_nested, rho_star_symmetric, solve_3country_nested,
)

AD, AT, TAU = 0.80, 0.40, 0.20
ETAS = [1.0, 1.5, 2.0]
COLORS = {1.0: "#66a3c2", 1.5: "#2166ac", 2.0: "#0b3d63"}


def d_logeAC_cum(eta, rho, tau=TAU):
    """Cumulative log e_AC change for an isolated tariff of size tau."""
    p = make_params_nested(alpha_T=AT, alpha_D=AD, eta=eta, rho=rho)
    T0, T1 = np.zeros((3, 3)), np.zeros((3, 3))
    T1[0, 1] = tau
    eq0 = solve_3country_nested(p, T0)
    eq1 = solve_3country_nested(p, T1, init=[eq0["log_e_AB"], eq0["log_e_AC"]])
    return eq1["log_e_AC"] - eq0["log_e_AC"]


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

    # ---------------- Panel (a): response vs rho ----------------
    rhos = np.linspace(1.05, 9.0, 60)
    for eta in ETAS:
        vals = [d_logeAC_cum(eta, r) for r in rhos]
        ax1.plot(rhos, 100 * np.array(vals), color=COLORS[eta], lw=2,
                 label=rf"$\eta = {eta:g}$")
        rs = rho_star_symmetric(AD, AT, eta)
        if rhos.min() < rs < rhos.max():
            ax1.axvline(rs, color=COLORS[eta], ls=":", lw=1.2)
            ax1.annotate(rf"$\rho^*={rs:.2f}$", xy=(rs, ax1.get_ylim()[0]),
                         xytext=(rs + 0.06, -1.55), color=COLORS[eta],
                         fontsize=9, rotation=90, va="bottom")
    # flat-CES path rho = eta = sigma
    sig = np.linspace(1.05, 9.0, 40)
    flat = [d_logeAC_cum(s, s) for s in sig]
    ax1.plot(sig, 100 * np.array(flat), color="#c23b22", lw=2, ls="--",
             label=r"flat CES ($\rho=\eta=\sigma$)")
    ax1.axhline(0, color="gray", lw=0.8)
    ax1.set_xlabel(r"cross-origin elasticity $\rho$", fontsize=11)
    ax1.set_ylabel(r"$\Delta \log e_{AC} \times 100$ (isolated tariff $\tau_{AB}=0.2$)",
                   fontsize=10)
    ax1.set_title("(a) Reversal requires separating the margins", fontsize=11)
    ax1.legend(fontsize=9, loc="upper left", frameon=False)
    ax1.spines[["top", "right"]].set_visible(False)

    # ---------------- Panel (b): rho* vs home bias ----------------
    aDs = np.linspace(0.45, 0.95, 100)
    for eta in ETAS:
        ax2.plot(aDs, [rho_star_symmetric(a, AT, eta) for a in aDs],
                 color=COLORS[eta], lw=2, label=rf"$\eta = {eta:g}$")
    ax2.axhspan(3.0, 8.0, color="#c8e0c8", alpha=0.5, zorder=0)
    ax2.annotate("measured cross-origin\nelasticity range", xy=(0.47, 7.4),
                 fontsize=9, color="#3a6b3a")
    ax2.plot([AD], [rho_star_symmetric(AD, AT, 1.5)], "o", color="#2166ac",
             ms=6, zorder=5)
    ax2.annotate(r"US-realistic: $\rho^*\!=3.96$",
                 xy=(AD, rho_star_symmetric(AD, AT, 1.5)),
                 xytext=(0.62, 2.2), fontsize=9,
                 arrowprops=dict(arrowstyle="->", lw=0.8))
    ax2.set_xlabel(r"home bias $\alpha_D$", fontsize=11)
    ax2.set_ylabel(r"threshold $\rho^*$", fontsize=11)
    ax2.set_title(r"(b) $\rho^* = 3[1+\alpha_D(\eta-1)-\alpha_T(1-\alpha_D)]$",
                  fontsize=11)
    ax2.legend(fontsize=9, loc="lower right", frameon=False)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    out = ROOT / "output" / "threshold_figure.pdf"
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=110, bbox_inches="tight")
    shutil.copy2(out, ROOT / "Exchange_Rate_Tariffs" / "threshold_figure.pdf")
    print(f"Saved: {out} (+ .png preview, + copy in Exchange_Rate_Tariffs/)")


if __name__ == "__main__":
    np.seterr(all="ignore")
    main()
