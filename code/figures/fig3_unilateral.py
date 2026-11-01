"""Figure 3: bilateral and effective responses to a unilateral tariff,
US-like parameters, N = 3 (panel a) and N = 5 (panel b).  Closed forms of
Proposition 3.3, cross-checked against the linear solver."""
import numpy as np

import style
from style import GREY, SHADE, plt
from model import closed_forms as cf
from model import linear as lin

CAL = cf.US_LIKE
rhos = np.linspace(1.0, 10.0, 451)

for panel, N in (("a", 3), ("b", 5)):
    resp = np.array([cf.unilateral(N, rho=r, **CAL) for r in rhos])   # neer, dB, dC
    d = np.zeros((N, N)); d[0, 1] = 1.0
    for r in (1.0, 2.5, 4.0, 7.0, 10.0):
        dnu = lin.response(lin.symmetric_base(N, rho=r, **CAL), d)
        neer, dB, dC = cf.unilateral(N, rho=r, **CAL)
        assert np.allclose([dnu.mean(), dnu[0], dnu[1]], [neer, dB, dC], atol=1e-12)
    thr = N * cf.rhoD(**CAL)
    single = np.array([cf.unilateral(N, CAL["aD"], CAL["aT"], s, s)[2] for s in rhos])
    assert np.all(single < 0)
    fig, ax = plt.subplots(figsize=(style.PANEL_W, 2.5))
    ax.axvspan(thr, rhos[-1], color=SHADE, lw=0)
    style.zero_line(ax)
    style.line(ax, rhos, resp[:, 1], 1, r"$d\nu_B$ (target)")
    style.line(ax, rhos, resp[:, 2], 2, r"$d\nu_c$ (bystander)")
    style.line(ax, rhos, resp[:, 0], 3, r"$d\nu^E_A$ (NEER)")
    ax.plot(rhos, single, color=GREY, lw=1.0, ls="-", marker="x", ms=3.5, markevery=40,
            label=r"$d\nu_c$, $\rho=\eta=\sigma$ (vs. $\sigma$)")
    ax.axvline(thr, color=GREY, lw=0.6)
    ax.text(thr + 0.15, 0.04, r"$N\rho_D=%.2f$" % thr, transform=ax.get_xaxis_transform(),
            fontsize=8.5, va="bottom")
    ax.set_xlabel(r"$\rho$  ($\sigma$ for the single-elasticity line)")
    ax.set_ylabel(r"response per unit $d\tau$")
    ax.set_xlim(1, 10)
    ax.set_title(r"$N=%d$" % N)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.24), ncol=2, fontsize=8,
              handlelength=2.4, columnspacing=1.0)
    style.save(fig, "fig3%s_unilateral.pdf" % panel)
