"""
Wide cross-section: exchange-rate response to the Liberation Day tariff vector.

The nine-partner version (scripts/liberation_day_scatter.py) has too few points to
say anything about lambda_D once the clean one-day window is imposed.  This script
trades the NEER anchor for cross-sectional power: every country we can price, on
the one trading day that is uncontaminated by retaliation.

Theory.  nu_j = lambda_S * tbar + lambda_D * (t_j - tbar), so in a cross-section
of partners the response should fall linearly in the partner's own tariff, with
slope lambda_D < 0.  The level (lambda_S * tbar) is absorbed by the intercept, so
an unweighted cross-sectional regression identifies lambda_D without needing
trade weights.  That is the whole content of the test here.

Window.  Close 2 Apr 2025 (tariffs announced ~16:00 ET, after the close) to close
3 Apr 2025.  China's counter-tariff landed before the US open on 4 Apr, so this is
the only session that prices the announcement alone.

Tariffs.  Executive Order 14257 Annex I as signed 2 Apr 2025 (Federal Register
vol. 90 no. 65, 2025-06063): 57 countries with country-specific rates.  Canada and
Mexico were exempt via USMCA (0).  Every other country got the 10% baseline.
These are the ORIGINAL rates, not the 9 Apr revision that raised several by 1pp
and took China to 84%.

Exchange rates.  USD per unit of foreign currency, matching e_Aj, so a positive
change is a USD depreciation against that partner.

Currency regime is the key control: a pegged currency cannot respond, so pegs
clustered at high tariffs would deliver a negative slope with no adjustment
mechanism behind it.  Regimes are declared below and cross-checked against
realised volatility in March 2025.

Usage: python scripts/liberation_day_cross_section.py
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

D0, D1 = "2025-04-02", "2025-04-03"
VOL_START, VOL_END = "2025-03-03", "2025-04-01"   # pre-event volatility screen
VOL_FLOOR = 0.10                                   # % daily sd; below this = inert

# name, ticker, invert(USD/foreign needs 1/x), tariff, regime
# regime: float | managed | peg
COUNTRIES = [
    ("Euro area",     "EURUSD=X", False, 20, "float"),
    ("Japan",         "USDJPY=X", True,  24, "float"),
    ("United Kingdom","GBPUSD=X", False, 10, "float"),
    ("Switzerland",   "USDCHF=X", True,  31, "float"),
    ("Canada",        "USDCAD=X", True,   0, "float"),
    ("Mexico",        "USDMXN=X", True,   0, "float"),
    ("Australia",     "AUDUSD=X", False, 10, "float"),
    ("New Zealand",   "NZDUSD=X", False, 10, "float"),
    ("Sweden",        "USDSEK=X", True,  20, "float"),
    ("Norway",        "USDNOK=X", True,  15, "float"),
    ("Poland",        "USDPLN=X", True,  20, "float"),
    ("Hungary",       "USDHUF=X", True,  20, "float"),
    ("Czechia",       "USDCZK=X", True,  20, "float"),
    ("Romania",       "USDRON=X", True,  20, "float"),
    ("Iceland",       "USDISK=X", True,  10, "float"),
    ("Turkey",        "USDTRY=X", True,  10, "float"),
    ("Israel",        "USDILS=X", True,  17, "float"),
    ("South Africa",  "USDZAR=X", True,  30, "float"),
    ("Brazil",        "USDBRL=X", True,  10, "float"),
    ("Chile",         "USDCLP=X", True,  10, "float"),
    ("Colombia",      "USDCOP=X", True,  10, "float"),
    ("Peru",          "USDPEN=X", True,  10, "float"),
    ("Uruguay",       "USDUYU=X", True,  10, "float"),
    ("South Korea",   "USDKRW=X", True,  25, "float"),
    ("India",         "USDINR=X", True,  26, "float"),
    ("Indonesia",     "USDIDR=X", True,  32, "float"),
    ("Thailand",      "USDTHB=X", True,  36, "float"),
    ("Philippines",   "USDPHP=X", True,  17, "float"),
    ("Malaysia",      "USDMYR=X", True,  24, "float"),
    ("Sri Lanka",     "USDLKR=X", True,  44, "float"),
    ("Pakistan",      "USDPKR=X", True,  29, "float"),
    ("Bangladesh",    "USDBDT=X", True,  37, "float"),
    ("Kazakhstan",    "USDKZT=X", True,  27, "float"),
    ("Nigeria",       "USDNGN=X", True,  14, "float"),
    ("Egypt",         "USDEGP=X", True,  10, "float"),
    ("Kenya",         "USDKES=X", True,  10, "float"),
    ("Ghana",         "USDGHS=X", True,  10, "float"),
    ("Zambia",        "USDZMW=X", True,  17, "float"),
    ("Mauritius",     "USDMUR=X", True,  40, "float"),
    ("Tunisia",       "USDTND=X", True,  28, "float"),
    ("Moldova",       "USDMDL=X", True,  31, "float"),
    ("Ukraine",       "USDUAH=X", True,  10, "float"),
    ("Dominican Rep", "USDDOP=X", True,  10, "float"),
    ("Costa Rica",    "USDCRC=X", True,  10, "float"),
    ("Guatemala",     "USDGTQ=X", True,  10, "float"),
    ("Jamaica",       "USDJMD=X", True,  10, "float"),
    # managed floats and bands
    ("China",         "USDCNY=X", True,  34, "managed"),
    ("Taiwan",        "USDTWD=X", True,  32, "managed"),
    ("Singapore",     "USDSGD=X", True,  10, "managed"),
    ("Vietnam",       "USDVND=X", True,  46, "managed"),
    ("Argentina",     "USDARS=X", True,  10, "managed"),
    # hard pegs: cannot respond by construction
    ("Hong Kong",     "USDHKD=X", True,  34, "peg"),
    ("Saudi Arabia",  "USDSAR=X", True,  10, "peg"),
    ("UAE",           "USDAED=X", True,  10, "peg"),
    ("Qatar",         "USDQAR=X", True,  10, "peg"),
    ("Jordan",        "USDJOD=X", True,  20, "peg"),
    ("Bahrain",       "USDBHD=X", True,  10, "peg"),
    ("Oman",          "USDOMR=X", True,  10, "peg"),
    ("Bulgaria",      "USDBGN=X", True,  20, "peg"),
    ("Denmark",       "USDDKK=X", True,  20, "peg"),
    ("Brunei",        "USDBND=X", True,  24, "peg"),
    ("Cambodia",      "USDKHR=X", True,  49, "peg"),
]

REGIME_COLOR = {"float": "#1d4ed8", "managed": "#b45309", "peg": "#94a3b8"}

# Advanced economies (IMF definition, plus EU members), used as the control for
# the risk-off composition effect described above the regression block in main().
ADVANCED = {
    "Euro area", "Japan", "United Kingdom", "Switzerland", "Canada", "Australia",
    "New Zealand", "Sweden", "Norway", "Denmark", "Iceland", "Israel",
    "South Korea", "Czechia", "Poland", "Hungary", "Romania", "Singapore",
    "Taiwan", "Hong Kong",
}


def fetch():
    tickers = sorted({c[1] for c in COUNTRIES})
    raw = yf.download(tickers, start="2025-02-20", end="2025-04-11",
                      progress=False, auto_adjust=True)["Close"]
    return raw


def wls(t, y, w=None):
    """Return slope, intercept, R^2 for a (weighted) linear fit."""
    w = np.ones_like(t) if w is None else np.asarray(w, dtype=float)
    w = w / w.sum()
    X = np.column_stack([np.ones(len(t)), t])
    b = np.linalg.solve(X.T @ (w[:, None] * X), X.T @ (w * y))
    r = y - X @ b
    ybar = (w * y).sum()
    return b[1], b[0], 1 - (w * r ** 2).sum() / (w * (y - ybar) ** 2).sum()


def ols(d, cols):
    """Multivariate OLS on the frame; returns coefficients, t-stats and R^2."""
    y = d["nu"].values
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    n, k = X.shape
    se = np.sqrt(np.diag((r ** 2).sum() / (n - k) * np.linalg.inv(X.T @ X)))
    r2 = 1 - (r ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return b[1:], b[1:] / se[1:], r2


def main():
    raw = fetch()
    rows, dropped = [], []

    for name, ticker, invert, tar, regime in COUNTRIES:
        if ticker not in raw.columns:
            dropped.append((name, "no ticker"))
            continue
        s = raw[ticker].dropna()
        if invert:
            s = 1.0 / s
        idx = s.index
        pre = idx[idx <= pd.Timestamp(D0)]
        post = idx[idx <= pd.Timestamp(D1)]
        if len(pre) == 0 or len(post) == 0 or pre[-1] == post[-1]:
            dropped.append((name, "no quote in window"))
            continue

        vol_slice = s.loc[VOL_START:VOL_END]
        vol = 100.0 * np.log(vol_slice).diff().std() if len(vol_slice) > 5 else np.nan
        nu = 100.0 * np.log(s.loc[post[-1]] / s.loc[pre[-1]])
        rows.append(dict(name=name, tariff=float(tar), nu=float(nu),
                         regime=regime, vol=float(vol) if vol == vol else np.nan))

    df = pd.DataFrame(rows).sort_values("tariff").reset_index(drop=True)

    # A currency whose pre-event daily sd is below the floor cannot express a
    # response, whatever its declared regime.  Flag those as inert.
    df["inert"] = ~(df["vol"] > VOL_FLOOR)
    df["live_float"] = (df["regime"] == "float") & ~df["inert"]
    df["ae"] = df["name"].isin(ADVANCED).astype(float)

    print(f"window {D0} -> {D1};  {len(df)} countries priced, "
          f"{len(dropped)} dropped")
    for n, why in dropped:
        print(f"    dropped {n}: {why}")

    print(f"\n{'country':<16}{'tariff':>7}{'d log e':>9}{'vol':>7}  regime")
    for _, r in df.iterrows():
        tag = r["regime"] + (" (inert)" if r["inert"] else "")
        print(f"{r['name']:<16}{r['tariff']:>7.0f}{r['nu']:>9.2f}"
              f"{r['vol']:>7.2f}  {tag}")

    samples = [
        ("all priced",              df),
        ("declared floats",         df[df["regime"] == "float"]),
        ("live floats (vol screen)", df[df["live_float"]]),
        ("live floats, Annex I only", df[df["live_float"] & (df["tariff"] > 10)]),
    ]
    print(f"\n{'sample':<28}{'n':>4}{'slope':>9}{'R^2':>7}{'mean t':>8}{'mean e':>8}")
    print("theory: slope < 0")
    fits = {}
    for nm, d in samples:
        if len(d) < 3:
            continue
        sl, ic, r2 = wls(d["tariff"].values, d["nu"].values)
        fits[nm] = (sl, ic, r2, len(d))
        print(f"{nm:<28}{len(d):>4}{sl:>+9.4f}{r2:>7.3f}"
              f"{d['tariff'].mean():>8.1f}{d['nu'].mean():>+8.2f}")

    # The reciprocal formula handed emerging markets higher rates on average, and
    # 3 Apr was a risk-off session in which the dollar fell against the major
    # funding and reserve currencies whatever their tariff.  Those two facts are
    # collinear, so a negative slope only means something if it survives the split.
    fl = df[df["live_float"]]
    checks = [
        ("live floats", fl),
        ("live floats, ex South Africa", fl[fl["name"] != "South Africa"]),
        ("Annex I only (t>10)", fl[fl["tariff"] > 10]),
        ("Annex I, ex South Africa",
         fl[(fl["tariff"] > 10) & (fl["name"] != "South Africa")]),
    ]
    print("\ncontrolling for the advanced/emerging split   [coefficient (t-stat)]")
    print(f"{'sample':<30}{'n':>4}{'tariff only':>17}{'tariff | AE':>17}"
          f"{'AE dummy':>17}{'R^2':>7}")
    for nm, d in checks:
        (s1,), (t1,), _ = ols(d, ["tariff"])
        (s2, a2), (t2, ta2), r2 = ols(d, ["tariff", "ae"])
        print(f"{nm:<30}{len(d):>4}{f'{s1:+.4f} ({t1:+.2f})':>17}"
              f"{f'{s2:+.4f} ({t2:+.2f})':>17}"
              f"{f'{a2:+.3f} ({ta2:+.2f})':>17}{r2:>7.3f}")
    print("South Africa is shown excluded because the rand was selling off on the")
    print("domestic budget and coalition crisis, unrelated to tariffs.")

    # ------------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.8))

    ax = axes[0]
    for regime, g in df.groupby("regime"):
        ax.scatter(g["tariff"], g["nu"], s=46, alpha=.75,
                   color=REGIME_COLOR[regime], edgecolor="white", linewidth=.8,
                   label=f"{regime} (n={len(g)})", zorder=3)
    sl, ic, r2, n = fits["all priced"]
    xs = np.linspace(-2, 52, 50)
    ax.plot(xs, ic + sl * xs, color="#334155", lw=1.5, alpha=.8,
            label=f"all: slope {sl:+.3f}, $R^2$ {r2:.2f}")
    ax.set_title(f"A.  Every currency priced (n={len(df)})", loc="left", fontsize=11)
    ax.legend(fontsize=8, loc="upper left", framealpha=.9)

    ax = axes[1]
    d = df[df["live_float"]]
    for is_ae, col, lab in [(1.0, "#0f766e", "advanced"), (0.0, "#be123c", "emerging")]:
        g = d[d["ae"] == is_ae]
        ax.scatter(g["tariff"], g["nu"], s=54, alpha=.8, color=col,
                   edgecolor="white", linewidth=.8, zorder=3,
                   label=f"{lab}: n={len(g)}, mean {g['nu'].mean():+.2f}%")
        sl_g, ic_g, _ = wls(g["tariff"].values, g["nu"].values)
        ax.plot(xs, ic_g + sl_g * xs, color=col, lw=1.3, ls="--", alpha=.75)
    for _, r in d.iterrows():
        if r["tariff"] > 10 or abs(r["nu"]) > 0.9:
            ax.annotate(r["name"], (r["tariff"], r["nu"]),
                        textcoords="offset points", xytext=(0, 9), ha="center",
                        fontsize=7.5, color="#334155")
    sl, ic, r2, n = fits["live floats (vol screen)"]
    ax.plot(xs, ic + sl * xs, color="#334155", lw=1.6, alpha=.85,
            label=f"pooled: slope {sl:+.3f} %/pp, $R^2$ {r2:.2f}, n={n}")
    ax.set_title("B.  Floating currencies, split by advanced vs emerging",
                 loc="left", fontsize=11)
    ax.legend(fontsize=8, loc="upper left", framealpha=.9)

    for ax in axes:
        ax.axhline(0, color="#94a3b8", lw=.8)
        ax.grid(alpha=.25, lw=.6)
        ax.set_axisbelow(True)
        ax.set_xlabel("announced reciprocal tariff, percentage points")
        ax.set_ylabel("USD per foreign currency, % change\n(positive = USD depreciation)")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)

    fig.suptitle("Cross-section of exchange-rate responses to the Liberation Day "
                 f"tariff vector, {D0} to {D1}\n"
                 "EO 14257 Annex I rates as signed 2 Apr 2025; "
                 "theory predicts a negative slope",
                 fontsize=12.5, y=1.0)
    fig.tight_layout()
    path = OUT_DIR / "liberation_day_cross_section.pdf"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=160, bbox_inches="tight")
    df.to_csv(OUT_DIR / "liberation_day_cross_section.csv", index=False)
    print(f"\nwrote {path}, .png and .csv")


if __name__ == "__main__":
    main()
