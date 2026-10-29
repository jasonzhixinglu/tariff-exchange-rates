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
    fig, ax = plt.subplots(figsize=(style.PANEL_W, 2.4))
    ax.axvspan(thr, rhos[-1], color=SHADE, lw=0)
    style.zero_line(ax)
    style.line(ax, rhos, resp[:, 1], 1, r"$d\nu_B$ (target)")
    style.line(ax, rhos, resp[:, 2], 2, r"$d\nu_C$ (bystander)")
    style.line(ax, rhos, resp[:, 0], 3, r"$d\nu^E_A$ (NEER)")
    ax.plot(rhos, single, color=GREY, lw=1.0, ls=(0, (1, 1.2)), label=r"$d\nu_C$, $\rho=\eta=\sigma$")
    ax.axvline(thr, color=GREY, lw=0.6)
    ax.text(thr + 0.12, 0.92, r"$N\rho_D=%.2f$" % thr, transform=ax.get_xaxis_transform(), fontsize=7.5)
    ax.set_xlabel(r"$\rho$  (single-elasticity line: $\sigma$)")
    ax.set_ylabel(r"response per unit $d\tau$")
    ax.set_xlim(1, 10)
    ax.set_title(r"$N=%d$" % N)
    if panel == "a":
        ax.legend(loc="lower right", fontsize=7)
    style.save(fig, "fig3%s_unilateral.pdf" % panel)
