"""
Fetch and tidy the exchange-rate data for the 2025 tariff figure.

Idempotent: each raw file is downloaded into data/raw/fx2025/ only if it is not
already cached there (files are saved byte-for-byte as served, no edits). The
processed monthly file is rebuilt from the cached raw files on every run.

Raw sources (see data/raw/fx2025/README.md for full documentation)
------------------------------------------------------------------
  FRED DEXUSEU   USD per EUR, daily (H.10 noon buying rates, NY)
  FRED DEXCHUS   CNY per USD, daily (H.10)
  FRED DTWEXBGS  Nominal broad dollar index, goods & services, Jan 2006 = 100,
                 daily (H.10); a rise = dollar appreciation
  BIS  WS_XRU    VND per USD, Viet Nam, monthly average (collection A) and
                 end-of-period (collection E). BIS publishes no daily VND
                 series, and the Aug-2025 monthly average is missing in BIS
                 (and in the IMF ER dataset), so usd_per_vnd is NaN for 2025-08.
  Fed H.10 weights pages (current + previous vintage), HTML.

Broad index excluding China
---------------------------
The H.10 broad index is a chained geometric weighted average:
    d log I_t = sum_j w_j(t) d log e_j,t      (e_j = foreign currency per USD)
so removing China gives
    d log I^exCN_t = (d log I_t - w_CN(t) * d log(CNY per USD)_t) / (1 - w_CN(t)).
We chain this DAILY, on dates where both DTWEXBGS and DEXCHUS are observed
(log changes are taken between consecutive common observation dates), using the
China weight for the calendar year of date t from the CURRENT weight vintage
(Fed page "Trade Weights as of February 2, 2026"). The Fed states that weights
from superseded vintages "are no longer used in calculating the historical and
current dollar index values", so the DTWEXBGS series downloaded now embeds the
current-vintage weights for 2024 and 2025; using that vintage keeps the
decomposition internally consistent. The index level is anchored to DTWEXBGS on
the first common date (2024-01-02); only percentage deviations are meaningful.

Monthly aggregation
-------------------
  *_avg (main columns): mean of daily observations in the month. USD-per-foreign
      series are inverted DAILY before averaging (1/DEXCHUS); VND is only
      available as a monthly average, so usd_per_vnd = 1 / (monthly avg VND/USD).
  *_eom: last available daily observation in the month (BIS end-of-period for VND).
  Base: the JANUARY 2025 average, the last month before the first tariff
      executive order (Feb 1, 2025): mean of the January 2025 daily
      observations (VND: the BIS January 2025 monthly average).

Deviation columns (positive = DOLLAR DEPRECIATION):
  USD-per-foreign series: 100 * (x / base - 1)
  broad indices:          100 * (base / x - 1)

Outputs: data/processed/fx2025_monthly.csv (monthly averages, end-of-month
values and deviations) and data/processed/fx2025_daily.csv (daily USD/EUR,
USD/CNY, broad index and broad index ex. China).
"""

from __future__ import annotations

import datetime as dt
import html.parser
import json
import re
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "fx2025"
OUT = ROOT / "data" / "processed" / "fx2025_monthly.csv"
OUT_DAILY = ROOT / "data" / "processed" / "fx2025_daily.csv"
BASE_MONTH = "2025-01"

START, END = "2023-12-01", "2025-12-31"
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={s}&coed={e}"
BIS_URL = ("https://stats.bis.org/api/v1/data/WS_XRU/.VN.VND."
           "?startPeriod=2024-01-01&endPeriod=2025-12-31&format=csv")
H10_CURRENT_URL = "https://www.federalreserve.gov/releases/h10/weights/default.htm"
H10_PREVIOUS_URL = "https://www.federalreserve.gov/releases/h10/weights/previousweights.htm"

