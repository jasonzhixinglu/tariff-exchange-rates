"""Data inputs of Section 4.5 (code/checks/episode2025.py, Figure 7):

  * every tariff series starts from a 2025-01-01 baseline of zero, has dated
    steps in order, and records a source URL for each non-baseline row;
  * the North American measures carry the dates and rates of the Federal
    Register and Department of Finance Canada notices;
  * the phase table's sign convention (positive = dollar depreciation) and
    the Feb 28 - Mar 7 window are computed from the cached daily data."""
import os

import pandas as pd
import pytest

from checks import episode2025 as ep

TL = pd.read_csv(os.path.join(ep.ROOT, "data", "raw", "tariffs2025", "tariff_timeline.csv"),
                 parse_dates=["effective_date"])
NEED_DAILY = pytest.mark.skipif(not os.path.exists(ep.DAILY), reason="run fetch_fx_2025.py first")


@pytest.mark.parametrize("series", sorted(TL.series.unique()))
def test_timeline_series_well_formed(series):
    s = TL[TL.series == series]
    base = s.effective_date == pd.Timestamp("2025-01-01")
    if series != "china_on_us_targeted":  # product-specific; no headline baseline row
        assert base.iloc[0] and s.rate_pp.iloc[0] == 0
    assert s.effective_date.is_monotonic_increasing
    assert s[~base].source_url.str.startswith("https://").all()


@pytest.mark.parametrize("series, date, rate", [
    ("us_on_canada", "2025-03-04", 25), ("us_on_canada", "2025-08-01", 35),
    ("us_on_mexico", "2025-03-04", 25), ("canada_on_us", "2025-03-04", 25),
    ("us_on_china", "2025-05-14", 30), ("us_on_china", "2025-11-10", 20),
])
def test_timeline_rates(series, date, rate):
    s = TL[TL.series == series].set_index("effective_date").rate_pp
    assert s.loc[:date].iloc[-1] == rate


def test_pct_sign_convention():
    # USD per foreign up = dollar depreciation; index up = dollar appreciation
    assert ep.pct(1.0, 1.1, "usd_per_eur") > 0
    assert ep.pct(100.0, 110.0, "broad_index") < 0


@NEED_DAILY
def test_week_window_and_cad_mxn():
    d = pd.read_csv(ep.DAILY, parse_dates=["date"]).set_index("date")
    for key in ("usd_per_cad", "usd_per_mxn", "broad_index"):
        t0, x0 = ep.last_close(d[key], ep.WEEK[0])
        t1, x1 = ep.last_close(d[key], ep.WEEK[1])
        assert str(t0.date()) == "2025-02-28" and str(t1.date()) == "2025-03-07"
        assert abs(ep.pct(x0, x1, key)) < 5
