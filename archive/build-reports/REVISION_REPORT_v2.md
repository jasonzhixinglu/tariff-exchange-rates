# Revision report: working paper v1 → v2

*Branch `paper-draft-v2`, created from `paper-draft-v1` on 2026-10-29. Not pushed.*

## Status

- **PDF.** `paper/main.pdf` (54 pages) builds with no undefined references or citations. Two overfull boxes remain, both under 3pt (v1 also had sub-5pt boxes).
- **Length.** The main text runs from p. 2 to p. 31, about 30 pages. The References start on p. 32, Appendices A–C on p. 36, and the Online Appendix on p. 51.
- **Rebuild.** `python code/run_all.py` rebuilds everything cleanly (exit 0). A second run reproduces every data file, result JSON and table byte-for-byte; only the PDF timestamps change.
- **Tests.** All **328** pass: the 154 from v1, plus 124 in `test_uniform.py` and 50 in `test_extensions.py`.
- **Open markers.** No `\todo` remains in the paper. Two red `[verify]` markers remain; see "Still open".

### Commits

| Commit | Content |
|---|---|
| `5067913` | Uniform-tariff helpers (`linear.own_rhoD`, `uniform_tariff`, `welfare_gradient`), their tests, and the g_C check on the Table 2 grid |
| `d991994` | `code/model/extensions.py` (Ricardo–Viner tradables and transfer-financed imbalance), its tests, and `code/checks/appendix_d.py` |
| `f5ab48d` | FX data re-based to January 2025, daily processed file, `code/checks/episode2025.py`, the phase table and Figure 7 |
| `839d9a4` | Paper text: Proposition 4.2, §4.1–4.3 framing, §4.5 rewrite, Appendix B proof, Appendix D, conclusion, intro and literature, notation, bibliography |
| `ca992af` | README results section; `run_all.py` wiring |

`paper_draft_v1.md` and `literature_review.md` were not edited. They had already been deleted at your request before this round and are in the Recycle Bin. The LaTeX sources were treated as the source of truth.

---

## Where my computations contradict the instructions

Nothing listed here was written into the paper in the form the instructions gave.

1. **"The dollar weakened by about 4% against the EUR *and the broad index ex-China* during the unilateral phase."** This is true for the euro but not for the index excluding China, which fell only about half as much (all measured from the January 2025 base):

   | Series | Jan → Mar monthly averages | Jan 31 → Apr 2 daily |
   |---|---|---|
   | EUR | +4.4% | +4.5% |
   | Broad index ex-China | +2.2% | +1.9% |
   | Full broad index | +2.1% | +1.7% |

   The paper reports the computed numbers.

