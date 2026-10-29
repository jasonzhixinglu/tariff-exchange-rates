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

Dates are US entry dates at 12:01 a.m. Eastern for US measures, and Beijing time for Chinese measures (12:01 or 13:01).
