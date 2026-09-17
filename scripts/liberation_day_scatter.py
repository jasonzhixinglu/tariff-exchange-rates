"""
Liberation Day event study: bilateral exchange-rate adjustment vs tariff adjustment.

Theory (Theorem, notes/model_derivations.tex).  With symmetric partners the
response of A's bilateral rates to any tariff vector splits into an average
tariff component and a relative tariff component,

    nu_j = lambda_S * tbar + lambda_D * (t_j - tbar),

so that

    NEER              = lambda_S * tbar                     (average tariff only)
    nu_j - NEER       = lambda_D * (t_j - tbar)             (relative tariff only)

Panel A plots nu_j against t_j and marks (tbar, NEER).
Panel B plots the relative response against the relative tariff, which is the
sharp test: the theory says this is a line through the origin with slope
lambda_D, and lambda_D < 0 (a partner taxed above average sees A appreciate
against it by more than the effective rate).

Event window
------------
Tariffs were announced after the US close on Wed 2 Apr 2025, so Thu 3 Apr is the
only full trading day that prices the announcement on its own.  China's 34%
counter-tariff landed before the US open on Fri 4 Apr, and the 90-day pause came
midday Wed 9 Apr.  Three windows are reported; see WINDOWS below.

Exchange-rate convention
------------------------
All rates are USD per unit of foreign currency, matching e_Aj in the model.
A positive change is a USD depreciation against that partner.

Tariff rates
------------
Reciprocal rates as ORIGINALLY announced on 2 Apr 2025 (Annex I).  Note these
differ from the 9 Apr "adjusted" annex, which raised several rates by 1pp and
escalated China to 84%, and from the August schedule.  Canada and Mexico were
exempted from the reciprocal tariffs (USMCA goods), so t = 0.

Usage: python scripts/liberation_day_scatter.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output"
OUT_DIR.mkdir(exist_ok=True)

# --------------------------------------------------------------------------
# Partners: the nine largest sources of US goods imports in 2024, treating the
# EU as a single bloc (one currency, one announced rate).  Import values come
# from data/calibration_inputs.json, which is sourced from US Census 2024.
# --------------------------------------------------------------------------
PARTNERS = [
    # key   ticker       invert  tariff_pct  label        currency
    ("EU",  "EURUSD=X",  False,  20.0,       "EU",        "EUR"),
    ("MEX", "USDMXN=X",  True,    0.0,       "Mexico",    "MXN"),
    ("CHN", "USDCNY=X",  True,   34.0,       "China",     "CNY"),
    ("CAN", "USDCAD=X",  True,    0.0,       "Canada",    "CAD"),
    ("JPN", "USDJPY=X",  True,   24.0,       "Japan",     "JPY"),
    ("VNM", "USDVND=X",  True,   46.0,       "Vietnam",   "VND"),
    ("KOR", "USDKRW=X",  True,   25.0,       "Korea",     "KRW"),
    ("TWN", "USDTWD=X",  True,   32.0,       "Taiwan",    "TWD"),
    ("IND", "USDINR=X",  True,   26.0,       "India",     "INR"),
]

# currencies that are heavily managed against the USD: flagged, not dropped
MANAGED = {"CHN", "VNM", "TWN"}

# Timeline.  Reciprocal tariffs were announced ~16:00 ET Wed 2 Apr, after the US
# close.  Thursday 3 Apr is therefore the only full trading day that prices the
# announcement alone.  China's Finance Ministry announced its 34% counter-tariff
# on all US goods before the US open on Fri 4 Apr (Dow futures were down 900pts
# by 07:10 ET), so Friday already trades on retaliation.  The 90-day pause came
# ~13:18 ET Wed 9 Apr, alongside China at 84% and the first EU countermeasures.
#
# Only the first window below is a clean unilateral-tariff experiment.  The other
# two are reported to show how quickly the cross-section is contaminated.
WINDOWS = [
    ("pre-retaliation",  "2025-04-02", "2025-04-03"),
    ("incl. China 34%",  "2025-04-02", "2025-04-04"),
    ("through 8 Apr",    "2025-04-02", "2025-04-08"),
]


def fetch_levels():
    """Daily close, USD per unit of foreign currency, for the event window."""
    tickers = [p[1] for p in PARTNERS]
    raw = yf.download(tickers, start="2025-03-20", end="2025-04-16",
                      progress=False, auto_adjust=True)["Close"]
    out = {}
    for key, ticker, invert, _, _, _ in PARTNERS:
        s = raw[ticker].dropna()
        out[key] = 1.0 / s if invert else s
    return pd.DataFrame(out)


def pct_change(levels, start, end):
    """Log change in percent between two trading-day closes."""
    idx = levels.index
    d0 = idx[idx <= pd.Timestamp(start)][-1]
    d1 = idx[idx <= pd.Timestamp(end)][-1]
    return 100.0 * np.log(levels.loc[d1] / levels.loc[d0]), d0.date(), d1.date()


def main():
    inputs = json.loads((ROOT / "data" / "calibration_inputs.json").read_text())
    us_imports = inputs["goods_imports_2024"]["USA"]

    keys = [p[0] for p in PARTNERS]
    tariff = pd.Series({p[0]: p[3] for p in PARTNERS})
    label = {p[0]: p[4] for p in PARTNERS}

    imports = pd.Series({k: us_imports[k] for k in keys}, dtype=float)
    weight = imports / imports.sum()

    levels = fetch_levels()

    tbar = float((weight * tariff).sum())
    wv = weight[keys].values
    tv = tariff[keys].values

    rows = []
    for name, s, e in WINDOWS:
        nu, d0, d1 = pct_change(levels, s, e)
        nu = nu[keys]
        neer = float((weight * nu).sum())
        y = nu.values

        # weighted OLS of nu on t.  The weighted fit passes through (tbar, NEER)
        # mechanically, so that is not the test; the content of the theory is that
        # the relation is linear and that the slope lambda_D is negative.
        X = np.column_stack([np.ones(len(keys)), tv])
        beta = np.linalg.solve(X.T @ (wv[:, None] * X), X.T @ (wv * y))
        resid = y - X @ beta
        r2 = 1 - (wv * resid ** 2).sum() / (wv * (y - neer) ** 2).sum()

        rel_t, rel_e = tv - tbar, y - neer
        b_rel = float((wv * rel_t * rel_e).sum() / (wv * rel_t ** 2).sum())

        rows.append(dict(name=name, nu=nu, neer=neer, beta=beta, r2=r2,
                         rel_t=rel_t, rel_e=rel_e, b_rel=b_rel, d0=d0, d1=d1))

    print(f"trade-weighted average announced tariff: {tbar:.1f}pp")
    print("theory predicts a NEGATIVE slope (lambda_D < 0)\n")
    for r in rows:
        print(f"--- {r['name']}: {r['d0']} -> {r['d1']}")
        print(f"    NEER {r['neer']:+.2f}%   slope {r['beta'][1]:+.4f} %/pp   "
              f"weighted R^2 {r['r2']:.3f}")
        print(f"    {'':<9}{'tariff':>7}{'d log e':>9}{'rel t':>7}{'rel e':>7}{'wt':>7}")
        for k in sorted(keys, key=lambda k: tariff[k]):
            flag = "*" if k in MANAGED else " "
            print(f"    {label[k]:<8}{flag}{tariff[k]:>7.0f}{r['nu'][k]:>9.2f}"
                  f"{tariff[k]-tbar:>7.1f}{r['nu'][k]-r['neer']:>7.2f}{weight[k]:>7.3f}")
        print()
    print("* heavily managed against the USD")

    # The three managed currencies also carry three of the four highest tariffs,
    # so they can generate a negative slope mechanically: they were tariffed most
    # and, being managed, moved least.  Re-fit on the freely floating partners.
    free = [k for k in keys if k not in MANAGED]
    fw = np.array([weight[k] for k in free]); fw = fw / fw.sum()
    ft = np.array([tariff[k] for k in free], dtype=float)
    Xf = np.column_stack([np.ones(len(free)), ft])
    print("\nrobustness: freely floating partners only "
          f"({', '.join(label[k] for k in free)})")
    for r in rows:
        fy = np.array([r["nu"][k] for k in free], dtype=float)
        bf = np.linalg.solve(Xf.T @ (fw[:, None] * Xf), Xf.T @ (fw * fy))
        nf = float((fw * fy).sum())
        rf = fy - Xf @ bf
        r2f = 1 - (fw * rf ** 2).sum() / (fw * (fy - nf) ** 2).sum()
        print(f"    {r['name']:<16} n={len(free)}  tbar {(fw*ft).sum():4.1f}pp  "
              f"NEER {nf:+.2f}%  slope {bf[1]:+.4f} %/pp  R^2 {r2f:.3f}")

    # ---------------------------------------------------------------- figure
    fig, axes = plt.subplots(len(WINDOWS), 2, figsize=(12.6, 5.2 * len(WINDOWS)))
    LETTERS = "ABCDEFGH"

    for row, r in enumerate(rows):
        nu, neer, beta = r["nu"], r["neer"], r["beta"]

        ax = axes[row][0]
        for k in keys:
            c = "#b45309" if k in MANAGED else "#1d4ed8"
            ax.scatter(tariff[k], nu[k], s=110 + 1300 * weight[k], alpha=.55,
                       color=c, edgecolor="white", linewidth=1.2, zorder=3)
            ax.annotate(label[k], (tariff[k], nu[k]), textcoords="offset points",
                        xytext=(0, 12), ha="center", fontsize=8.5, color="#334155")
        xs = np.linspace(-4, 51, 50)
        ax.plot(xs, beta[0] + beta[1] * xs, color="#1d4ed8", lw=1.6, alpha=.85,
                label=f"weighted fit, slope {beta[1]:+.3f} %/pp  ($R^2$ {r['r2']:.2f})")
        ax.scatter([tbar], [neer], marker="*", s=480, color="#dc2626", zorder=5,
                   edgecolor="white", linewidth=1.1,
                   label=f"$(\\bar t={tbar:.0f}$pp, NEER ${neer:+.2f}$%)")
        ax.axhline(neer, color="#dc2626", lw=.8, ls=":", alpha=.7)
        ax.axvline(tbar, color="#dc2626", lw=.8, ls=":", alpha=.7)
        ax.set_xlabel("announced reciprocal tariff, percentage points")
        ax.set_ylabel("USD per foreign currency, % change\n(positive = USD depreciation)")
        ax.set_title(f"{LETTERS[2*row]}.  Level, {r['name']} "
                     f"({r['d0']} to {r['d1']})", loc="left", fontsize=10.5)
        ax.legend(fontsize=8, loc="best", framealpha=.9)

        ax = axes[row][1]
        for i, k in enumerate(keys):
            c = "#b45309" if k in MANAGED else "#059669"
            ax.scatter(r["rel_t"][i], r["rel_e"][i], s=110 + 1300 * weight[k],
                       alpha=.55, color=c, edgecolor="white", linewidth=1.2, zorder=3)
            ax.annotate(label[k], (r["rel_t"][i], r["rel_e"][i]),
                        textcoords="offset points", xytext=(0, 12), ha="center",
                        fontsize=8.5, color="#334155")
        xs = np.linspace(r["rel_t"].min() - 4, r["rel_t"].max() + 5, 50)
        ax.plot(xs, r["b_rel"] * xs, color="#059669", lw=1.6, alpha=.85,
                label=f"through origin, slope {r['b_rel']:+.3f} %/pp")
        ax.axvline(0, color="#94a3b8", lw=.8)
        ax.set_xlabel(r"relative tariff  $t_j-\bar t$,  percentage points")
        ax.set_ylabel(r"relative response  $\nu_j-$NEER,  %")
        ax.set_title(f"{LETTERS[2*row+1]}.  Discrimination channel, {r['name']}",
                     loc="left", fontsize=10.5)
        ax.legend(fontsize=8, loc="best", framealpha=.9)

    for ax in axes.ravel():
        ax.axhline(0, color="#94a3b8", lw=.8)
        ax.grid(alpha=.25, lw=.6)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    fig.suptitle("Liberation Day tariffs and the dollar: nine largest US "
                 "goods-import sources, EU as a bloc\n"
                 "tariffs as announced 2 Apr 2025; theory predicts a negative slope",
                 fontsize=12.5, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    path = OUT_DIR / "liberation_day_scatter.pdf"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=150, bbox_inches="tight")
    print(f"\nwrote {path} and .png")


if __name__ == "__main__":
    main()
