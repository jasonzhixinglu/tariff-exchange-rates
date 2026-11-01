"""Figure 5 (the paper's Figure 4, label fig:configurations): configuration
dependence, US-like parameters, N = 3.  Responses of nu_j = log e_{Aj} per unit
d tau (positive = depreciation of A): the NEER and the bystander response under
(a) a unilateral tariff and (b) bilateral retaliation.  The multilateral-war
response is computed and cross-checked but not plotted (at N = 3 it equals the
bystander response under bilateral retaliation)."""
import numpy as np

import style
from style import BLUE, GREY, MUTED, ORANGE, SHADE, plt
from model import closed_forms as cf
from model import linear as lin

N, CAL = 3, cf.US_LIKE
RHO_BAND = (2.0, 4.0)  # central range of cross-origin elasticities (see text)
rhos = np.linspace(1.0, 10.0, 451)
uni = np.array([cf.unilateral(N, rho=r, **CAL) for r in rhos])
ret = np.array([cf.retaliation(N, rho=r, **CAL) for r in rhos])
war = np.array([cf.multilateral_war(N, rho=r, **CAL) for r in rhos])

# cross-checks against the linear solver
for r in (1.2, 3.0, 6.0):
    b = lin.symmetric_base(N, rho=r, **CAL)
    du = np.zeros((3, 3)); du[0, 1] = 1
    dr = np.zeros((3, 3)); dr[0, 1] = dr[1, 0] = 1
    dw = np.zeros((3, 3)); dw[0, 1:] = 1; dw[1:, 0] = 1
    u = cf.unilateral(N, rho=r, **CAL)
    assert np.allclose(lin.response(b, du), [u[1], u[2]], atol=1e-12)
    assert np.allclose(lin.response(b, dr), [0.0, cf.retaliation(N, rho=r, **CAL)[1]], atol=1e-12)
    assert np.allclose(lin.response(b, dw), cf.multilateral_war(N, rho=r, **CAL), atol=1e-12)
# at N = 3 the multilateral-war response coincides with the bystander response
# under bilateral retaliation, and the retaliation NEER is half of it
assert np.allclose(war, ret[:, 1])
assert np.allclose(ret[:, 2], 0.5 * ret[:, 1])

rD = cf.rhoD(**CAL)
LW = 1.6
panels = (("(a) Unilateral tariff", uni[:, 0], uni[:, 2], N * rD, r"$3\rho_D=%.2f$" % (N * rD)),
          ("(b) Bilateral retaliation", ret[:, 2], ret[:, 1], rD, r"$\rho_D=%.2f$" % rD))
fig, axes = plt.subplots(1, 2, figsize=(style.FULL_W, 2.9), sharey=True)
for k, (ax, (title, neer, bys, thr, lab)) in enumerate(zip(axes, panels)):
    ax.axvspan(*RHO_BAND, color=SHADE, lw=0, zorder=0)
    style.zero_line(ax)
    ax.plot(rhos, neer, color=BLUE, lw=LW, ls="-", label="NEER")
    ax.plot(rhos, bys, color=ORANGE, lw=LW, ls=(0, (5, 2)), label="Bystander")
    ax.axvline(thr, color=GREY, lw=0.7, ls=(0, (1, 1.5)))
    ax.text(thr + 0.15, 0.04, lab, transform=ax.get_xaxis_transform(), fontsize=8, ha="left")
    if k == 1:
        ax.text(sum(RHO_BAND) / 2, 0.98, "Central\n" r"range of $\rho$", ha="center", va="top",
                transform=ax.get_xaxis_transform(), fontsize=7.5, color=MUTED, linespacing=1.1)
    ax.set_title(title)
    ax.set_xlim(1, 10)
    ax.set_ylim(-0.5, 0.8)
    ax.set_xticks([2, 4, 6, 8, 10])
    ax.set_xlabel(r"Cross-origin elasticity, $\rho$")
axes[0].set_ylabel(r"Response per unit $d\tau$ ($>0$: $A$ depreciates)")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=2,
           handlelength=3.0, columnspacing=2.0)
fig.subplots_adjust(wspace=0.12, bottom=0.22)
style.save(fig, "fig5_configurations.pdf")