2. **The phase was not purely unilateral, and almost all of its movement came in one week.**
   - US 25% tariffs on Canada and Mexico took effect on **March 4, 2025**, Canada retaliated immediately (25% on C$30bn), and USMCA-qualifying goods were exempted from March 7. Sources: [Holland & Knight](https://www.hklaw.com/en/insights/publications/2025/03/us-implements-threatened-tariffs-on-canada-mexico-and-china), [GHY](https://www.ghy.com/trade-compliance/u-s-25-tariff-on-canada-and-mexico-imports-in-effect-march-4th/). v1 said "without tariffs on third countries".
   - The week of March 3–7 alone accounts for +4.4% against the euro and +1.8% against the broad index, essentially the whole phase.
   - That same week also saw the March 4 German fiscal announcement.
   - The paper now says the phase was not purely unilateral, with one clause on Canada and Mexico, and mentions the German news in one sentence with `[verify]`.
   - Canada and Mexico are not in `data/raw/tariffs2025/tariff_timeline.csv` or Figure 7(b); the caption now says so. You may want to add them.

3. **The full broad index also weakened in Phase 1.** That is, effective weakness that *includes* China. Under the symmetric standard you asked for, this is "not explained by the trade channel", and the paper says so. Bilateral weakness against bystanders on its own would be consistent with ρ > Nρ_D.

4. **US–China–ROW footnote: "Both sit at the upper end of the central range of ρ estimates."**
   - The bilateral bystander threshold (3.87–4.01) is at the upper end of the range ρ ∈ [2, 4] shaded in Figure 4.
   - The aggregate terms-of-trade threshold (4.50–4.66) lies *above* that range.
   - The footnote says the aggregate threshold is "just above it".

5. **Phase 3: "observed weakness".** Within the near-uniform phase the dollar barely moved:

   | Series | Jul → Dec monthly | Aug 6 → Dec 31 daily |
   |---|---|---|
   | Broad index | −0.1% | +0.6% |
   | Ex-China | −0.3% | +0.4% |
   | EUR | +0.3% | +0.8% |

   The weakness is in *levels*: in December the dollar was 13.1% (EUR), 7.2% (broad) and 7.7% (ex-China) below January. Much of that accumulated between Geneva and August 6 (+4.9% EUR, +2.5% broad). The text therefore says the dollar "did not appreciate" as the model predicts, and that the *persistent* weakness is not explained by the trade channel. It does not claim further depreciation within the phase.

6. **The proposition can be stated more strongly than suggested.**
   - Under MML, (−J)⁻¹ is nonsingular and nonnegative, so every row has a positive entry. If A imports from every partner, F < 0 entrywise, and so dν < 0 strictly *without* irreducibility.
   - The proposition states "strictly against every partner if A imports from all of them or J is irreducible".
   - The margin ρ_D^A uses A's realized home share h_A, not α_D. These coincide at the symmetric point.

7. **Appendix D: "diminishing returns lower the threshold" holds, but the v1 mechanism was wrong.**
   - v1 said upward-sloping export supply loads diverted demand onto the bystander's price.
   - In this model, with Cobb–Douglas preferences and the tradable price fixed at one in own currency, tradable employment at a balanced free-trade baseline is L_T = γα_T L/(γα_T + 1 − α_T), independent of exchange rates. The bystander's export supply therefore does **not** respond at the margin, and J is only rescaled.
   - The effect runs through A's own income. Rebated revenue raises demand for non-tradables, pulls labor out of tradables and, with γ < 1, raises A's wage and P_N. A's nominal spending rises 6.25% instead of 4% per unit tariff at γ = 0.5, which acts like a smaller ρ_D (3.825/3 = 1.275 vs 1.32).
   - The text was rewritten accordingly.
   - Caveat: a Ricardo–Viner model in which the tradable price can move against the wage could behave differently. That is not what this specification does.

8. **Table numbering.** The new phase table is Table 4 in the main text (§4.5), not "Table 6"; LaTeX numbers it by position.

9. **Minor.** The instruction's "(A.3)" corresponds to the paper's Eq. (A.1) (`eq:linear`), and its "Eq. (2.4)" to `eq:signrule`.

---

## 1. Uniform tariffs and the welfare gradient

### Verification

- **Closed form.** F_j = −f_Aj ρ_D^A holds to 1e−12 on 60 random asymmetric baselines with country-specific parameters (N = 3, 4, 5; `test_uniform_disturbance_closed_form`). It also matches the complex-step derivative of the exact model's trade balances (`test_uniform_disturbance_exact_model`).
- **Signs.** On the same 60 baselines: every entry of F < 0, every entry of dν < 0, and welfare change > 0 (`test_uniform_tariff_signs`).
- **Stress test** (not in the suite). On 1,500 random draws (N = 3–7, η ∈ (0.2, 5), ρ ∈ (0.3, 15), α_T, α_D ∈ (0.05, 0.95), log-normal sizes), 1,229 satisfied MML, with **zero violations**. At 603 of them at least one partner-specific component g_j was negative.
- **Example (b).** At ρ = 5, g_B < 0 < g_B + g_C (`test_component_can_be_negative`).

### Paper changes

- **§4.1.**
  - Eq. (4.3) defines the welfare gradient g_j = −m_A R_{A|j}.
  - **Proposition 4.2 (Uniform tariffs)** follows Lemma 4.1, with a proof sketch.
  - New discussion: the uniform tariff switches off cross-origin substitution; components need not be positive; with N = 3, g_B < 0 implies g_C > 0.
  - The old bold sentence is now explicitly restricted to the symmetric benchmark.
  - New paragraph, "Relation to optimal-tariff theory".
- **§4.2.**
  - The condition is restated as "every component g_B > 0" versus "the proposition guarantees only the sum".
  - The "always reduces to three-country form … exact for any configuration" passage is toned down to one sentence: it holds by the definition of R̄^B_{−B}. The same tone-down is applied in §4.4.
- **§4.3 Takeaway.** Adds that the same country gains from a uniform tariff, and that g_C > 0 in the "+" cells beyond the root. It ends with the bold sentence: "The gains from protection are guaranteed only for uniform protection; discrimination can backfire."
- **Appendix B.** Full five-step proof of Proposition 4.2, plus a replication note.
- **Abstract and intro.**
  - The intro's "Asymmetry" paragraph gains one sentence.
  - The abstract gains a clause on uniform tariffs; it is 281 words, down from 290.
- **§1.1.** One sentence on Johnson (1953), Broda, Limão and Weinstein (2008) and Costinot et al. (2015).

### Literature claims

All three entries were already in `refs.bib`, and their fields were re-verified (IDEAS, AEA, and the QJE PDF). Claims made in the text:

- **Johnson (1953)** shows that a country with sufficient monopoly–monopsony power can remain better off than under free trade even after retaliation. **Marked `[verify]`.** This is confirmed only through a secondary source (Syropoulos 2002, RES, abstract); the original was not accessible. The small-tariff gain itself is presented as the classic argument that Johnson starts from, not as his result.
- **Broda, Limão and Weinstein (2008).** Countries not bound by WTO commitments set higher tariffs on goods whose foreign export supply is less elastic. Confirmed from the abstract. Their optimal tariff is product-level, and their derivation assumes equal tariffs across exporters of a good.
- **Costinot, Donaldson, Vogel and Werning (2015).** In a two-country Ricardian model with a continuum of goods, optimal import tariffs are uniform across goods. Confirmed from the abstract.
- **Bagwell and Staiger (1999, 2002).** Nondiscrimination confines a country's tariffs to a single terms-of-trade channel. Confirmed through their abstract and the NBER w22087 chapter.
- **Not written:** any claim that the literature shows *optimal partner-specific tariffs* follow export-supply elasticities. No source supporting it could be confirmed. Gatsios (1990) and Horn & Mavroidis (2001) look relevant but could not be read.

### Optional: g_C on the Table 2 grid (report only)

- **"+" cells (29).** g_C > 0 for every ρ ∈ [1, 60]: a tariff on the bystander would always pay. This is guaranteed where g_B < 0 by the proposition with N = 3, and it holds for all ρ in these cells.
- **"−" cells.** In many of them, g_C becomes negative at high ρ (roots between 3.3 and 51). There the bystander C is the relatively small, low-weight partner. Example roots by (L_B/L_C, β_AB):

  | (L_B/L_C, β_AB) | g_C root |
  |---|---|
  | (1.0, 0.9) | 3.75 |
  | (2.0, 0.8) | 3.98 |
  | (5.0, 0.1) | 12.28 |

  The full list is in `code/results/asymmetry.json` (fields `qC`, `gC_roots`, `gC_positive_all_rho`).
- **Uniform tariff.** Q_{A|B} + Q_{A|C} < 0 for all ρ ∈ [1, 60] in every cell (`uniform_negative_all_rho`).

---

## 2. The 2025 reading

### Data and figure

- **Base.** `code/data/fetch_fx_2025.py` now bases every deviation on the **January 2025 average** of daily observations (VND: BIS January monthly average). It also writes `data/processed/fx2025_daily.csv`.
- **Figure 7(a).** Re-based, with the **full broad index** (solid black, square markers) next to the ex-China series. The y-label and caption state the base.
- **Phase dates.** Now set by announcements, for the figure shading and the table alike:

  | Phase | Dates | Anchor |
  |---|---|---|
  | Unilateral | Feb 1 – Apr 2 | EO 14195 signed; reciprocal announcement |
  | Retaliation | Apr 3 – May 12 | Geneva statement |
  | Near-uniform | Aug 7 – Dec 31 | Framework rates in force |

  v1 used effective dates (Feb 4 – Apr 4, Apr 5 – May 13).
- **Phase table** (`code/checks/episode2025.py` → `paper/tables/tab6_phases.tex`; Table 4 in §4.5). The "daily" change runs from the last close before the phase to the last close in it. The "monthly" change runs from the month before the phase to its last full month. VND has no daily series, so its daily column uses BIS end-of-month values (flagged in the table).

  | % (+ = USD depreciation) | Unilateral mo. | daily | Retaliation mo. | daily | Near-uniform mo. | daily |
  |---|---|---|---|---|---|---|
  | EUR | 4.4 | 4.5 | 3.9 | 2.2 | 0.3 | 0.8 |
  | CNY | 0.6 | −0.3 | −0.7 | 0.9 | 1.9 | 2.7 |
  | VND | −1.8 | −2.1ᵃ | −0.5 | −0.5ᵃ | 0.0 | 0.5ᵃ |
  | Broad index | 2.1 | 1.7 | 1.7 | 2.3 | −0.1 | 0.6 |
  | Broad ex-China | 2.2 | 1.9 | 2.0 | 2.5 | −0.3 | 0.4 |

- **US tariff on China after Geneva.** `tariff_timeline.csv` already had 30% (May 14 – Nov 10), then 20%, and Figure 7(b) was correct. The **text** was wrong ("about 20 percent") and now says 30% falling to 20% on Nov 10. The Vietnam paragraph now says Vietnam's 20% was below China's 30% and equal to China's rate after Nov 10.

### Narrative

- **Standard.** §4.5 opens by defining "consistent with" and "not explained by" and applying them in both directions. The phrasings "attribute … to trade fundamentals" and "refuses to attribute", and the bolded Phase 3 sentence, were removed. Same fixes in the intro ("What we do not do"), §1.1 and the conclusion.
- **Phase 1.**
  - States the two firm predictions (effective appreciation, appreciation against the target) and the conditional one (bystander depreciation iff ρ > Nρ_D).
  - Reports the data: EUR +4.5%, ex-China +1.9%, CNY −0.3%, full broad index +1.7%.
  - Bystander weakness is called consistent with the trade channel at high ρ; effective weakness is called not explained by it.
  - One sentence on the March 3–7 concentration and the German package (Ripper 2025, Euronews, `[verify]`).
- **Phase 2.** Argument kept, with numbers recomputed: CNY +0.9% daily / −0.7% monthly; EUR +2.2–3.9%; ex-China +2.0–2.5%.
- **Phase 3.** "Did not appreciate", with the level gaps versus January and the interim build-up. The persistent weakness is "not explained by the trade channel".
- **Vietnam.** Recomputed: +3.2% dollar appreciation against the dong from January to December, nearly all of it by July, and flat within Phase 3 (0.0 to +0.5).
- **US–China–ROW footnote** in the "China's size does not" bullet, from `code/checks/us_china_row.py`:
  - grid placement: L_B/L_C = 0.29, b_AB = 0.135, q₂ > 0;
  - calibrated network: aggregate threshold 4.66 (common α_D) or 4.50 (measured US home share 0.673); bystander threshold 4.01 or 3.87;
  - caveats in one sentence, and an explicit "places the episode on the map; not a calibration of exchange rates".
- **Abstract.** The 2025 sentence now says the retaliation phase is consistent with the logic, while the dollar's effective weakness under unilateral and near-uniform tariffs is not explained by the trade channel.

---

## 3. Appendix D

### Model (`code/model/extensions.py`)

- **Technology.** Y_T = A_T L_T^γ; w = γ A_T L_T^(γ−1); P_N = w/A_N; labor mobile, L_T + L_N = L.
- **Income.** Y_T + P_N Y_N, plus rebated revenue on realized shares. Rents (1−γ)Y_T are rebated.
- **Transfer.** T_i is fixed in A's currency with Σ T_i = 0. Expenditure equals income plus the transfer.
- **Equilibrium.**
  - Non-tradable clearing in every country.
  - TB_i + T_i = 0 for i ≠ A.
- **Welfare.** Uses expenditure.

### Tests

- γ = 1 and T = 0 reproduce `nested_ces` (allocations, ν, local responses, J) to 1e−12, at symmetric and random N = 3, 4, 5 baselines, with and without tariffs.
- The implicit-function-theorem linearization matches central finite differences (step 1e−4, tolerance 1e−6) for γ ∈ {0.5, 2/3}, nonzero transfers, and both together.

### Numbers

US-like parameters, N = 3, all else symmetric. Every case has exactly one threshold on ρ ∈ [1.05, 60], MML holds there, and the crossing runs from − to +.

| Item | v1 | v2 |
|---|---|---|
| D.2 symmetric point, γ = 0.5 | 3.83 [TODO] | **3.83** (3.825); also 3.88 at γ = 2/3 |
| D.2 small bystander, γ = 1 | 8.76 [TODO; old "Vietnam" calibration] | **4.98** (L_C = 0.1) |
| D.2 small bystander, γ = 2/3 | 5.27 [TODO] | **4.43**; also 4.19 at γ = 0.5 |
| D.3 3% deficit, marginal threshold | 4.6–5.1 [TODO] | **4.94** (B pays), **4.61** (C pays) |
| D.3 combined (real rate, deficit, τ = 1.45) | ≈ 3.5 (3.55) [TODO] | **3.42** (C pays) – **3.64** (B pays) |
| Reference: nominal discrete threshold, τ = 1.45 | 2.70 balanced | 2.70 balanced; 2.94–3.07 with deficit |
| Reference: real marginal threshold | — | 4.93 balanced (= `closed_forms.rho_q_star`); 5.64–6.33 with deficit |
| Reference: real discrete threshold, balanced, τ = 1.45 | — | 3.19 |

Deficit sensitivity:

| Imbalance | B pays | C pays |
|---|---|---|
| 1% deficit | 4.21 | 4.14 |
| 3% surplus | 3.46 | 3.56 |

### Qualitative claims

- **"Diminishing returns lower the threshold."** Holds, with the new mechanism (contradiction 7 above). The effect is modest at the symmetric point and larger for small bystanders, as v1 said.
- **"Tariff size dominates."** Holds. The deficit raises the marginal threshold, but at τ = 1.45 the combined real-rate threshold (3.42–3.64) stays below 3ρ_D = 3.96.
- **New deficit mechanisms in the text:**
  - B pays: C's share of A's imports falls from 0.50 to 0.45, and C's sales to A fall from 0.50 to 0.39 of its exports.
  - C pays: the bystander is smaller in A's currency.
  - Financing the deficit requires A to appreciate about 15% against the payer and 8% against the third country.

No extension proved infeasible, and no subsection was cut.

---

## 4. Smaller fixes

- **Conclusion.** Now reads: under bilateral retaliation the belligerents' bilateral rate is unchanged, and each depreciates against bystanders and in effective terms once ρ > ρ_D; only in a multilateral war does the tariffing country depreciate against everyone. The abstract ("both belligerents depreciate in effective terms") and intro ("depreciate against every bystander and in effective terms") were already correct.
- **§1 / §1.1 redundancy.**
  - Intro paragraph 2 is cut to one clause pointing to §1.1; the Ostry et al. sentence is kept.
  - The overview paragraph at the start of §1.1 is reduced to one framing sentence.
  - The detailed discussion stays in "The 2025 dollar".
- **Notation.** Country size is L throughout: Table 2 header, its notes, example (b), the two-root example, and the "Which asymmetries matter" paragraph. L_i is defined once in §3.2 as the labor endowment ("its size") with L_T + L_N = L. The internal JSON key `S_B` in `asymmetry.json` is unchanged.
- **§4.2.** The three-country form is toned down to one sentence; same in §4.4.
- **README.md.**
  - The results section is rewritten: no "ρ* ≈ 4", no flat-σ "impossibility". It states the Nρ_D / ρ_D thresholds, the uniform-tariff result and the 2025 reading, and points to `paper/main.pdf` and `code/run_all.py`.
  - The old package, notebooks, dashboard and calibration sections are kept under "Legacy code (earlier three-country draft)", because the dashboard and `src/` still exist.
  - **Please review before pushing.** The legacy calibration tables (σ by country) describe the old flat-σ exercise.
- **Author decisions applied.**
  - Table 3 R_{A|B} column and its §4.3 paragraph: kept.
  - Example (c) at 8.66 / 22.86: kept.
  - `monacelli2025`: removed from `refs.bib` (it was not cited).
  - Figure 7 shading from Aug 7: kept.
- **Bibliography.**
  - Added `ripper2025` (Euronews, March 4, 2025; headline, author and date confirmed from the page).
  - Added `\usepackage{xurl}` so its URL breaks.
  - Added a `\verify` macro (red "[verify]").

---

## Every number in the paper that changed (v1 → v2)

Unchanged: §3, Appendices A and C, Tables 1–3 and C.1–C.3, and Figures 1–6. Changes are in the abstract, §4.1–4.5 and Appendix D.

| Location | v1 | v2 |
|---|---|---|
| **Abstract** | | no numbers; the 2025 sentence is reworded |
| **§4.5 base** | 2024 average | January 2025 average |
| **§4.5 phase dates** | Feb 4–Apr 4; Apr 5–May 13 | Feb 1–Apr 2; Apr 3–May 12 |
| **Phase 1**, USD vs CNY | −0.8% (March vs 2024) | −0.3% (Jan 31 → Apr 2) |
| **Phase 1**, USD vs EUR | −0.1% (March vs 2024) | +4.5% |
| **Phase 1**, broad ex-China | — | +1.9% |
| **Phase 1**, full broad index | — | +1.7% |
| **Phase 1**, week of Mar 3–7 | — | +4.4% EUR, +1.8% broad |
| **Phase 2**, USD vs CNY | −1.4% (April vs 2024) | +0.9% daily / −0.7% monthly |
| **Phase 2**, USD vs EUR | +3.8% (April vs 2024) | +2.2–3.9% |
| **Phase 2**, broad ex-China | — | +2.0–2.5% |
| **Phase 3**, US tariff on China | "about 20 percent" | 30% (May 14 – Nov 10), then 20% |
| **Phase 3**, USD vs EUR in December | +8.2% (vs 2024) | +13.1% (vs January) |
| **Phase 3**, broad ex-China in December | +2.3% (vs 2024) | +7.7% |
| **Phase 3**, full broad index in December | — | +7.2% |
| **Phase 3**, within-phase broad index | — | −0.1% to +0.6% |
| **Phase 3**, Geneva → Aug 6 | — | +4.9% EUR, +2.5% broad |
| **Vietnam**, USD vs VND | −3.9% in December (vs 2024) | −3.2% Jan → Dec; within Phase 3 0.0 to +0.5% |
| **Vietnam vs China** | "about equal to the late-2025 rate on China" | below China's 30%; equal after Nov 10 |
| **US–China–ROW footnote** | — (BUILD_REPORT only) | aggregate threshold ≈ 4.5–4.7; bystander threshold ≈ 3.9–4.0; central range [2, 4] |
| **New Table 4** (phase table) | — | the 30 entries above |
| **Figure 7(a)** | four series vs 2024 | five series (adds the full broad index) vs January 2025 |
| **Appendix D.2** | 3.83 [TODO] at γ = 0.5 | 3.83; 3.88 at γ = 2/3 |
| **Appendix D.2** | 8.76 → 5.27 [TODO] | 4.98 → 4.43 (γ = 2/3), 4.19 (γ = 0.5), at L_C = 0.1 |
| **Appendix D.2** | — | 6.25% vs 4% spending response |
| **Appendix D.3** | 4.6–5.1 [TODO] | 4.94 / 4.61 |
| **Appendix D.3** | — | appreciation of 15% / 8%; shares 0.50 → 0.45 and 0.39; sensitivities 4.21, 4.14, 3.46, 3.56 |
| **Appendix D.3** | ≈ 3.5 (3.55) [TODO] | 3.42–3.64 |
| **Appendix D.3** | — | 2.94–3.07; 4.93; 5.64–6.33; 3.19 |
| **§4.1 / Appendix B (new)** | — | tolerance 10⁻¹²; 60 random baselines, N = 3, 4, 5 |

---

## Still open

1. **`[verify]` on the Johnson (1953) characterization** (§4.1, "Relation to optimal-tariff theory"). It needs a check against the original article.
2. **`[verify]` on the German fiscal sentence** (§4.5, Phase 1). The source is real and the date is confirmed (Euronews, Kirsten Ripper, March 4, 2025). The marker is there because you asked for one; a more authoritative source (official, ECB or a working paper) may be preferable.
3. **Canada and Mexico** (March 4 tariffs, Canadian retaliation) are mentioned in the text but are not in the tariff timeline or Figure 7(b).
4. **README** needs review before pushing; see §4 above.
5. **Unrecomputed v1 numbers.** All main-text numbers outside §4.5 are unchanged from v1 and were re-verified by the existing tests and checks. None were recomputed by hand.
