"""Paper Figure 5 (files fig6*): three relationships between rho and the
aggregate terms-of-trade condition.  Normalized Q_{A|B}(rho) at a fixed
baseline: (a) symmetric benchmark (no crossing), (b) small target with a low
import weight (single crossing), (c) strongly asymmetric network (two
crossings).  Baselines from code/checks/asymmetry_checks.py.  MML is checked at
the fixed baseline over the whole plotted rho range, so every shaded region
lies inside the MML-valid region."""
import os
import sys

import numpy as np

import style
from style import BLUE, GREY, MUTED, SHADE, plt

sys.path.insert(0, os.path.join(style.ROOT, "code", "checks"))
import asymmetry_checks as ac  # noqa: E402
from model import asymmetry as asy  # noqa: E402
from model import linear as lin  # noqa: E402

plt.rcParams["hatch.linewidth"] = 0.4
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
    fig, ax = plt.subplots(figsize=(1.95, 1.9))
    # shaded = Q-hat > 0: A's aggregate terms of trade deteriorate (gray + hatch for print)
    ax.fill_between(rho, vals, 0, where=vals > 0, facecolor=SHADE, edgecolor=GREY, hatch="////",
                    lw=0, label="condition fails")
    ax.plot(rho, vals, color=BLUE)
    ax.axhline(0, color=MUTED, lw=0.6)
    for r in roots:
        ax.axvline(r, color=MUTED, lw=0.5, ls=(0, (2, 2)))
        ax.text(r, 0.03, "%.2f" % r, transform=ax.get_xaxis_transform(), fontsize=7, ha="center",
                bbox=dict(fc="white", ec="none", pad=0.5))
    ax.set_xlim(*xr)
    ax.set_xlabel(r"$\rho$")
    if name == "a":
        ax.set_ylabel(r"$\hat Q_{A|B}(\rho)$")
    style.save(fig, "fig6%s_aggregate_tot.pdf" % name)
