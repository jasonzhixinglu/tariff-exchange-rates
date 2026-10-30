"""Figure 4: the composite bystander.  (a) N rho_D and the threshold of the
'ordinary-eta' composite against N; (b) eta_C against N for rho in {2, 4, 8}.
US-like parameters.  Thresholds are computed from the composite economy with
the linear solver and checked against N rho_D."""
import numpy as np
from scipy.optimize import brentq

import style
from style import plt
from model import closed_forms as cf
from model import linear as lin

CAL = cf.US_LIKE
Ns = np.arange(3, 11)
cc = np.zeros((3, 3)); cc[0, 1] = 1.0


def threshold(N, ordinary):
    f = lambda r: lin.response(cf.composite_base(N, CAL["aD"], CAL["aT"], CAL["eta"], r,
                                                 ordinary_eta=ordinary), cc)[1]
    return brentq(f, 1.0001, 40.0, xtol=1e-12)


true = np.array([threshold(N, False) for N in Ns])
ordinary = np.array([threshold(N, True) for N in Ns])
assert np.allclose(true, Ns * cf.rhoD(**CAL), atol=1e-9)
assert np.all(np.diff(ordinary) < 0)

fig, ax = plt.subplots(figsize=(style.PANEL_W, 2.4))
style.line(ax, Ns, true, 1, r"$N\rho_D$ (true, composite with $\eta_C$)", marker="o", ms=3)
style.line(ax, Ns, ordinary, 2, r"composite with ordinary $\eta$", marker="s", ms=3)
ax.set_xlabel(r"$N$"); ax.set_ylabel(r"bystander threshold in $\rho$")
ax.set_ylim(0, 14); ax.legend(loc="upper left", fontsize=7)
style.save(fig, "fig4a_composite_threshold.pdf")

fig, ax = plt.subplots(figsize=(style.PANEL_W, 2.4))
for slot, rho in zip((1, 2, 3), (2.0, 4.0, 8.0)):
    eC = np.array([cf.eta_C(N, CAL["aD"], CAL["eta"], rho) for N in Ns])
    style.line(ax, Ns, eC, slot, r"$\rho=%g$" % rho, marker="o", ms=3)
    ax.axhline(rho, color=style.STYLES[slot][0], lw=0.6, alpha=0.6)
ax.axhline(CAL["eta"], color=style.GREY, lw=0.6)
ax.text(10.1, CAL["eta"], r"$\eta$", va="center", fontsize=8)
ax.set_xlabel(r"$N$"); ax.set_ylabel(r"$\eta_C$")
ax.set_ylim(0, 8.6); ax.legend(loc="center right", fontsize=7)
style.save(fig, "fig4b_eta_C.pdf")