SOURCES = {
    "fred_DEXUSEU.csv": FRED_URL.format(sid="DEXUSEU", s=START, e=END),
    "fred_DEXCHUS.csv": FRED_URL.format(sid="DEXCHUS", s=START, e=END),
    "fred_DTWEXBGS.csv": FRED_URL.format(sid="DTWEXBGS", s=START, e=END),
    "bis_WS_XRU_VN_VND.csv": BIS_URL,
    "h10_weights_current.htm": H10_CURRENT_URL,
    "h10_weights_previous.htm": H10_PREVIOUS_URL,
}
MANIFEST = RAW / "download_manifest.json"


# ---------------------------------------------------------------- download --
def fetch_raw() -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    for fname, url in SOURCES.items():
        path = RAW / fname
        if path.exists() and path.stat().st_size > 0:
            print(f"cached     {fname}")
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)"})
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read()
        path.write_bytes(data)
        manifest[fname] = {"url": url, "retrieved": dt.date.today().isoformat(),
                           "bytes": len(data)}
        print(f"downloaded {fname} ({len(data):,} bytes)")
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


# ------------------------------------------------------- H.10 weight table --
class _TableParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self._row, self._cell, self._in = [], None, "", False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._in, self._cell = True, ""

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._in:
            self._row.append(" ".join(self._cell.split()))
            self._in = False
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._in:
            self._cell += data


def parse_h10_weights(path: Path) -> tuple[str, pd.DataFrame]:
    text = path.read_text(encoding="utf-8-sig")
    m = re.search(r"Trade Weights as of\s+([A-Z][a-z]+ \d{1,2}, \d{4})", text)
    vintage = m.group(1) if m else "unknown"
    p = _TableParser()
    p.feed(text)
    header = next(r for r in p.rows if r and r[0].startswith("Country"))
    years = [int(y) for y in header[1:]]
    body = {r[0].lstrip("*").strip(): [float(v) for v in r[1:]]
            for r in p.rows if r is not header and len(r) == len(header)
            and re.fullmatch(r"[\d.]+", r[1] or "")}
    return vintage, pd.DataFrame(body, index=years).T


def china_weights() -> dict[int, float]:
    vin_cur, w_cur = parse_h10_weights(RAW / "h10_weights_current.htm")
    vin_prev, w_prev = parse_h10_weights(RAW / "h10_weights_previous.htm")
    manifest = json.loads(MANIFEST.read_text())
    used = {y: float(w_cur.loc["China", y]) for y in (2024, 2025)}
    record = {
        "description": ("Federal Reserve H.10 broad dollar index total trade weight for "
                        "China (percent). 'used' = weights applied to construct "
                        "broad_exCN_index (current vintage; the Fed states superseded "
                        "vintages are no longer used for historical index values)."),
        "used": {
            "vintage": f"Trade Weights as of {vin_cur}",
            "source_url": H10_CURRENT_URL,
            "retrieval_date": manifest["h10_weights_current.htm"]["retrieved"],
            "china_weight_pct": {str(y): v for y, v in used.items()},
        },
        "previous_vintage_for_reference": {
            "vintage": f"Trade Weights as of {vin_prev} (in use Mar 24, 2025 - Jan 30, 2026)",
            "source_url": H10_PREVIOUS_URL,
            "retrieval_date": manifest["h10_weights_previous.htm"]["retrieved"],
            "china_weight_pct": {str(y): float(w_prev.loc["China", y])
                                 for y in (2024, 2025) if y in w_prev.columns},
        },
        "full_table_current_vintage_2024_2025_pct": {
            c: {"2024": float(w_cur.loc[c, 2024]), "2025": float(w_cur.loc[c, 2025])}
            for c in w_cur.index},
    }
    (RAW / "h10_china_weight.json").write_text(json.dumps(record, indent=2) + "\n")
    return {y: v / 100.0 for y, v in used.items()}


