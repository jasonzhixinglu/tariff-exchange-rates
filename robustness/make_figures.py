# -*- coding: utf-8 -*-
"""Redraw the task B and task D figures from the saved results (the task
scripts also draw them; this avoids re-solving to adjust a layout)."""
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
import style

HERE = os.path.dirname(__file__)
R = lambda f: json.load(open(os.path.join(HERE, "results", f)))


def fig_b():
    out = R("task_b.json")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1))
    for ax, scen, lab in zip(axes, ("unilateral", "retaliation"),
                             (r"$\rho^\ast(\tau)/3\rho_D$", r"$\rho^\ast(\tau)/\rho_D$")):
        for (name, r), c in zip(out["scen"][scen].items(), style.SERIES):
            t = np.array(r["tau"])
            ax.plot(np.r_[0, t], np.r_[1, r["ratio"]], color=c, lw=1.7, label=name)
            tt = np.linspace(0, 0.3, 10)
            ax.plot(tt, 1 + r["kappa"] * tt / r["rho0"], color=c, lw=0.9, ls=(0, (3, 2)))
        ax.axhline(1, color=style.MUTED, lw=0.7)
        ax.set_xlabel(r"tariff $\tau$")
        ax.set_ylabel(lab)
        ax.set_title("(a) unilateral tariff on B" if scen == "unilateral"
                     else r"(b) bilateral retaliation, $\tau_{AB}=\tau_{BA}=\tau$", fontsize=9)
        style.finish(ax)
    axes[0].legend(frameon=False, fontsize=7.5, loc="lower left")
    fig.text(0.5, 0.005, r"solid: exact threshold;  dashed: local slope $\rho^\ast_0+\kappa\tau$",
             ha="center", fontsize=7.5, color="0.4")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(HERE, "figures", "task_b_threshold.png"), dpi=200)


def fig_d():
    d = np.load(os.path.join(HERE, "results", "task_d_common.npz"))
    opt = R("task_d_targeted_common.json")
    labels = (r"$d\nu_A^E/d\tau$ (trade-weighted)", r"$(d\nu_B-d\nu_C)/d\tau$")
    titles = ("(a) NEER of A", "(b) target vs bystander")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1))
    for ax, key, okey, lab, title in zip(axes, ("neer_raw", "order_raw"), ("neer", "order"),
                                         labels, titles):
        ax.scatter(d["rho"], d[key], s=1.5, color=style.SERIES[0], alpha=0.35, lw=0,
                   rasterized=True)
        o = opt[okey]
        x0 = o["params"]["rho"][0]
        ax.plot([x0], [o["raw"]], marker="*", ms=9, color=style.SERIES[1], ls="none")
        right = x0 > 5
        ax.annotate("targeted-search\nmaximum %.2f" % o["raw"], (x0, o["raw"]),
                    xytext=(-8 if right else 10, -2), textcoords="offset points",
                    ha="right" if right else "left", va="top", fontsize=7, color="0.3")
        ax.axhline(0, color="0.2", lw=0.7)
        ax.set_xlabel(r"$\rho$")
        ax.set_ylabel(lab)
        ax.set_title(title, fontsize=9)
        style.finish(ax)
    fig.text(0.5, 0.005, "20,000 draws, common elasticities, MML-satisfying draws only (19,995); "
             "points above zero reverse the symmetric-benchmark sign",
             ha="center", fontsize=7.2, color="0.4")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(HERE, "figures", "task_d_search.png"), dpi=200)


if __name__ == "__main__":
    which = sys.argv[1:] or ["b", "d"]
    if "b" in which:
        fig_b()
    if "d" in which:
        fig_d()
    print("figures redrawn:", which)
