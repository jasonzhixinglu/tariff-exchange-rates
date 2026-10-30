"""
Long-horizon test: exchange rates against the tariff schedule that actually stuck.

lambda_D in the model is a post-adjustment equilibrium object.  nu = (-J)^{-1}F,
where F is the trade-balance effect at unchanged exchange rates and (-J)^{-1} is
the adjustment that restores TB_i = 0; the model pins down where the system
converges, not how fast (MML is equivalent to stability of the tatonnement
d nu_i/dt = k_i TB_i, and the k_i are free).  A one-day announcement window is
therefore the wrong horizon, which is what the 3 Apr cross-section showed.

This script uses the settled schedule instead:

  tariff   the IEEPA rate in force from 7 Aug 2025 (EO 14326 Annex I), which held
           stable until the Swiss cut on 14 Nov, plus the country-specific add-ons
           in force over the same period (India +25 Russian-oil penalty from
           27 Aug; Brazil +40 from 6 Aug).
  response monthly-average USD per foreign currency, March 2025 (pre-announcement)
           to October 2025.  Monthly averages, not closes: a comparative-statics
           prediction should not be read off a single day.

Caveats that cannot be designed away, and which the user flagged up front:
  - By October most partners had retaliated or negotiated, so the tariff vector is
    an equilibrium outcome, not an exogenous shock.  This is a correlation at the
    right horizon, not a clean experiment.
  - Canada and Mexico keep USMCA duty-free treatment for the compliant majority of
    trade, so their headline 35/25 non-USMCA rates badly overstate the applied
    rate.  They are held at their effective rate and flagged.
  - China sits on a separate truce track (reciprocal cut to 10 plus a 20 fentanyl
    tranche) and its currency is managed, so it is reported but excluded.

Usage: python scripts/settled_schedule_cross_section.py
"""

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

BASE_MONTH, END_MONTH = "2025-03", "2025-10"
VOL_FLOOR = 0.10

# name, ticker, invert, settled tariff, regime, note
# Rates: EO 14326 Annex I (7 Aug 2025).  Countries absent from Annex I take the
# 10% baseline.  EU members take the EU rate.  Flagged exceptions carry a note.
COUNTRIES = [
    ("Euro area",     "EURUSD=X", False, 15, "float", ""),
    ("Japan",         "USDJPY=X", True,  15, "float", ""),
    ("United Kingdom","GBPUSD=X", False, 10, "float", ""),
    ("Switzerland",   "USDCHF=X", True,  39, "float", "cut to 15 on 14 Nov"),
    ("Sweden",        "USDSEK=X", True,  15, "float", "EU"),
    ("Norway",        "USDNOK=X", True,  15, "float", ""),
    ("Denmark",       "USDDKK=X", True,  15, "peg",   "EU"),
    ("Poland",        "USDPLN=X", True,  15, "float", "EU"),
    ("Hungary",       "USDHUF=X", True,  15, "float", "EU"),
    ("Czechia",       "USDCZK=X", True,  15, "float", "EU"),
    ("Romania",       "USDRON=X", True,  15, "float", "EU"),
    ("Iceland",       "USDISK=X", True,  15, "float", ""),
    ("Australia",     "AUDUSD=X", False, 10, "float", ""),
    ("New Zealand",   "NZDUSD=X", False, 15, "float", ""),
    ("Canada",        "USDCAD=X", True,   0, "float", "USMCA-exempt; 35 non-USMCA"),
    ("Mexico",        "USDMXN=X", True,   0, "float", "USMCA-exempt; 25 non-USMCA"),
    ("Turkey",        "USDTRY=X", True,  15, "float", ""),
    ("Israel",        "USDILS=X", True,  15, "float", ""),
    ("South Africa",  "USDZAR=X", True,  30, "float", ""),
    ("Brazil",        "USDBRL=X", True,  50, "float", "10 Annex I + 40 EO 14323"),
    ("Chile",         "USDCLP=X", True,  10, "float", ""),
    ("Colombia",      "USDCOP=X", True,  10, "float", ""),
    ("Peru",          "USDPEN=X", True,  10, "float", ""),
    ("Uruguay",       "USDUYU=X", True,  10, "float", ""),
    ("South Korea",   "USDKRW=X", True,  15, "float", ""),
    ("India",         "USDINR=X", True,  50, "float", "25 Annex I + 25 Russian oil"),
    ("Indonesia",     "USDIDR=X", True,  19, "float", ""),
    ("Thailand",      "USDTHB=X", True,  19, "float", ""),
    ("Philippines",   "USDPHP=X", True,  19, "float", ""),
    ("Malaysia",      "USDMYR=X", True,  19, "float", ""),
    ("Sri Lanka",     "USDLKR=X", True,  20, "float", ""),
    ("Pakistan",      "USDPKR=X", True,  19, "float", ""),
    ("Bangladesh",    "USDBDT=X", True,  20, "float", ""),
    ("Kazakhstan",    "USDKZT=X", True,  25, "float", ""),
    ("Nigeria",       "USDNGN=X", True,  15, "float", ""),
    ("Egypt",         "USDEGP=X", True,  10, "float", ""),
    ("Kenya",         "USDKES=X", True,  10, "float", ""),
    ("Ghana",         "USDGHS=X", True,  15, "float", ""),
    ("Zambia",        "USDZMW=X", True,  15, "float", ""),
    ("Mauritius",     "USDMUR=X", True,  15, "float", ""),
    ("Tunisia",       "USDTND=X", True,  25, "float", ""),
    ("Moldova",       "USDMDL=X", True,  25, "float", ""),
    ("Ukraine",       "USDUAH=X", True,  10, "float", ""),
    ("Dominican Rep", "USDDOP=X", True,  10, "float", ""),
    ("Costa Rica",    "USDCRC=X", True,  15, "float", ""),
    ("Guatemala",     "USDGTQ=X", True,  10, "float", ""),
    ("Jamaica",       "USDJMD=X", True,  10, "float", ""),
    ("Singapore",     "USDSGD=X", True,  10, "managed", ""),
    ("Taiwan",        "USDTWD=X", True,  20, "managed", ""),
    ("Vietnam",       "USDVND=X", True,  20, "managed", ""),
    ("China",         "USDCNY=X", True,  30, "managed", "truce: 10 + 20 fentanyl"),
    ("Argentina",     "USDARS=X", True,  10, "managed", ""),
    ("Hong Kong",     "USDHKD=X", True,  30, "peg",   "China track"),
    ("Saudi Arabia",  "USDSAR=X", True,  10, "peg",   ""),
    ("UAE",           "USDAED=X", True,  10, "peg",   ""),
    ("Qatar",         "USDQAR=X", True,  10, "peg",   ""),
    ("Jordan",        "USDJOD=X", True,  15, "peg",   ""),
    ("Brunei",        "USDBND=X", True,  25, "peg",   ""),
    ("Cambodia",      "USDKHR=X", True,  19, "peg",   ""),
]

