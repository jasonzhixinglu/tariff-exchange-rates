"""Figure 1: bilateral tariff and exchange-rate adjustment (schematic, no data)."""
import numpy as np

import style
from style import BLUE, INK, MUTED, ORANGE, plt

fig, ax = plt.subplots(figsize=(4.2, 2.9))
slope, shift = 1.0, 0.6          # TB_{A nu} > 0 and TB_{A tau} d tau > 0 (illustrative)
x = np.linspace(-1.2, 1.0, 50)
ax.axhline(0, color=MUTED, lw=0.6)
ax.axvline(0, color=MUTED, lw=0.6)
ax.plot(x, slope * x, color=BLUE, label="Marshall–Lerner")
ax.plot(x, slope * x + shift, color=ORANGE, linestyle=(0, (5, 2)),
        label="tariff at unchanged exchange rates")
xs = -shift / slope
ax.plot([xs], [0], "o", color=INK, ms=4)
ax.annotate(r"$d\nu^*=-\,TB_{A\tau}\,d\tau/TB_{A\nu}<0$", xy=(xs, 0), xytext=(-1.15, -0.75),
            fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.6, color=INK))
ax.annotate("", xy=(0.55, 0.55 + shift), xytext=(0.55, 0.55),
            arrowprops=dict(arrowstyle="->", lw=0.8, color=INK))
ax.text(0.6, 0.55 + shift / 2, r"$TB_{A\tau}\,d\tau$", fontsize=8, va="center")
ax.text(0.62, 0.30, r"slope $TB_{A\nu}>0$", fontsize=8, color=BLUE)
ax.set_xlabel(r"$d\nu$  (rise = depreciation of $A$)")
ax.set_ylabel(r"$dTB_A$")
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-1.25, 1.05); ax.set_ylim(-1.0, 1.6)
ax.legend(loc="upper left")
style.save(fig, "fig1_bilateral.pdf")
