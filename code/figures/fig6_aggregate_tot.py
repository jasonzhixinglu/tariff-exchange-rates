"""Paper Figure 6, panels (a)-(b), and online-supplement Figure S4.1, panel (c)
(files fig6*).

Panels (a) and (b) plot the aggregate terms-of-trade response
R_{A|B} = b_AB R^B_B + (1-b_AB) Rbar^B_{-B} at a fixed baseline: (a) symmetric
benchmark, (b) small target with a low import weight, with its target and
bystander contributions.  Panel (c) (supplement) plots the normalized
numerator Q_{A|B}(rho) for the strongly asymmetric network (two crossings).
Baselines from code/checks/asymmetry_checks.py.  MML is checked at the fixed
baseline over the whole plotted rho range."""
import os
import sys

import numpy as np

import style
from style import AQUA, BLUE, GREY, MUTED, ORANGE, SHADE, plt

sys.path.insert(0, os.path.join(style.ROOT, "code", "checks"))
import asymmetry_checks as ac  # noqa: E402
from model import asymmetry as asy  # noqa: E402
from model import linear as lin  # noqa: E402

plt.rcParams["hatch.linewidth"] = 0.4
YLIM = (-0.45, 0.15)
XLABEL = r"Cross-origin elasticity, $\rho$"
panels = {"a": (ac.example_a, (1, 10)), "b": (ac.example_b, (1, 10)), "c": (ac.example_c, (1, 30))}
for name, (fn, xr) in panels.items():
    base, q = fn()
    qh = asy.normalized(q)
    roots = asy.positive_roots(q)
    rho = np.linspace(*xr, 600)
    vals = np.polyval(qh, rho)
    # cross-check the polynomial against the linear solver (sign of R_{A|B})
    for r in np.linspace(xr[0] + 0.3, xr[1] - 0.3, 7):
        bb = lin.with_rho(base, r)
        R = lin.import_weights(base) @ lin.response(bb, ac.D)
        assert np.sign(R) == np.sign(np.polyval(qh, r)) or abs(R) < 1e-12
    # MML at the fixed baseline throughout the plotted range (and at the roots)
    for r in list(np.linspace(*xr, 200)) + list(roots):
        assert lin.mml(lin.reduced_jacobian(lin.with_rho(base, r))), (name, r)
    if name == "a":
        assert len(roots) == 0 and np.all(vals < 0)
    elif name == "b":
        assert len(roots) == 1 and abs(roots[0] - 3.344) < 1e-3
    else:
        assert len(roots) == 2

    fig, ax = plt.subplots(figsize=(style.PANEL_W, 2.5))
    if name in ("a", "b"):
        # contributions b_Aj R^B_j: target j = B, bystander j = C (N = 3)
        b = lin.import_weights(base)
        contrib = np.array([b * lin.response(lin.with_rho(base, r), ac.D) for r in rho])
        agg = contrib.sum(axis=1)
        assert agg.min() > YLIM[0] and agg.max() < YLIM[1]
        style.zero_line(ax)
        if name == "b":
            ax.plot(rho, contrib[:, 0], color=ORANGE, lw=1.1, ls=(0, (5, 2)), label="Target contribution")
            ax.plot(rho, contrib[:, 1], color=AQUA, lw=1.1, ls=(0, (6, 1.5, 1, 1.5)),
                    label="Bystander contribution")
            ax.axvline(roots[0], color=MUTED, lw=0.6, ls=(0, (1, 1.5)))
            ax.text(roots[0] + 0.15, 0.12, r"$\rho^*=%.2f$" % roots[0], fontsize=8.5, va="top")
            # sign labels hug the zero line at the right edge, clear of the curves
            ax.text(0.995, 0.005, "ToT deterioration", fontsize=7, color=MUTED, ha="right", va="bottom",
                    transform=ax.get_yaxis_transform())
            ax.text(0.995, -0.035, "ToT improvement", fontsize=7, color=MUTED, ha="right", va="top",
                    transform=ax.get_yaxis_transform())
        ax.plot(rho, agg, color=BLUE, lw=2.2, label="Aggregate response")
        if name == "b":
            ax.legend(loc="lower right", handlelength=2.4)
        ax.set_ylim(*YLIM)
        ax.set_xlim(*xr)
        ax.set_xlabel(XLABEL)
        ax.set_ylabel(r"Aggregate ToT response, $R_{A|B}$")
    else:
        # shaded = Q-hat > 0: A's aggregate terms of trade deteriorate (gray + hatch for print)
        ax.fill_between(rho, vals, 0, where=vals > 0, facecolor=SHADE, edgecolor=GREY, hatch="////",
                        lw=0, label="condition fails")
        ax.plot(rho, vals, color=BLUE)
        ax.axhline(0, color=MUTED, lw=0.6)
        for r in roots:
            ax.axvline(r, color=MUTED, lw=0.5, ls=(0, (2, 2)))
            ax.text(r, 0.03, "%.2f" % r, transform=ax.get_xaxis_transform(), fontsize=8.5,
                    ha="center", bbox=dict(fc="white", ec="none", pad=0.5))
        ax.set_xlim(*xr)
        ax.set_xlabel(r"$\rho$")
        ax.set_ylabel(r"$\hat Q_{A|B}(\rho)$")
    style.save(fig, "fig6%s_aggregate_tot.pdf" % name)
