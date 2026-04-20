"""
Visualization for 2-country and 3-country tariff-exchange rate models.

plot_tb_locus          — 2-country: trade balance curve(s) over log exchange rate
plot_equilibria        — 3-country: balanced-trade loci and equilibria across regimes
plot_calibration_results — grouped bar chart of exchange rate changes by regime
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from .economy import compute_allocation
from .equilibrium import solve_2country, solve_3country

_COUNTRY_IDX = {"A": 0, "B": 1, "C": 2}


# =============================================================================
# 2-Country: trade balance locus
# =============================================================================

def plot_tb_locus(params, taus, log_e_range=(-1.5, 1.5), n_points=300,
                  title=None, pdf_name=None, figsize=(8, 4)):
    """
    Plot country A's trade balance as a function of the log exchange rate
    for one or more tariff rates, and mark the equilibrium for each.

    Parameters
    ----------
    params      : dict   — 2-country model parameters
    taus        : list   — tariff rates to overlay (e.g. [0.0, 0.5, 1.0])
    log_e_range : tuple  — (min, max) for log(e_AB)
    n_points    : int    — grid resolution
    title       : str    — plot title (auto-generated if None)
    pdf_name    : str    — save to PDF if provided
    figsize     : tuple
    """
    log_e_vec = np.linspace(*log_e_range, n_points)
    e_vec     = np.exp(log_e_vec)

    fig, ax = plt.subplots(figsize=figsize)

    for tau in taus:
        tariffs = np.array([[0.0, tau], [0.0, 0.0]])
        tb_vec  = [
            compute_allocation(params, [e], tariffs)["trade_balance"][0]
            for e in e_vec
        ]
        label = f"τ = {tau}" if tau > 0 else "free trade"
        (line,) = ax.plot(log_e_vec, tb_vec, label=label)

        # Mark equilibrium
        eq = solve_2country(params, tau=tau, log_e_bounds=log_e_range)
        ax.scatter(eq["log_e_AB"], 0, color=line.get_color(), zorder=5, s=50)

    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel(r"$\log(e_{AB})$", fontsize=12)
    ax.set_ylabel("Trade balance (A)", fontsize=11)
    ax.set_title(title or "Two-country model: trade balance locus", fontsize=12)
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    if pdf_name:
        plt.savefig(pdf_name, dpi=150, bbox_inches="tight")
        print(f"Saved: {pdf_name}")
    plt.show()


# =============================================================================
# 3-Country: balanced-trade loci and equilibria
# =============================================================================

def _compute_tb_grid(params, tariffs, log_eAB_vec, log_eAC_vec):
    """Evaluate trade balances and real exchange rates over a 2D grid."""
    log_EAB, log_EAC = np.meshgrid(log_eAB_vec, log_eAC_vec)
    shape = log_EAB.shape

    TB  = [np.zeros(shape) for _ in range(3)]
    log_QAB = np.zeros(shape)
    log_QAC = np.zeros(shape)

    for i in range(shape[0]):
        for j in range(shape[1]):
            e_AB = np.exp(log_EAB[i, j])
            e_AC = np.exp(log_EAC[i, j])
            out  = compute_allocation(params, [e_AB, e_AC], tariffs)
            for k in range(3):
                TB[k][i, j] = out["trade_balance"][k]
            P = out["price_level"]
            log_QAB[i, j] = np.log(e_AB * P[1] / P[0])
            log_QAC[i, j] = np.log(e_AC * P[2] / P[0])

    return {
        "log_EAB": log_EAB, "log_EAC": log_EAC,
        "TB_A": TB[0], "TB_B": TB[1], "TB_C": TB[2],
        "log_QAB": log_QAB, "log_QAC": log_QAC,
    }


def _log_e_grid(grids, i, j):
    """
    Extract log(e_ij) as a grid array from the base grids (log_EAB, log_EAC).
    Uses no-arbitrage: log e_ij = log r_j - log r_i where r = [1, e_AB, e_AC].
    """
    log_r = [np.zeros_like(grids["log_EAB"]), grids["log_EAB"], grids["log_EAC"]]
    return log_r[j] - log_r[i]


def _log_e_star(eq, i, j):
    """Extract log(e_ij) from a solve_3country result dict."""
    log_r = [0.0, eq["log_e_AB"], eq["log_e_AC"]]
    return log_r[j] - log_r[i]


def plot_equilibria(
    params,
    tariff_scenarios,
    tb_pair=("B", "C"),
    coord1=("A", "B"),
    coord2=("A", "C"),
    log_eAB_range=(-1.0, 1.0),
    log_eAC_range=(-1.0, 1.0),
    n_grid=50,
    tb_colors=("red", "green"),
    figsize=(8, 7),
    title=None,
    pdf_name=None,
):
    """
    Plot balanced-trade loci and equilibria for one or more tariff regimes.

    Each regime contributes two contour lines (TB_i = 0 and TB_j = 0 for the
    chosen tb_pair) and an annotated equilibrium point. The axes can display
    any valid bilateral rate derived from the two free rates (e_AB, e_AC).

    Parameters
    ----------
    params          : dict  — 3-country model parameters
    tariff_scenarios : dict  {label: tariff_matrix (3x3 numpy array)}
    tb_pair         : (X, Y) — which two countries' balanced-trade loci to show
    coord1          : (X, Y) — country pair for x-axis
    coord2          : (X, Y) — country pair for y-axis
    log_eAB_range   : (min, max) for log(e_AB) grid
    log_eAC_range   : (min, max) for log(e_AC) grid
    n_grid          : int  — grid resolution per axis
    tb_colors       : (color_i, color_j) for the two TB = 0 loci
    figsize         : tuple
    title           : str  — plot title (auto-generated if None)
    pdf_name        : str  — save to PDF if provided
    """
    sigma = params.get("sigma", 1.0)
    model_label = (
        "Cobb-Douglas" if abs(sigma - 1.0) < 1e-10 else f"CES (σ = {sigma})"
    )

    i_cty = _COUNTRY_IDX[tb_pair[0]]
    j_cty = _COUNTRY_IDX[tb_pair[1]]
    c1_i  = _COUNTRY_IDX[coord1[0]]
    c1_j  = _COUNTRY_IDX[coord1[1]]
    c2_i  = _COUNTRY_IDX[coord2[0]]
    c2_j  = _COUNTRY_IDX[coord2[1]]

    log_eAB_vec = np.linspace(*log_eAB_range, n_grid)
    log_eAC_vec = np.linspace(*log_eAC_range, n_grid)

    line_styles = ["solid", "dashed", "dotted", "dashdot"]
    c_i, c_j    = tb_colors

    fig, ax = plt.subplots(figsize=figsize)
    legend_handles, legend_labels = [], []

    # Solve equilibria first so annotations can be spaced intelligently
    solved = []
    for name, T in tariff_scenarios.items():
        eq = solve_3country(params, T)
        solved.append({
            "name": name,
            "T":    T,
            "eq":   eq,
            "x":    _log_e_star(eq, c1_i, c1_j),
            "y":    _log_e_star(eq, c2_i, c2_j),
        })

    xs    = [s["x"] for s in solved]
    x_mid = (max(xs) + min(xs)) / 2 if len(xs) > 1 else xs[0]

    for k, pt in enumerate(solved):
        name   = pt["name"]
        eq     = pt["eq"]
        x_star = pt["x"]
        y_star = pt["y"]
        style  = line_styles[k % len(line_styles)]
        dx     = 14 if x_star >= x_mid else -80
        dy     = 14 + k * 28

        grids  = _compute_tb_grid(params, pt["T"], log_eAB_vec, log_eAC_vec)
        log_X  = _log_e_grid(grids, c1_i, c1_j)
        log_Y  = _log_e_grid(grids, c2_i, c2_j)

        CS_i = ax.contour(log_X, log_Y, grids[f"TB_{tb_pair[0]}"],
                          levels=[0], colors=c_i, linestyles=style, linewidths=2)
        CS_j = ax.contour(log_X, log_Y, grids[f"TB_{tb_pair[1]}"],
                          levels=[0], colors=c_j, linestyles=style, linewidths=2)

        ax.scatter(x_star, y_star, s=60, color="black", zorder=5)
        ax.annotate(
            f"{name}\n({x_star:.2f}, {y_star:.2f})",
            xy=(x_star, y_star),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=9,
            arrowprops=dict(arrowstyle="-", color="black", lw=0.8,
                            shrinkA=0, shrinkB=4),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.85),
            zorder=6,
        )

        h_i, _ = CS_i.legend_elements()
        h_j, _ = CS_j.legend_elements()
        legend_handles += [h_i[0], h_j[0]]
        legend_labels  += [
            f"$TB_{{{tb_pair[0]}}}=0$ ({name})",
            f"$TB_{{{tb_pair[1]}}}=0$ ({name})",
        ]

    x_label = f"log($e_{{{coord1[0]}{coord1[1]}}}$)"
    y_label = f"log($e_{{{coord2[0]}{coord2[1]}}}$)"
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(title or f"{model_label}: {', '.join(tariff_scenarios)}", fontsize=12)
    ax.legend(legend_handles, legend_labels, fontsize=9, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    if pdf_name:
        plt.savefig(pdf_name, dpi=150, bbox_inches="tight")
        print(f"Saved: {pdf_name}")
    plt.show()


# =============================================================================
# Calibration results bar chart
# =============================================================================

def plot_calibration_results(
    results_df,
    config_col="Configuration",
    regime_col="Regime",
    er_cols=None,
    er_labels=None,
    colors=None,
    figsize=(13, 4.5),
    title=None,
    pdf_name=None,
):
    """
    Grouped bar chart of bilateral exchange rate changes across tariff regimes,
    one panel per model configuration.

    Parameters
    ----------
    results_df  : pd.DataFrame — output of the calibration run with columns for
                  configuration, regime, and at least three exchange rate changes
    config_col  : str — column identifying the model configuration
    regime_col  : str — column identifying the tariff regime
    er_cols     : list of str — columns with % exchange rate changes to plot
    er_labels   : list of str — axis labels for each exchange rate pair (LaTeX ok)
    colors      : list of str — bar colors
    figsize     : tuple
    title       : str
    pdf_name    : str — save to PDF/PNG if provided (saves both formats)
    """
    configs = results_df[config_col].unique()

    if er_cols is None:
        er_cols = [c for c in results_df.columns
                   if c not in (config_col, regime_col)][:3]
    if er_labels is None:
        er_labels = er_cols
    if colors is None:
        colors = ["#2166ac", "#d6604d", "#4dac26"]

    regimes = results_df[regime_col].unique()
    x       = np.arange(len(regimes))
    width   = 0.22

    fig, axes = plt.subplots(1, len(configs), figsize=figsize, sharey=False)
    if len(configs) == 1:
        axes = [axes]

    for col_idx, (cfg, ax) in enumerate(zip(configs, axes)):
        sub = results_df[results_df[config_col] == cfg]

        for k, (col, label, color) in enumerate(zip(er_cols, er_labels, colors)):
            vals = sub.set_index(regime_col).loc[regimes, col].values
            ax.bar(x + (k - 1) * width, vals, width,
                   label=label, color=color, alpha=0.85, edgecolor="white")

        ax.axhline(0, color="black", linewidth=0.7, linestyle="--")
        ax.set_xticks(x)
        ax.set_xticklabels(regimes, fontsize=8.5)
        ax.set_title(cfg, fontsize=10, fontweight="bold")
        ax.set_ylabel("% change vs. free trade" if col_idx == 0 else "")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=len(er_cols),
               fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.04))
    fig.suptitle(
        title or "Model-implied bilateral exchange rate changes by configuration and regime",
        fontsize=11, y=1.01,
    )
    plt.tight_layout()

    if pdf_name:
        base = pdf_name.rsplit(".", 1)[0]
        plt.savefig(f"{base}.pdf", dpi=150, bbox_inches="tight")
        plt.savefig(f"{base}.png", dpi=150, bbox_inches="tight")
        print(f"Saved: {base}.pdf, {base}.png")
    plt.show()
