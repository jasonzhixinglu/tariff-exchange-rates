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
    fig, ax = plt.subplots(figsize=(style.PANEL_W, style.PANEL_W))
    lim = 0.85
    s = np.linspace(-lim, lim, 2)
    ax.plot(s, s, color=GREY, lw=0.7, ls=(0, (4, 2)))
    ax.plot(s, -s, color=GREY, lw=0.7, ls=(0, (1, 1.5)))
    ax.axhline(0, color=MUTED, lw=0.5); ax.axvline(0, color=MUTED, lw=0.5)
    ax.text(0.12, 0.22, r"common ($\mathbf{1}$)", color=GREY, fontsize=7, rotation=45,
            ha="center", va="center")
    ax.text(-0.52, 0.62, "zero-sum", color=GREY, fontsize=7, rotation=-45,
            ha="center", va="center")
    tip_ext = common + N * rel
    arrow(ax, common, tip_ext, ORANGE, ls=(0, (3, 2)), lw=1.0)
    arrow(ax, (0, 0), common, BLUE)
    arrow(ax, common, eq, ORANGE)
    arrow(ax, (0, 0), eq, INK, lw=1.6)
    ax.plot(*eq, "o", color=INK, ms=3.5)
    ax.annotate(r"$\lambda_{\mathrm{avg}}\bar t\,\mathbf{1}$", xy=common, xytext=(common[0] - 0.52, common[1] - 0.12),
                fontsize=8, color=BLUE)
    ax.annotate(r"$d\nu$", xy=eq, xytext=(eq[0] + 0.03, eq[1] + 0.05), fontsize=8)
    ax.text(tip_ext[0] + 0.02, tip_ext[1] + 0.02, r"$F/j_S$", fontsize=8, color=ORANGE)
    ax.set_xlim(-0.95, 0.45); ax.set_ylim(-0.6, lim)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$d\nu_B$"); ax.set_ylabel(r"$d\nu_C$")
    ax.set_title(r"$\rho=%.1f$:  $d\nu=(%.3f,\ %+.3f)$" % (rho, eq[0], eq[1]), fontsize=8)
    style.save(fig, "fig2%s_geometry.pdf" % panel)
