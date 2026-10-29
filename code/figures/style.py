"""Shared matplotlib style for the paper's figures.

One palette (validated categorical slots 1-4: blue, orange, aqua, yellow) plus
grey for references; every series also differs in line style so figures read
in grayscale.  Computer Modern via mathtext to match the LaTeX body text.
Panels are separate PDFs, combined in LaTeX with subcaption.
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "paper", "figures")
sys.path.insert(0, os.path.join(ROOT, "code"))

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
GREY, INK, MUTED = "#8c8c8c", "#222222", "#666666"
SHADE = "#e9e9e9"
STYLES = {  # color, dashes
    1: (BLUE, "-"),
    2: (ORANGE, (0, (5, 2))),
    3: (AQUA, (0, (1, 1.5))),
    4: (YELLOW, (0, (6, 2, 1, 2))),
}

PANEL_W = 2.9      # inches; two panels side by side at 0.45\textwidth each
FULL_W = 5.85      # 0.9\textwidth of a 6.5in text block

plt.rcParams.update({
    "font.family": ["cmr10", "DejaVu Serif"],
    "font.serif": ["cmr10", "Computer Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.formatter.use_mathtext": True,
    "axes.unicode_minus": False,
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 9,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "lines.linewidth": 1.6,
    "legend.frameon": False,
    "pdf.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})


def line(ax, x, y, slot, label=None, **kw):
    color, dash = STYLES[slot]
    return ax.plot(x, y, color=color, linestyle=dash, label=label, **kw)


def zero_line(ax):
    ax.axhline(0.0, color=MUTED, lw=0.6, zorder=0)


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    fig.savefig(path)
    plt.close(fig)
    print("wrote", os.path.relpath(path, ROOT))
