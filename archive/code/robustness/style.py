# -*- coding: utf-8 -*-
"""Shared figure style for the robustness figures (matches the paper's
serif / Computer Modern look)."""
import matplotlib

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.linewidth": 0.7,
    "axes.edgecolor": "0.25",
    "xtick.color": "0.25",
    "ytick.color": "0.25",
    "axes.labelcolor": "0.1",
})

SERIES = ["#1f4e79", "#c0504d", "#6a9a3a", "#7f6084"]
MUTED = "0.55"


def finish(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=3, width=0.6)