# ---------------------------------------------------------------- tidying --
def read_fred(sid: str) -> pd.Series:
    df = pd.read_csv(RAW / f"fred_{sid}.csv", na_values=["."])
    s = df.set_index(pd.to_datetime(df.iloc[:, 0]))[sid].astype(float).dropna()
    return s.loc["2024-01-01":"2025-12-31"]


def read_bis_vnd() -> tuple[pd.Series, pd.Series]:
    df = pd.read_csv(RAW / "bis_WS_XRU_VN_VND.csv")
    m = df[df.FREQ == "M"]
    avg = m[m.COLLECTION == "A"].set_index("TIME_PERIOD")["OBS_VALUE"].astype(float)
    eop = m[m.COLLECTION == "E"].set_index("TIME_PERIOD")["OBS_VALUE"].astype(float)
    return avg.sort_index(), eop.sort_index()


def broad_ex_china(broad: pd.Series, cny: pd.Series, w: dict[int, float]) -> pd.Series:
    j = pd.concat({"I": broad, "c": cny}, axis=1).dropna()
    dl = np.log(j).diff()
    wcn = pd.Series([w[d.year] for d in j.index], index=j.index)
    dlex = (dl["I"] - wcn * dl["c"]) / (1 - wcn)
    dlex.iloc[0] = 0.0
    return j["I"].iloc[0] * np.exp(dlex.cumsum())


def main() -> None:
    fetch_raw()
    w = china_weights()

    eur = read_fred("DEXUSEU")              # USD per EUR
    cny = read_fred("DEXCHUS")              # CNY per USD
    broad = read_fred("DTWEXBGS")
    exc = broad_ex_china(broad, cny, w)
    daily = {"usd_per_eur": eur, "usd_per_cny": 1.0 / cny,
             "broad_index": broad, "broad_exCN_index": exc}

    months = pd.period_range("2024-01", "2025-12", freq="M")
    out = pd.DataFrame(index=months.astype(str))
    eom = pd.DataFrame(index=out.index)
    base = {}
    for k, s in daily.items():
        g = s.groupby(s.index.to_period("M"))
        out[k] = g.mean().reindex(months).values
        eom[k] = g.last().reindex(months).values
        base[k] = s.loc[BASE_MONTH].mean()

    vavg, veop = read_bis_vnd()
    out["usd_per_vnd"] = (1.0 / vavg).reindex(out.index)
    eom["usd_per_vnd"] = (1.0 / veop).reindex(out.index)
    base["usd_per_vnd"] = out.loc[BASE_MONTH, "usd_per_vnd"]

    cols = ["usd_per_eur", "usd_per_cny", "usd_per_vnd", "broad_index", "broad_exCN_index"]
    out = out[cols]
    eom = eom[cols]

    def dev(df):
        d = pd.DataFrame(index=df.index)
        for k in cols:
            if k.startswith("usd_per"):
                d[k] = 100 * (df[k] / base[k] - 1)
            else:
                d[k] = 100 * (base[k] / df[k] - 1)
        return d

    d_avg, d_eom = dev(out), dev(eom)
    final = out.copy()
    for k in cols:
        final[f"dev_{k}"] = d_avg[k]
    for k in cols:
        final[f"{k}_eom"] = eom[k]
    for k in cols:
        final[f"dev_{k}_eom"] = d_eom[k]
    final.index.name = "month"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(OUT, float_format="%.8g")
    print(f"wrote {OUT}")
    dd = pd.concat(daily, axis=1)
    dd.index.name = "date"
    dd.to_csv(OUT_DAILY, float_format="%.8g")
    print(f"wrote {OUT_DAILY}")
    print(f"China weights used: {w}")
    show = ["2025-03", "2025-04", "2025-12"]
    print("\n(a) monthly average vs January 2025 average (%, + = USD depreciation)")
    print(d_avg.loc[show].round(2).to_string())
    print("\n(b) end-of-month vs January 2025 average (%, + = USD depreciation)")
    print(d_eom.loc[show].round(2).to_string())


if __name__ == "__main__":
    main()
