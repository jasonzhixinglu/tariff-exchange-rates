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
}


def fetch_monthly_avg(ticker_sym: str, invert: bool) -> dict[str, float]:
    """Download daily close prices and return period averages."""
    raw = yf.download(
        ticker_sym,
        start="2024-01-01",
        end="2025-05-01",
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
                    "regime1": pct_change(avgs["regime1"], base),
                    "regime2": pct_change(avgs["regime2"], base),
                },
            }
            r1 = results[key]["pct_changes"]["regime1"]
            r2 = results[key]["pct_changes"]["regime2"]
            print(f"R1={r1:+.2f}%  R2={r2:+.2f}%")
        except Exception as exc:
            results[key] = {"label": label, "ticker": ticker, "error": str(exc)}
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
