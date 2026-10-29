"""Figure 4: configuration dependence, US-like parameters, N = 3.
NEER under unilateral tariff, bilateral retaliation and multilateral war, and
the bystander response under unilateral tariff and retaliation."""
import numpy as np

import style
from style import GREY, SHADE, plt
from model import closed_forms as cf
from model import linear as lin

N, CAL = 3, cf.US_LIKE
rhos = np.linspace(1.0, 10.0, 451)
uni = np.array([cf.unilateral(N, rho=r, **CAL) for r in rhos])
ret = np.array([cf.retaliation(N, rho=r, **CAL) for r in rhos])
war = np.array([cf.multilateral_war(N, rho=r, **CAL) for r in rhos])

# cross-checks against the linear solver
for r in (1.2, 3.0, 6.0):
    b = lin.symmetric_base(N, rho=r, **CAL)
    dr = np.zeros((3, 3)); dr[0, 1] = dr[1, 0] = 1
    dw = np.zeros((3, 3)); dw[0, 1:] = 1; dw[1:, 0] = 1
    assert np.allclose(lin.response(b, dr), [0.0, cf.retaliation(N, rho=r, **CAL)[1]], atol=1e-12)
    assert np.allclose(lin.response(b, dw), cf.multilateral_war(N, rho=r, **CAL), atol=1e-12)
# at N = 3 the multilateral-war response coincides with the bystander response
# under bilateral retaliation
assert np.allclose(war, ret[:, 1])

rD = cf.rhoD(**CAL)
fig, ax = plt.subplots(figsize=(style.FULL_W * 0.78, 3.0))
ax.axvspan(2.0, 4.0, color=SHADE, lw=0)
ax.text(3.0, 0.97, "central empirical range\nfor cross-origin elasticities", ha="center", va="top",
        transform=ax.get_xaxis_transform(), fontsize=7, color=style.MUTED)
style.zero_line(ax)
style.line(ax, rhos, uni[:, 0], 1, r"NEER, unilateral")
style.line(ax, rhos, ret[:, 2], 2, r"NEER, bilateral retaliation")
style.line(ax, rhos, war, 3, r"NEER, multilateral war $=$ bystander, retaliation", lw=2.6, alpha=0.55)
style.line(ax, rhos, uni[:, 2], 4, r"bystander $d\nu_C$, unilateral")
ax.plot(rhos, ret[:, 1], color=style.INK, lw=0.9, ls=(0, (1, 1.5)), label=r"bystander $d\nu_C$, retaliation")
for x, lab in ((rD, r"$\rho_D=%.2f$" % rD), (3 * rD, r"$3\rho_D=%.2f$" % (3 * rD))):
    ax.axvline(x, color=GREY, lw=0.6)
    ax.text(x + 0.1, 0.06, lab, transform=ax.get_xaxis_transform(), fontsize=7.5)
ax.set_xlim(1, 10)
ax.set_xlabel(r"$\rho$"); ax.set_ylabel(r"response per unit $d\tau$")
ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=7)
style.save(fig, "fig4_configurations.pdf")
