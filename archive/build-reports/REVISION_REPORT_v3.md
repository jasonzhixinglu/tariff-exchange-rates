# Revision report: v2 → v3 (2025 section and loose ends)

Branch `paper-draft-v3`, created from `paper-draft-v2`, not pushed. `python code/run_all.py` rebuilds cleanly (exit 0). All **345 tests pass**: the 328 from v2 plus 17 new ones in `code/tests/test_episode2025.py`. `paper/main.pdf` has 55 pages, no undefined references or citations, and no [verify] markers. Only two overfull boxes remain, both under 3pt and unchanged from v2.

## Where the instructions and the data or model disagree

1. **"The dollar was flat to stronger against the renminbi" (Phase 1).** It was stronger on daily data (−0.3%) but slightly weaker on monthly averages (+0.6%). The paper says "roughly unchanged against the renminbi (−0.3 percent on daily data, +0.6 percent on monthly averages), with no sign of a depreciation against the target".
2. **"Residual relative treatment … lean[s] toward effective depreciation if ρ > ρ_D" (Phase 3).** On its own, a discriminatory unilateral tariff always *appreciates* the effective rate (Prop. 3.3). It leans toward effective depreciation only when it is met by retaliation (Prop. 3.5). That was the case in Phase 3, where China's 10% and Canada's countermeasures remained in force. The paper therefore calls the residual tariff gaps, *met by retaliation*, "retaliation configurations in miniature, [which] lean toward effective depreciation if ρ > ρ_D". It does not attribute that lean to relative treatment alone.
3. **The March 3–7 week.** The dollar fell 4.4% against the euro but only 0.3% against CAD and 1.3% against MXN. The paper reports these numbers and adds that "the data do not separate these forces". It does not attribute the week's move to Germany or to North America.

## Changes

### §4.5 (paper/sections/asymmetry.tex)
- **Classification rule.** Added: "The rule applies to a phase only insofar as the phase approximates a single configuration of the model, and in 2025 none did cleanly: each phase mixed discriminatory, retaliatory and near-uniform elements."
- **Phase 1** is retitled "unilateral tariffs on China" and rewritten as a mixed configuration:
  - It covers the 25% US tariffs on Canada and Mexico from March 4, Canada's same-day 25% surtax on C$30 billion, and the combined Canada and Mexico H.10 weight of 27.6%.
  - The US–China leg behaved as predicted.
  - Bystander weakness is consistent with the trade channel if ρ > Nρ_D.
  - The effective move "is not a test of either" a purely unilateral or a retaliatory configuration.
  - "The effective depreciation is not explained by it" has been dropped.
- **Phase 3.**
  - Names the residual treatment: China at 30% vs 10–20% for others until Nov 10, China's 10% retaliation, the US rate on non-USMCA Canadian goods rising to 35% on Aug 1, and Canada's remaining countermeasures.
  - Keeps "showed no sign of the predicted appreciation" within the phase.
  - Drops "The persistent weakness is not explained by the trade channel".
  - Keeps the facts on levels (−7.2% broad, mostly before August). It notes that the level sums all phases, including retaliation, and lists the non-trade forces as forces "that plausibly matter for the level".
- **Vietnam.** From Aug 7 to Nov 10, Vietnam's 20% against China's 30% was relative treatment in Vietnam's favour, a bystander-like position. The near-equal-tariffs argument now applies only after Nov 10.
- **Table 4.** Added CAD and MXN rows; the notes list USD/CAD and USD/MXN as H.10 rates.
- **Figure 7 caption.** Panel (b) now describes the Canada and Mexico series. "Tariffs on Canada and Mexico are not shown" has been removed. DEXCAUS, DEXMXUS and Department of Finance Canada are added to the sources.

### Abstract, conclusion, §1
- **Abstract.** Cut from 287 to **229 words**, counting each math expression as one word.
  - The 2025 sentence now reads: "Read stylistically, the 2025 retaliation phase is consistent with the model, while the near-uniform phase shows none of the predicted effective appreciation."
  - Removed to save words: the "which requires that the two elasticities differ" clause. The three-country sentence is shortened to "The symmetric economy reduces exactly to three countries."
