"""Figure 5 (the paper's Figure 4, label fig:configurations): configuration
dependence, US-like parameters, N = 3.  Responses of nu_j = log e_{Aj} per unit
d tau (positive = depreciation of A): the NEER and the bystander response under
a unilateral tariff and under bilateral retaliation, and the common response
under a multilateral war.  Every series differs in line style and markers so
the figure reads in grayscale."""
import numpy as np

import style
from style import GREY, SHADE, plt
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
fig, ax = plt.subplots(figsize=(style.FULL_W, 3.3))
ax.axvspan(*RHO_BAND, color=SHADE, lw=0)
ax.text(sum(RHO_BAND) / 2, 0.98, r"central range of $\rho$", ha="center", va="top",
        transform=ax.get_xaxis_transform(), fontsize=8, color=style.MUTED)
style.zero_line(ax)
# multilateral war: wide pale band with hollow markers, drawn first so that the
# coincident bystander-under-retaliation line stays visible on top of it
ax.plot(rhos, war, color=style.AQUA, lw=4.0, alpha=0.35, solid_capstyle="butt",
        marker="o", markevery=(25, 50), ms=6, mfc="white", mec=style.AQUA, mew=1.0,
        label=r"Multilateral war: common $d\nu_j=d\nu^E_A$")
ax.plot(rhos, ret[:, 1], color=style.INK, lw=1.0, ls=(0, (1, 1.2)),
        label=r"Bilateral retaliation: bystander $d\nu_c$")
style.line(ax, rhos, ret[:, 2], 2, r"Bilateral retaliation: NEER $d\nu^E_A$")
# yellow slot, darkened so that it stays visible in grayscale, with markers
ax.plot(rhos, uni[:, 2], color="#b07800", ls=style.STYLES[4][1], marker="^",
        markevery=(10, 50), ms=4.5, label=r"Unilateral: bystander $d\nu_c$")
style.line(ax, rhos, uni[:, 0], 1, r"Unilateral: NEER $d\nu^E_A$")
for x, lab, dx, ha in ((rD, r"$\rho_D=%.2f$" % rD, 0.12, "left"),
                       (N * rD, r"$3\rho_D=%.2f$" % (N * rD), 0.12, "left")):
    ax.axvline(x, color=GREY, lw=0.7, ls=(0, (4, 2)))
    ax.text(x + dx, 0.04, lab, transform=ax.get_xaxis_transform(), fontsize=8, ha=ha)
ax.set_xlim(1, 10)
ax.set_xlabel(r"cross-origin elasticity $\rho$")
ax.set_ylabel(r"response per unit $d\tau$ ($>0$: $A$ depreciates)")
handles, labels = ax.get_legend_handles_labels()
order = [4, 3, 2, 1, 0]  # unilateral, retaliation, war
ax.legend([handles[i] for i in order], [labels[i] for i in order],
          loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=8,
          handlelength=3.2, columnspacing=1.6)
style.save(fig, "fig5_configurations.pdf")
