# Exchange-rate raw data for the 2025 tariff figure

The files are downloaded by `code/data/fetch_fx_2025.py` and saved exactly as served, with no edits. All files were retrieved on **2026-10-29**. `download_manifest.json` records the URL, retrieval date and byte count of each file. The processed output is `data/processed/fx2025_monthly.csv`.

| File | Source / URL | Series ID | Units | Frequency |
|---|---|---|---|---|
| `fred_DEXUSEU.csv` | FRED, https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU&cosd=2023-12-01&coed=2025-12-31 | DEXUSEU (Fed H.10) | U.S. dollars per euro, noon buying rates in New York | Daily (business days; "." = missing) |
| `fred_DEXCHUS.csv` | FRED, https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXCHUS&cosd=2023-12-01&coed=2025-12-31 | DEXCHUS (Fed H.10) | Chinese yuan renminbi per U.S. dollar | Daily |
| `fred_DTWEXBGS.csv` | FRED, https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTWEXBGS&cosd=2023-12-01&coed=2025-12-31 | DTWEXBGS (Fed H.10) | Nominal broad U.S. dollar index, goods and services, Jan 2006 = 100. A rise means dollar appreciation | Daily |
| `bis_WS_XRU_VN_VND.csv` | BIS SDMX API, https://stats.bis.org/api/v1/data/WS_XRU/.VN.VND.?startPeriod=2024-01-01&endPeriod=2025-12-31&format=csv | BIS dataflow WS_XRU ("US dollar exchange rates"), keys M.VN.VND.A (monthly average) and M.VN.VND.E (end of period); Q and A rows are also in the file | Viet Nam dong per U.S. dollar | Monthly |
| `h10_weights_current.htm` | https://www.federalreserve.gov/releases/h10/weights/default.htm | H.10 broad index total trade weights, "Trade Weights as of February 2, 2026" | Percent | Annual weights |
| `h10_weights_previous.htm` | https://www.federalreserve.gov/releases/h10/weights/previousweights.htm | Previous vintage, "Trade Weights as of March 24, 2025" (in use Mar 24, 2025 to Jan 30, 2026) | Percent | Annual weights |
| `h10_china_weight.json` | Built from the two pages above | China weight used, plus the previous vintage and the full 2024/2025 table | Percent | |

Notes:
- **VND.** BIS publishes no daily VND series; the old WS_XRU_D dataflow no longer exists, and WS_XRU has no D frequency for VN. The BIS monthly average for **2025-08 is missing**. The IMF ER dataset (api.imf.org, IMF.STA:ER, VNM USD_XDC PA_RT) also lacks it, so `usd_per_vnd` is NaN for 2025-08. The end-of-month value is available.
- **China weight used:** 10.897% for both 2024 and 2025, from the current vintage. The Fed says superseded weights "are no longer used in calculating the historical and current dollar index values", so DTWEXBGS as downloaded today embeds this vintage. In the previous vintage the China weight was 11.212% for 2024 and 2025.
- **Broad ex-China index.** It is chained daily as d log I_exCN = (d log I - w_CN(year) * d log(CNY/USD)) / (1 - w_CN), over dates where both DTWEXBGS and DEXCHUS are observed. Its level is set equal to DTWEXBGS on 2024-01-02.
