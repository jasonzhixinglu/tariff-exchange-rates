"""
Fetch historical exchange rate data from Yahoo Finance and compute period
averages for use in the calibration panel.

Periods
-------
  baseline : 2024 annual average (Jan 1 – Dec 31, 2024)
  regime1  : March 2025 average  (corresponds to Regime 1 fentanyl tariffs)
  regime2  : April 2025 average  (corresponds to Regime 2 peak escalation)

Convention
----------
  All rates are expressed as USD per unit of foreign currency (e_AC in the
  model sense: units of A's currency per unit of C's currency).  A positive
  percent change means the USD depreciated against that currency.

Yahoo Finance tickers
---------------------
  EURUSD=X  → USD per EUR  (already in correct direction)
  USDJPY=X  → JPY per USD  → invert to get USD per JPY
  USDKRW=X  → KRW per USD  → invert
  USDMXN=X  → MXN per USD  → invert
  USDCAD=X  → CAD per USD  → invert
  USDVND=X  → VND per USD  → invert
  USDTWD=X  → TWD per USD  → invert
  USDINR=X  → INR per USD  → invert
  USDCNY=X  → CNY per USD  → invert  (onshore RMB; use for USD/RMB e_AB)

Output: data/fx_data.json
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Ticker definitions
# ticker      : Yahoo Finance symbol
# invert      : True  → series = 1 / raw  (converts "USD per foreign" convention)
# country_key : matches keys in calibration_panel.json; "RMB" is the B-country rate
# label       : human-readable description
# ---------------------------------------------------------------------------
TICKERS = [
    {"ticker": "USDCNY=X", "invert": True,  "key": "RMB", "label": "USD/CNY (RMB)"},
    {"ticker": "EURUSD=X", "invert": False, "key": "EU",  "label": "USD/EUR"},
    {"ticker": "USDJPY=X", "invert": True,  "key": "JPN", "label": "USD/JPY"},
    {"ticker": "USDKRW=X", "invert": True,  "key": "KOR", "label": "USD/KRW"},
    {"ticker": "USDMXN=X", "invert": True,  "key": "MEX", "label": "USD/MXN"},
    {"ticker": "USDCAD=X", "invert": True,  "key": "CAN", "label": "USD/CAD"},
    {"ticker": "USDVND=X", "invert": True,  "key": "VNM", "label": "USD/VND"},
    {"ticker": "USDTWD=X", "invert": True,  "key": "TWN", "label": "USD/TWD"},
    {"ticker": "USDINR=X", "invert": True,  "key": "IND", "label": "USD/INR"},
]

PERIODS = {
    "baseline": ("2024-01-01", "2024-12-31", "2024 annual average"),
    "regime1":  ("2025-03-01", "2025-03-31", "March 2025 (Regime 1)"),
    "regime2":  ("2025-04-01", "2025-04-30", "April 2025 (Regime 2)"),
    # Extended windows (revision item D3): the model's object is the long-run
    # position, which only becomes visible as the transition plays out.
    "h2_2025":  ("2025-07-01", "2025-12-31", "H2 2025 average (extended window)"),
    "dec2025":  ("2025-12-01", "2025-12-31", "December 2025 (extended window)"),
}

FETCH_END = "2026-01-01"

# Matched ROW index (revision item D2): the model's C = "world minus US and
# China", so the comparison index must exclude the RMB. We strip the CNY
# component out of the Fed H.10 BROAD nominal dollar index using the Fed's
# published weight and renormalize:
#   dlog I_exCN = (dlog I_broad - w_CN * dlog CNYperUSD) / (1 - w_CN)
# expressed in this file's convention (positive = USD depreciation) as the
# negative of dollar appreciation. Weight source: H.10 currency weights,
# China = 10.897 percent (2024/2025 weights).
FRED_BROAD_URL = ("https://fred.stlouisfed.org/graph/fredgraph.csv"
                  "?id=DTWEXBGS")
CN_WEIGHT = 0.10897


def fetch_monthly_avg(ticker_sym: str, invert: bool) -> dict[str, float]:
    """Download daily close prices and return period averages."""
    raw = yf.download(
        ticker_sym,
        start="2024-01-01",
        end=FETCH_END,
        auto_adjust=True,
        progress=False,
    )["Close"]

    if isinstance(raw, pd.DataFrame):
        raw = raw.squeeze()

    if invert:
        raw = 1.0 / raw

    avgs = {}
    for period_key, (start, end, _) in PERIODS.items():
        slice_ = raw.loc[start:end].dropna()
        avgs[period_key] = float(slice_.mean()) if len(slice_) > 0 else None

    return avgs


def fetch_row_matched_index() -> dict:
    """
    Construct the ex-China broad-dollar index for the ROW configuration.

    Returns period log-levels of the Fed broad index and USD/CNY, and the
    implied ex-China percent changes in this file's convention
    (positive = USD depreciation against the ex-China basket).
    """
    import io
    import urllib.request

    with urllib.request.urlopen(FRED_BROAD_URL, timeout=60) as resp:
        csv_bytes = resp.read()
    broad = pd.read_csv(io.BytesIO(csv_bytes), na_values=".")
    date_col, val_col = broad.columns[0], broad.columns[1]
    broad[date_col] = pd.to_datetime(broad[date_col])
    broad = broad.set_index(date_col)[val_col].dropna()

    cny_per_usd = yf.download("USDCNY=X", start="2024-01-01", end=FETCH_END,
                              auto_adjust=True, progress=False)["Close"]
    if isinstance(cny_per_usd, pd.DataFrame):
        cny_per_usd = cny_per_usd.squeeze()

    out = {"log_broad": {}, "log_cny": {}, "pct_changes": {}}
    for period_key, (start, end, _) in PERIODS.items():
        b = broad.loc[start:end].dropna()
        c = cny_per_usd.loc[start:end].dropna()
        out["log_broad"][period_key] = float(np.log(b).mean()) if len(b) else None
        out["log_cny"][period_key] = float(np.log(c).mean()) if len(c) else None

    b0, c0 = out["log_broad"]["baseline"], out["log_cny"]["baseline"]
    for period_key in PERIODS:
        if period_key == "baseline":
            continue
        bt, ct = out["log_broad"][period_key], out["log_cny"][period_key]
        if None in (b0, c0, bt, ct):
            out["pct_changes"][period_key] = None
            continue
        dlog_appr_ex_cn = ((bt - b0) - CN_WEIGHT * (ct - c0)) / (1 - CN_WEIGHT)
        out["pct_changes"][period_key] = round(
            100.0 * (np.exp(-dlog_appr_ex_cn) - 1.0), 4)
    return out


def pct_change(new_val, base_val):
    """Percent change: 100 × (level_t / level_0 − 1)."""
    if new_val is None or base_val is None:
        return None
    return round(100.0 * (new_val / base_val - 1.0), 4)


def run():
    out_path = ROOT / "data" / "fx_data.json"
    out_path.parent.mkdir(exist_ok=True)

    results = {}
    for spec in TICKERS:
        key    = spec["key"]
        ticker = spec["ticker"]
        label  = spec["label"]
        print(f"  Fetching {ticker} ({label}) ...", end=" ", flush=True)

        try:
            avgs = fetch_monthly_avg(ticker, spec["invert"])
            base = avgs["baseline"]
            results[key] = {
                "label":   label,
                "ticker":  ticker,
                "inverted": spec["invert"],
                "levels":  {k: round(v, 8) if v else None for k, v in avgs.items()},
                "pct_changes": {
                    k: pct_change(avgs[k], base)
                    for k in PERIODS if k != "baseline"
                },
            }
            pc = results[key]["pct_changes"]
            print("  ".join(f"{k}={v:+.2f}%" for k, v in pc.items()
                            if v is not None))
        except Exception as exc:
            results[key] = {"label": label, "ticker": ticker, "error": str(exc)}
            print(f"FAILED: {exc}")

    # Matched ex-China broad-dollar index for the ROW configuration
    print("  Fetching FRED DTWEXBGS + stripping CNY (w = "
          f"{CN_WEIGHT:.5f}) ...", end=" ", flush=True)
    try:
        row = fetch_row_matched_index()
        results["ROW"] = {
            "label": "Ex-China broad dollar index (Fed H.10 DTWEXBGS, "
                     "CNY stripped and renormalized)",
            "ticker": "DTWEXBGS (FRED) + USDCNY=X",
            "cn_weight": CN_WEIGHT,
            "log_levels": {"broad": row["log_broad"], "cny": row["log_cny"]},
            "pct_changes": row["pct_changes"],
        }
        print("  ".join(f"{k}={v:+.2f}%" for k, v in row["pct_changes"].items()
                        if v is not None))
    except Exception as exc:
        results["ROW"] = {"label": "Ex-China broad dollar index",
                          "error": str(exc)}
        print(f"FAILED: {exc}")

    payload = {
        "meta": {
            "description": "Observed bilateral exchange rates vs USD, period averages",
            "convention":  "USD per unit of foreign currency; positive pct-change = USD depreciation",
            "source":      "Yahoo Finance via yfinance",
            "periods": {k: {"start": v[0], "end": v[1], "description": v[2]}
                        for k, v in PERIODS.items()},
        },
        "rates": results,
    }

    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"\nWritten to {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    run()
