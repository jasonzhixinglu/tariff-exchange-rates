# 2024 goods-trade raw inputs (US / China / ROW)

Retrieved 2026-10-29. All values are in `trade_2024.json`. Each value has its units, source URL, table or series, and raw file. Raw files are saved unmodified.

| File | Source |
|---|---|
| `census_c5700_china.html` | Census, Trade in Goods with China (NSA, current revised) |
| `census_c0004_world.html` | Census, Trade in Goods with World (seasonally adjusted) |
| `census_hist_goods.xlsx`, `census_hist_goods.pdf` | Census, U.S. Trade in Goods, BOP vs Census basis, annual (NSA) |
| `census_hist_gands.xlsx` | Census, goods and services, BOP basis (context only) |
| `gacc_2024_12_by_country_usd.html` | GACC, (2) Imports and Exports by Country (Region), 12.2024, US$1,000 (preliminary) |
| `imf_imts_2024.csv` | IMF IMTS SDMX API (US, China, World; annual 2024) |
| `imf_weo_gdp_2024.csv` | IMF WEO Oct 2026 SDMX API (NGDPD, PPPGDP) |
| `wto_trade_outlook25.pdf` | WTO Global Trade Outlook and Statistics, Apr 2025 |
| `bea_NipaDataA.txt` | BEA NIPA annual flat file (PCE goods, GDP goods, goods X/M) |

Caveats:
- US figures are on two vintages. The Census pages are revised (China imports 440.3). The IMF IMTS copy is the first release (438.9), which `data/calibration_inputs.json` uses.
- Valuation bases differ: Census imports are at customs value and exports at FAS. GACC imports are CIF and exports FOB.
- The `derived` block in the JSON is plain arithmetic for convenience. It is not a balanced baseline.
- The `check_3p8_vs_28_claim` block records what reproduces the draft's 3.8% / 28% claim in Section 4.5 of `paper_draft_v1.md`.

Note: `bea_NipaDataA.txt` (12 MB) is git-ignored and kept locally only. It can be re-downloaded from https://apps.bea.gov/national/Release/TXT/NipaDataA.txt; the values used are recorded in `trade_2024.json`.