- **Conclusion.** The statement is now general: "in a unilateral or nearly uniform configuration the trade channel predicts effective appreciation, so effective weakness in such a configuration is not explained by it. Whether an episode is such a configuration has to be checked phase by phase, because actual episodes mix unilateral, retaliatory and near-uniform elements."
- **§1 "What we do not do".** Now reads "configurations in which observed movements would not be explained by the trade channel, although an actual episode approximates such a configuration only partially." §1.1 makes no episode-specific "not explained" claim, so it is unchanged. Its April 2 sentence and the Ostry et al. description are factual.
- **README.** The 2025 results line is updated to match.

### [verify] markers
- **Johnson (1953).** The marker is removed. The bib entry matches the published article: *Review of Economic Studies* 21(2), 142–153, doi 10.2307/2296006. The page range and issue were confirmed via a secondary listing; the full text was not retrieved.
- **German fiscal announcement.** The marker is removed. The citation stays Euronews (`ripper2025`). Reuters is not reachable from this environment, the Federal Finance Ministry's April 2025 Monatsbericht article returned HTTP 503, and no Bundesbank or exploratory-paper source dated March 4 could be confirmed.

## Data and code
- `code/data/fetch_fx_2025.py` now fetches FRED **DEXCAUS** and **DEXMXUS** (cached in `data/raw/fx2025/`, documented in its README). It adds `usd_per_cad` and `usd_per_mxn` to the monthly and daily processed files. All previously reported numbers are unchanged.
- `code/checks/episode2025.py` adds the CAD and MXN rows, a `week_mar3_7` block (Feb 28 close to Mar 7 close) and `h10_weight_2025_pct` to `code/results/episode2025.json`.
- **`data/raw/tariffs2025/tariff_timeline.csv`** gains three series, each row with its source URL. They are documented in the README.

  | Series | Changes during 2025 | Sources |
  |---|---|---|
  | `us_on_canada` | 25 from Mar 4 (EO 14193); USMCA goods exempt from Mar 7 (EO 14231); 35 from Aug 1 (EO 14325) | Federal Register |
  | `us_on_mexico` | 25 from Mar 4 (EO 14194); USMCA goods exempt from Mar 7 (EO 14232); unchanged through 2025 | Federal Register |
  | `canada_on_us` | 25 on covered goods: C$30B from Mar 4; +C$29.8B from Mar 13; autos from Apr 9; C$44.2B removed Sep 1 (steel, aluminium, autos remain) | Department of Finance Canada |

  From Mar 7, `rate_pp` for the US series is the rate on non-USMCA goods only (energy and potash 10%). `canada_on_us` records coverage changes as rows with an unchanged rate.
- **Figure 7(b)** plots US on Canada (black, non-USMCA) and Canada on US (grey, covered goods). Mexico equals Canada until Aug 1, which the caption explains; it is not plotted separately.
- **New tests**, in `code/tests/test_episode2025.py` (17):
  - timeline well-formedness for every series: baseline row, ordered dates, a source URL on every non-baseline row;
  - key dates and rates (Canada, Mexico, China);
  - the sign convention;
  - the Mar 3–7 window dates.

## New numbers (% change, positive = dollar depreciation)

**Dollar change against CAD and MXN, by phase (Table 4):**

| | Unilateral (monthly / daily) | Retaliation (monthly / daily) | Near-uniform (monthly / daily) |
|---|---|---|---|
| CAD | 0.2 / 1.0 | 2.7 / 2.2 | −0.7 / 0.2 |
| MXN | 1.6 / 0.6 | 1.0 / 4.5 | 3.4 / 3.5 |

**Week of March 3–7** (Feb 28 close to Mar 7 close):
- EUR 4.39
- CNY 0.67
- CAD 0.33
- MXN 1.28
- broad index 1.82
- broad ex-China 1.97

**H.10 broad-index weights, 2025** (vintage of Feb 2, 2026):
- Canada 12.776
- Mexico 14.809
- **Canada + Mexico 27.585**
- China 10.897

**December 2025 vs the January 2025 average:** CAD 4.3, MXN 13.6. These are not used in the text.

## Not done
- Section 232 product tariffs (steel, aluminium, autos) are still outside the timeline, as in v2.
- Mexico's IEEPA extensions after July 31 changed no rate, so they are not recorded as rows.
