"""Section 4.5 and Table 6: exchange-rate changes within each phase of the
2025 tariff episode, from monthly averages and from daily data.

Phases are dated by announcements, when markets learn the configuration:
  unilateral    Feb 1 (EO 14195 signed) - Apr 2 (reciprocal-tariff announcement)
  retaliation   Apr 3 - May 12 (Geneva joint statement)
  near-uniform  Aug 7 (framework rates in force) - Dec 31
Daily changes run from the last close before the phase to the last close in
it.  Monthly changes run from the average of the month before the phase to the
average of its last full month (unilateral Jan->Mar, retaliation Mar->Apr,
near-uniform Jul->Dec).  VND is available only monthly (BIS), so its "daily"
entry uses BIS end-of-month values over the same months.
Positive = dollar depreciation.  Writes code/results/episode2025.json and
paper/tables/tab6_phases.tex.
"""
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DAILY = os.path.join(ROOT, "data", "processed", "fx2025_daily.csv")
MONTHLY = os.path.join(ROOT, "data", "processed", "fx2025_monthly.csv")
TAB = os.path.join(ROOT, "paper", "tables", "tab6_phases.tex")

PHASES = {
    "unilateral": dict(daily=("2025-01-31", "2025-04-02"), monthly=("2025-01", "2025-03")),
    "retaliation": dict(daily=("2025-04-02", "2025-05-12"), monthly=("2025-03", "2025-04")),
    "near_uniform": dict(daily=("2025-08-06", "2025-12-31"), monthly=("2025-07", "2025-12")),
}
SERIES = [("usd_per_eur", "EUR"), ("usd_per_cny", "CNY"), ("usd_per_vnd", "VND"),
          ("broad_index", "Broad index"), ("broad_exCN_index", r"Broad index ex.\ China")]


def pct(x0, x1, key):
    """Percent change, positive = dollar depreciation."""
    return 100 * (x1 / x0 - 1) if key.startswith("usd_per") else 100 * (x0 / x1 - 1)


def last_close(s, date):
    s = s.dropna().loc[:date]
    return s.index[-1], s.iloc[-1]


def main():
    d = pd.read_csv(DAILY, parse_dates=["date"]).set_index("date")
    m = pd.read_csv(MONTHLY).set_index("month")
    res = {}
    for ph, spec in PHASES.items():
        out = {}
        (m0, m1), (d0, d1) = spec["monthly"], spec["daily"]
        for key, _ in SERIES:
            row = dict(monthly=pct(m.loc[m0, key], m.loc[m1, key], key))
            if key in d:
                t0, x0 = last_close(d[key], d0)
                t1, x1 = last_close(d[key], d1)
                row.update(daily=pct(x0, x1, key), daily_dates=[str(t0.date()), str(t1.date())])
            else:
                row.update(daily=pct(m.loc[m0, key + "_eom"], m.loc[m1, key + "_eom"], key),
                           daily_dates=["end-" + m0, "end-" + m1], daily_is_eom=True)
            out[key] = row
        res[ph] = out
    # cumulative since the January 2025 base (monthly averages; Figure 7a)
    res["vs_january"] = {mo: {k: float(m.loc[mo, "dev_" + k]) for k, _ in SERIES}
                         for mo in m.index if mo.startswith("2025")}
    # the US tariff on China by date (checked against the timeline)
    tl = pd.read_csv(os.path.join(ROOT, "data", "raw", "tariffs2025", "tariff_timeline.csv"),
                     parse_dates=["effective_date"])
    c = tl[tl.series == "us_on_china"].sort_values("effective_date")
    res["us_on_china_timeline"] = [[str(t.date()), float(r)] for t, r in zip(c.effective_date, c.rate_pp)]
    with open(os.path.join(HERE, "..", "results", "episode2025.json"), "w") as fh:
        json.dump(res, fh, indent=1)

    lines = []
    for key, lab in SERIES:
        cells = []
        for ph in PHASES:
            r = res[ph][key]
            dv = "%.1f" % r["daily"] + ("$^{a}$" if r.get("daily_is_eom") else "")
            cells += ["%.1f" % r["monthly"], dv]
        lines.append(lab + " & " + " & ".join(c.replace("-", "$-$") if c[0] == "-" else c for c in cells) + r" \\")
    os.makedirs(os.path.dirname(TAB), exist_ok=True)
    with open(TAB, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    for ph in PHASES:
        print(ph, {k: (round(v["monthly"], 2), round(v["daily"], 2)) for k, v in res[ph].items()})
    print("Dec vs Jan", {k: round(v, 2) for k, v in res["vs_january"]["2025-12"].items()})


if __name__ == "__main__":
    main()
