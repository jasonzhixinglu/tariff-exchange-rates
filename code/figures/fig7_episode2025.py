"""Figure 7: the 2025 episode (stylized; no model magnitudes).

(a) Monthly-average USD/EUR, USD/CNY, USD/VND and the Fed H.10 broad dollar
    index excluding China, % deviation from the 2024 average; positive = dollar
    depreciation.  Data cached by code/data/fetch_fx_2025.py.
(b) Headline incremental tariff rates (pp above the pre-2025 baseline): US on
    China, China on US (across the board), US on EU, US baseline on others.
Phases: unilateral (US tariffs on China, Feb 4 - Apr 4), retaliation (from the
universal baseline and China's counter-tariffs, Apr 5 - May 13), near-uniform
(framework rates in force from Aug 7; the Nov 10 cut on China completes it)."""
import os
from datetime import date

import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import style
from style import GREY, plt

FX = os.path.join(style.ROOT, "data", "processed", "fx2025_monthly.csv")
TAR = os.path.join(style.ROOT, "data", "raw", "tariffs2025", "tariff_timeline.csv")
START, END = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31")
PHASES = [(pd.Timestamp("2025-02-04"), pd.Timestamp("2025-04-04"), "unilateral"),
          (pd.Timestamp("2025-04-05"), pd.Timestamp("2025-05-13"), "retaliation"),
          (pd.Timestamp("2025-08-07"), END, "near-uniform")]
SHADES = ["#eeeeee", "#dcdcdc", "#eeeeee"]
SIZE = (style.FULL_W, 2.35)
MARGINS = dict(left=0.09, right=0.80, top=0.93, bottom=0.14)


def shade(ax, label=False):
    for (a, b, lab), c in zip(PHASES, SHADES):
        ax.axvspan(a, b, color=c, lw=0, zorder=0)
        if label:
            ax.text(a + (b - a) / 2, 1.0, lab, transform=ax.get_xaxis_transform(), ha="center",
                    va="bottom", fontsize=7, color=style.MUTED)


def finish(ax):
    ax.set_xlim(START, END)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))


# ------------------------------------------------------------------ (a)
fx = pd.read_csv(FX)
fx["date"] = pd.to_datetime(fx["month"] + "-15")
fx = fx[(fx["date"] >= START) & (fx["date"] <= END)]
assert len(fx) == 12, "expected 12 months of 2025 data"
fig = plt.figure(figsize=SIZE)
fig.subplots_adjust(**MARGINS)
ax = fig.add_subplot()
shade(ax, label=True)
ax.axhline(0, color=style.MUTED, lw=0.6)
series = [("dev_usd_per_eur", 1, "USD/EUR"), ("dev_usd_per_cny", 2, "USD/CNY"),
          ("dev_usd_per_vnd", 3, "USD/VND"), ("dev_broad_exCN_index", 4, "Broad index ex. China")]
for col, slot, lab in series:
    style.line(ax, fx["date"], fx[col], slot, lab, marker="o", ms=2.5)
ax.set_ylabel("% vs 2024 average\n(+ = dollar depreciation)", fontsize=8)
finish(ax)
ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7)
style.os.makedirs(style.OUT, exist_ok=True)
fig.savefig(os.path.join(style.OUT, "fig7a_fx2025.pdf"), bbox_inches=None)
plt.close(fig)
print("wrote paper/figures/fig7a_fx2025.pdf")

# ------------------------------------------------------------------ (b)
tar = pd.read_csv(TAR, parse_dates=["effective_date"])


def steps(name):
    s = tar[tar["series"] == name].sort_values("effective_date")
    x = list(s["effective_date"]) + [END]
    y = list(s["rate_pp"]) + [s["rate_pp"].iloc[-1]]
    return x, y


fig = plt.figure(figsize=SIZE)
fig.subplots_adjust(**MARGINS)
ax = fig.add_subplot()
shade(ax)
for (name, slot, lab) in (("us_on_china", 1, "US on China"), ("china_on_us", 2, "China on US"),
                          ("us_on_eu", 3, "US on EU"), ("us_on_others", 4, "US on others (baseline)")):
    x, y = steps(name)
    color, dash = style.STYLES[slot]
    ax.step(x, y, where="post", color=color, linestyle=dash, label=lab, lw=1.5)
ax.set_ylabel("tariff increase (pp)", fontsize=8)
ax.set_ylim(0, 155)
finish(ax)
ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7)
fig.savefig(os.path.join(style.OUT, "fig7b_tariffs2025.pdf"), bbox_inches=None)
plt.close(fig)
print("wrote paper/figures/fig7b_tariffs2025.pdf")
