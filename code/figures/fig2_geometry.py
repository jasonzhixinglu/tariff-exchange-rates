"""Figure 2: average protection and relative treatment, N = 3, unilateral
tariff t = (1, 0); alpha_D = 0.7, alpha_T = 0.6, eta = 1.5.

Vectors come from Theorem 3.2 and are cross-checked against the linear
solver; the coordinates stated in the draft are asserted."""
import numpy as np

import style
from style import AQUA, BLUE, GREY, INK, MUTED, ORANGE, plt
from model import closed_forms as cf
from model import linear as lin

N, CAL = 3, cf.FIG2
t = np.array([1.0, 0.0])
tbar = t.mean()
ttil = t - tbar
EXPECTED = {2.2: dict(common=(-0.275, -0.275), rel=(-0.173, 0.173), eq=(-0.448, -0.103)),
            5.0: dict(common=(-0.166, -0.166), rel=(-0.236, 0.236), eq=(-0.402, 0.070))}

assert abs(cf.rhoD(**CAL) - 1.17) < 1e-12


def vectors(rho):
    common = cf.lamA(N, rho=rho, **CAL) * tbar * np.ones(2)
    rel = cf.lamR(N, rho=rho, **CAL) * ttil
    d = np.zeros((3, 3)); d[0, 1:] = t
    eq = lin.response(lin.symmetric_base(N, rho=rho, **CAL), d)
    assert np.allclose(common + rel, eq, atol=1e-12)
    # F / j_S: the response if relative adjustment were no more effective than common
    F = lin.disturbance(lin.symmetric_base(N, rho=rho, **CAL), d)
    jS = cf.m(CAL["aD"], CAL["aT"]) * cf.MN(N, rho=rho, aD=CAL["aD"], eta=CAL["eta"]) / (N - 1)
    assert np.allclose(F / jS, common + N * rel, atol=1e-12)
    return common, rel, eq, F


def arrow(ax, start, end, color, ls="-", lw=1.4):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, linestyle=ls,
                                shrinkA=0, shrinkB=0, mutation_scale=9))


for panel, rho in (("a", 2.2), ("b", 5.0)):
    common, rel, eq, F = vectors(rho)
    for k, v in (("common", common), ("rel", rel), ("eq", eq)):
        assert np.allclose(np.round(v, 3), EXPECTED[rho][k], atol=1.5e-3), (rho, k, v)
    if panel == "a":
        assert F[1] > 0 and eq[1] < 0      # C gains at old rates, yet A appreciates against C
    else:
        assert eq[1] > 0
    fig, ax = plt.subplots(figsize=(style.PANEL_W, 2.65))
    lim = 0.95
    s = np.linspace(-lim, lim, 2)
    ax.plot(s, s, color=GREY, lw=0.7, ls=(0, (4, 2)))
    z = np.linspace(-0.42, 0.45, 2)
    ax.plot(z, -z, color=GREY, lw=0.7, ls=(0, (1, 1.5)))
    ax.axhline(0, color=MUTED, lw=0.5); ax.axvline(0, color=MUTED, lw=0.5)
    ax.text(0.24, 0.40, r"$\mathbf{1}$ direction", color=MUTED, fontsize=8.5, rotation=45,
            ha="center", va="center")
    ax.text(0.37, -0.17, "zero-sum", color=MUTED, fontsize=8.5, rotation=-45, ha="center", va="center")
    tip_ext = common + N * rel
    arrow(ax, common, tip_ext, ORANGE, ls=(0, (3, 2)), lw=1.1)
    arrow(ax, (0, 0), common, BLUE, lw=1.8)
    arrow(ax, common, eq, ORANGE, lw=1.8)
    arrow(ax, (0, 0), eq, INK, lw=2.0)
    ax.plot(*eq, "o", color=INK, ms=4)
    # direct labels, so the arrows read without colour
    ax.text(-0.04, -0.29, "common", fontsize=9, color=BLUE, ha="left", va="top")
    mid = (common + eq) / 2
    ax.text(mid[0] - 0.06, mid[1] - 0.02, "relative", fontsize=9, color=ORANGE, ha="right", va="top")
    ax.text(eq[0] + 0.05, eq[1] + 0.05, r"$d\nu$", fontsize=10, color=INK, ha="left", va="bottom")
    ax.text(tip_ext[0] + 0.06, tip_ext[1], "counterfactual", fontsize=8, color=ORANGE,
            ha="left", va="center")
    ax.set_xlim(-0.95, 0.45); ax.set_ylim(-0.48, 0.74)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$d\nu_B$"); ax.set_ylabel(r"$d\nu_c$")
    style.save(fig, "fig2%s_geometry.pdf" % panel)