ADVANCED = {
    "Euro area", "Japan", "United Kingdom", "Switzerland", "Canada", "Australia",
    "New Zealand", "Sweden", "Norway", "Denmark", "Iceland", "Israel",
    "South Korea", "Czechia", "Poland", "Hungary", "Romania", "Singapore",
    "Taiwan", "Hong Kong",
}
EXCLUDE = {"China", "Hong Kong"}          # separate legal track, managed/pegged


def ols(d, cols):
    y = d["nu"].values
    X = np.column_stack([np.ones(len(d))] + [d[c].values for c in cols])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    n, k = X.shape
    se = np.sqrt(np.diag((r ** 2).sum() / (n - k) * np.linalg.inv(X.T @ X)))
    r2 = 1 - (r ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return b[1:], b[1:] / se[1:], r2


def main():
    tickers = sorted({c[1] for c in COUNTRIES})
    raw = yf.download(tickers, start="2025-01-01", end="2025-11-15",
                      progress=False, auto_adjust=True)["Close"]

    rows, dropped = [], []
    for name, ticker, invert, tar, regime, note in COUNTRIES:
        if ticker not in raw.columns:
            dropped.append(name)
            continue
        s = raw[ticker].dropna()
        if invert:
            s = 1.0 / s
        m = s.resample("ME").mean()
        m.index = m.index.strftime("%Y-%m")
        if BASE_MONTH not in m.index or END_MONTH not in m.index:
            dropped.append(name)
            continue
        vol = 100.0 * np.log(s.loc["2025-01":"2025-03"]).diff().std()
        rows.append(dict(name=name, tariff=float(tar), regime=regime, note=note,
                         nu=100.0 * np.log(m[END_MONTH] / m[BASE_MONTH]),
                         vol=float(vol)))

    df = pd.DataFrame(rows)
    df["ae"] = df["name"].isin(ADVANCED).astype(float)
    df["live_float"] = ((df["regime"] == "float") & (df["vol"] > VOL_FLOOR)
                        & ~df["name"].isin(EXCLUDE))
    df = df.sort_values("tariff").reset_index(drop=True)

    print(f"{BASE_MONTH} -> {END_MONTH} monthly averages; "
          f"{len(df)} priced, dropped: {', '.join(dropped) or 'none'}")
    print(f"\n{'country':<16}{'tariff':>7}{'d log e':>9}  {'regime':<8} note")
    for _, r in df.iterrows():
        print(f"{r['name']:<16}{r['tariff']:>7.0f}{r['nu']:>9.2f}  "
              f"{r['regime']:<8} {r['note']}")

    fl = df[df["live_float"]]
    checks = [
        ("live floats", fl),
        ("ex South Africa", fl[fl["name"] != "South Africa"]),
        ("ex India, Brazil (add-ons)", fl[~fl["name"].isin(["India", "Brazil"])]),
        ("ex Canada, Mexico (USMCA)", fl[~fl["name"].isin(["Canada", "Mexico"])]),
        ("above baseline only (t>10)", fl[fl["tariff"] > 10]),
    ]
    print(f"\n{'sample':<30}{'n':>4}{'tariff only':>17}{'tariff | AE':>17}"
          f"{'AE dummy':>17}{'R^2':>7}")
    print("theory: negative tariff coefficient")
    for nm, d in checks:
        if len(d) < 5:
            continue
        (s1,), (t1,), _ = ols(d, ["tariff"])
        (s2, a2), (t2, ta2), r2 = ols(d, ["tariff", "ae"])
        print(f"{nm:<30}{len(d):>4}{f'{s1:+.4f} ({t1:+.2f})':>17}"
              f"{f'{s2:+.4f} ({t2:+.2f})':>17}"
              f"{f'{a2:+.3f} ({ta2:+.2f})':>17}{r2:>7.3f}")

    # leave-one-out envelope on the headline sample
    loo = [(ols(fl[fl["name"] != c], ["tariff"])[0][0],
            ols(fl[fl["name"] != c], ["tariff"])[1][0], c) for c in fl["name"]]
    lo, hi = min(loo), max(loo)
    print(f"\nleave-one-out slope {lo[0]:+.4f} (drop {lo[2]}) .. "
          f"{hi[0]:+.4f} (drop {hi[2]})")
    print(f"leave-one-out t     {min(loo, key=lambda r: r[1])[1]:+.2f} .. "
          f"{max(loo, key=lambda r: r[1])[1]:+.2f}")

    # ------------------------------------------------------------------ figure
    fig, ax = plt.subplots(figsize=(9.6, 6.4))
    xs = np.linspace(-2, 55, 50)
    for is_ae, col, lab in [(1.0, "#0f766e", "advanced"), (0.0, "#be123c", "emerging")]:
        g = fl[fl["ae"] == is_ae]
        ax.scatter(g["tariff"], g["nu"], s=58, alpha=.8, color=col,
                   edgecolor="white", linewidth=.8, zorder=3,
                   label=f"{lab}: n={len(g)}, mean {g['nu'].mean():+.1f}%")
    for _, r in fl.iterrows():
        ax.annotate(r["name"], (r["tariff"], r["nu"]), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=7.5, color="#334155")
    (s1,), (t1,), r2 = ols(fl, ["tariff"])
    ic = fl["nu"].mean() - s1 * fl["tariff"].mean()
    ax.plot(xs, ic + s1 * xs, color="#334155", lw=1.7, alpha=.85,
            label=f"slope {s1:+.3f} %/pp (t={t1:+.2f}), $R^2$ {r2:.2f}, n={len(fl)}")
    ax.axhline(0, color="#94a3b8", lw=.8)
    ax.grid(alpha=.25, lw=.6)
    ax.set_axisbelow(True)
    ax.set_xlabel("settled tariff rate in force from 7 Aug 2025, percentage points")
    ax.set_ylabel("USD per foreign currency, % change Mar to Oct 2025\n"
                  "(positive = USD depreciation)")
    ax.set_title("Exchange rates against the settled tariff schedule\n"
                 "monthly averages, March to October 2025; "
                 "theory predicts a negative slope", loc="left", fontsize=12)
    ax.legend(fontsize=8.5, loc="best", framealpha=.9)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    path = OUT_DIR / "settled_schedule_cross_section.pdf"
    fig.savefig(path, bbox_inches="tight")
    fig.savefig(path.with_suffix(".png"), dpi=160, bbox_inches="tight")
    df.to_csv(OUT_DIR / "settled_schedule_cross_section.csv", index=False)
    print(f"\nwrote {path}, .png and .csv")


if __name__ == "__main__":
    main()
