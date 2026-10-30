# 2025 tariff timeline (headline rates)

`tariff_timeline.csv` holds step functions with the columns `series, effective_date, rate_pp, note, source_url`. Each `rate_pp` is the headline additional tariff, in percentage points above the pre-2025 baseline. It applies from `effective_date` until the next row of the same series. These are statutory headline rates, not trade-weighted effective rates. Section 232 product tariffs (steel, aluminium, autos, copper and others), de minimis changes and exclusions are left out.

Compiled 2026-10-29. US effective times come from the Federal Register text of each executive order. The FR documents were checked through the federalregister.gov API, and the EO 14326 Annex I rates were checked on whitehouse.gov. Chinese measures are State Council Tariff Commission (SCTC) announcements. They are documented here through USDA FAS reports, the recitals of US executive orders, China Daily/Xinhua and a law-firm alert (White & Case), because the original gss.mof.gov.cn pages were not retrieved.

Series:
- `us_on_china` is the IEEPA fentanyl tariff (EO 14195/14228/14357) plus the IEEPA reciprocal tariff (EO 14257/14259/14266/14298/14358).
- `china_on_us` is China's across-the-board additional tariff on all US goods.
- `china_on_us_targeted` covers China's product-specific retaliation of February 10 (coal and LNG at 15%; oil, farm machinery and some vehicles at 10%) and March 10 (740 agricultural lines at 10-15%). Here `rate_pp` is the maximum product rate. These measures are kept out of the headline series. For a headline figure, show them as a separate dashed or shaded "targeted measures" band, or as a footnote. If a single number is needed, convert them to a trade-weighted increment using 2024 US export shares of the covered lines. Do not add 15 pp to the headline.
- `us_on_eu`: from 2025-08-07 the EU rate is **inclusive of MFN** (15% all-in floor). The increment above baseline is 15 minus the MFN rate, line by line.
- `us_on_others` is the 10% default for partners not listed in an annex.
- `us_on_vietnam` is shown for the Vietnam example.
- `us_on_canada` and `us_on_mexico` are the IEEPA tariffs of EO 14193 and EO 14194, effective March 4. From March 7 (EO 14231/14232), USMCA-qualifying goods are exempt, so `rate_pp` from that date is the rate on non-USMCA goods only (energy and potash: 10%). Canada's rate rose to 35% on August 1 (EO 14325). Mexico's rate was unchanged through 2025. Neither country is subject to the EO 14257 reciprocal tariff.
- `canada_on_us` is Canada's 25% surtax on **covered** US goods, which is not an across-the-board rate. Coverage starts on March 4 (C$30 billion), widens on March 13 (C$29.8 billion more, including steel and aluminium) and April 9 (autos), and narrows on September 1, when surtaxes on C$44.2 billion were removed and only the steel, aluminium and auto countermeasures remained. Rows at an unchanged rate record these coverage changes. Sources are Department of Finance Canada notices. Mexico did not retaliate.

Added 2026-10-29 (v3). Canada/Mexico US measures come from the Federal Register (EO text and CBP implementation notices). Canadian measures come from Department of Finance Canada news releases and its "Canada's response to U.S. tariffs" page.

Dates are US entry dates at 12:01 a.m. Eastern for US measures, and Beijing time for Chinese measures (12:01 or 13:01).
