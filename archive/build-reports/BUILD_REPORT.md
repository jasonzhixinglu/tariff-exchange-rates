# Build report: LaTeX working paper v1

*Built 2026-10-29 from `paper_draft_v1.md` and `literature_review.md` on branch `paper-draft-v1`.*

**Deliverables**
- `paper/main.pdf`: 49 pages.
  - Title page: p. 1.
  - Main text: pp. 2–28, about 27 pages.
  - References: pp. 29–32.
  - Appendices A–C: pp. 33–46.
  - Online Appendix D: pp. 47–49.
- Sources: `paper/main.tex` and `paper/sections/*.tex`.
- Bibliography: `paper/refs.bib` (85 entries).
- Figures and tables: `paper/figures/*.pdf` and `paper/tables/*.tex`.

**Build status**
- `latexmk -pdf` builds with no undefined references or citations and no BibTeX warnings.
- Two overfull boxes remain, both under 3pt.
- `aer.bst` was missing from MiKTeX. I installed the `economic` package to get it.

**Rebuilding.** `python code/run_all.py` rebuilds everything in order: unit tests, numerical checks, tables, figures and the PDF. Add `--fetch` to re-download the FX data.

---

## 0. Model version and code

I did not use the earlier code for any paper number:
- `src/tariff_exchange_rates/` is the August-draft package. It is three-country only, and its flat-σ parts are the old model.
- `robustness/model.py` implements the correct nested model.

Every number comes from a new implementation in `code/model/`:

| module | content |
|---|---|
| `nested_ces.py` | Exact N-country model as in Section 3.2 of the md. Country-specific primitives; realized-share rebate `I_i = w_i L_i/(1 − Σ s_ij τ_ij/(1+τ_ij))`; border-price trade balances. Newton solver for the N−1 trade-balance conditions. Complex-step implicit-function responses at any baseline, including positive tariffs. |
| `linear.py` | Appendix A linearization, written as general functions of baseline shares `(y_i, h_i, b_ij)`, country-specific η and ρ, and an arbitrary tariff-change matrix. Returns `dν = (−J)⁻¹F`, real-rate and welfare responses, and MML checks. |
| `closed_forms.py` | Theorem 3.2 and Propositions 3.3, 3.5 and 3.7, plus the composite bystander of Proposition 3.6. |
| `asymmetry.py` | Fixed-baseline polynomial `Q = w'·adj(−J(ρ))·F(ρ)`. Coefficients are extracted by exact interpolation and checked at two further points. Thresholds with primitives held fixed. |

**Unit tests:** `code/tests/`, 154 tests, all passing.
- **Linearization vs finite differences.** Central differences of the nonlinear solver at τ = ±1e−4 match the linearization to better than 1e−6. Cases:
  - symmetric baselines, N = 2–5;
  - random asymmetric baselines, N = 3–5, with country-specific α_T, α_D, η and ρ;
  - random, unilateral and retaliatory tariff directions.
  
  The Jacobian and disturbances also match complex-step derivatives to 1e−12.
- **Closed forms, N = 2,…,8.** All reproduced to 1e−12:
  - unilateral responses, with bystander threshold Nρ_D found by root-finding on the linear solver;
  - k-partner responses and threshold;
  - the relative-treatment condition `t_j/t̄ < 1 − Nρ_D/ρ`;
  - bilateral retaliation: dν_B = 0 and threshold ρ_D;
  - multilateral war;
  - real-rate responses and the threshold ρ*_q, which equals 4.93 at N = 3 with US-like parameters;
  - Lemma A.1, g_S and g_D, the two-country slope, and Corollary 3.4.
- **Proposition 3.6.** For all four shocks, all four (α_D, α_T, η) sets, N = 4,…,10 and ρ ∈ {1.1, 4, 9}, the composite's dν_B, dν_C and NEER match the N-country model to 1e−12. Equations (3.10)–(3.11) are also verified.
- **Ordinary-η composite thresholds:** 3.8177, 3.7648 and 3.7092 at N = 4, 5, 8. These are 3.82, **3.76** and 3.71, against the md's 3.82, 3.77 and 3.71; see §(c).
- **Lemma 4.1 (welfare) holds.**
  - Test: central finite differences of A's log indirect utility in the nonlinear model (Cobb–Douglas outer layer, CES indices, income including rebated revenue) against −m_A Σ_j b_Aj dν_j.
  - Coverage: symmetric (N = 3, 5) and asymmetric (N = 3, 4, 5) free-trade baselines; unilateral, bilateral-retaliation, multilateral-war, foreign-only and random shocks.
  - Agreement is within 1e−6 in every case.
  - I wrote the full proof (Appendix B) from the md sketch, and the lemma itself is unchanged.

Numerical check scripts are in `code/checks/`, with outputs in `code/results/*.json`:
- `appendix_c.py`
- `asymmetry_checks.py`
- `us_china_row.py`

---

## (a) [check] numbers: md value, computed value, status

| Location | md | Computed | Status / what the paper uses |
|---|---|---|---|
| §4.3 ex. (a), Q̂ | −(ρ+2.2) | −(ρ+2.2) | match |
| §4.3 ex. (b), Q̂ and root | ρ² − 2.6695ρ − 2.2579; 3.344 | ρ² − 2.6695ρ − **2.2568**; root 3.3443 (baseline solved at ρ̄ = 3.96, L_B = 0.22) | Root matches; q₀ differs in the 3rd decimal. Paper uses the computed values. |
| §4.3 ex. (c), Q̂ and roots | −ρ² + 31.83ρ − 198.53; 8.52 < ρ < 23.31 | Shares exactly as printed: −ρ² + 31.65ρ − 199.56, roots **8.69, 22.96**. The printed incomes (1, 5.118, 0.866) leave trade unbalanced by about 9e−4. With incomes rebalanced to (1, 5.126, 0.867): −ρ² + **31.53**ρ − **198.04**, roots **8.66, 22.86**. | **Does not match** to two decimals. The two-root shape is reproduced. The md's numbers were presumably computed from unrounded primitives that are not in the repo. Paper uses the rebalanced values and states the incomes. |
| Table 2 (q₂ sign grid) | "+ fills the upper-left region …" (source note (21) is not in the repo) | Recomputed on the full 9×7 grid at ρ̄ = 3.96 (`tab2_q2grid.tex`). + in the upper left with a size–weight trade-off. q₀ < 0 in every cell, no two-root cell, MML in every cell. The symmetric cell has q₂ = 0 exactly and is printed "0". | Pattern matches the md's description. Each + cell also shows its root ρ*. I could not cell-check against the original Table 1 of (21). |
| Two-root example (S_B/S_C = 2, β_AB = 0.2, β_BA = 0.9, β_CA = 0.1) | two-root case, no roots given | roots 6.29 and 15.03 | confirmed; roots added to the text |
| Table 3, w_AC = 0.75 | L_B 0.49; 2.72; 4.98 | 0.4876; 2.724; 4.982 | match |
| Table 3, w_AC = 0.85 | L_B 0.22; 2.59; 3.98 | 0.2232; 2.589; **3.975 → 3.97** | NEER column off by 0.01 (rounding; the old JSON also has 3.9749) |
| Table 3, w_AC = 0.90 | L_B 0.12; 2.52; 3.67 | 0.1225; 2.524; **3.665 → 3.66** | NEER column off by 0.01 |
| §4.5 March 2025 | RMB −0.9%, EUR −0.2% | FRED monthly avg vs 2024 avg: CNY **−0.75**, EUR **−0.06**. End of month: −0.85, −0.22. | **Not reproduced** by monthly averages. The md's values match the old Yahoo-Finance file `data/fx_data.json` exactly. Paper uses FRED monthly averages: −0.8 and −0.1. Signs and the narrative are unchanged. |
| §4.5 April 2025 | RMB −1.5%, EUR +3.4% | FRED monthly avg: CNY **−1.39**, EUR **+3.81**. End of month: −1.04, +4.89. | **Not reproduced.** Paper uses −1.4 and +3.8. The qualitative pattern is unchanged: stable to stronger against the RMB, weaker against the euro. |
| §4.5 December 2025 | EUR +8.2% | +8.23 (monthly avg) | match. Paper adds broad ex-China +2.3 and VND −3.9 (dollar stronger), both computed. |
| §4.5 China weight | China ≈ 3.8% of US tradable spending vs ≈ 28% for all foreign | Reproduced only as imports / (0.40 × US GDP): 3.76% / 27.99% (old inputs), 3.75% / 27.79% (revised). The 0.40 is the calibration's *assumed* tradable share. Measured goods absorption (GDP goods + M − X) gives 4.41% / 32.7%. | Builder note, so **not in the paper**. If the authors restore the sentence, it should say the denominator is an assumed 40% tradable share, or use the measured 4.4% / 33%. |
| App. C.1 table, ρ*(τ₀)/Nρ_D | N=3: 1.12, 1.22, 1.41; N=5: 1.23, 1.49, 2.07 | 1.116, 1.220, 1.408; 1.231, 1.486, 2.069 | match at **(α_D, α_T, η) = (0.7, 0.6, 1.5)**, the Figure 2 calibration of the derivations note. US-like gives 1.10, 1.19, 1.36; 1.23, 1.48, 2.07. Paper labels the calibration. |
| App. C.1 discrete cut | 6.23 vs 4.28 locally | 6.234 vs 4.283 | match, at (0.7, 0.6, 1.5). US-like: 7.23 vs 4.71. |
| App. C.2 unilateral, τ = 1 | 0.76 × 3ρ_D | 0.756 at (0.7, 0.6, 1.5); 0.723 US-like | match at the Figure 2 calibration; paper states both |
| App. C.2, τ = 1.45 | 2.70 (US-like) | 2.7004 | match |
| App. C.2 retaliation, τ = 1 | 1.07 × ρ_D | 1.065 at (0.7, 0.6, 1.5); 1.029 US-like | match; paper states both |
| Online App. D, sector-specific factors | 3.96 → 3.83 (γ = 0.5); 8.76 → 5.27 (γ = 2/3) | not recomputed | `\todo` in paper |
| Online App. D, imbalances | 3.96 → 4.6–5.1 (3% deficit); "tariff size dominates" | not recomputed | `\todo` in paper. The 4.6–5.1 range and the ~3.5 combined real-rate value come from `REVISION_PLAN.md`. |

**Other draft numbers I verified even though they carried no [check] tag**
- **Matches:**
  - Figure 2 vectors, all six asserted to the stated three decimals in `fig2_geometry.py`;
  - ρ_D = 1.32, 3ρ_D = 3.96, 5ρ_D = 6.60, ρ*_q = 4.93;
  - the η_C column of Table 1: 1.50, 2.46, 2.89, 3.39;
  - App. C sensitivities +3.70, +0.99, −0.20, +5.31, at (0.7, 0.6, 1.5);
  - the reversal window 5.99 < ρ < 53.8 at L_B = 2.2;
  - no reversal for ρ ≤ 1000 at L_B ≥ 2.6;
  - the ordering counterexample, 0.0792 (exact model at τ = 0.01: 0.0787);
  - κ_war's closed form against finite differences: 0.1342 vs 0.1331;
  - κ_uni ≤ 0 at all 64 points of a grid on the stated box.
- **Discrepancies:** two, listed under (c).

## (b) Bibliography: [verify] items

85 entries are in `paper/refs.bib`. The paper cites 48, and natbib prints only those. The full per-key report is in `bib_report.md` in the build scratchpad; its substance is summarized below.

**Confirmed from Crossref, publisher, NBER, CEPR or RePEc pages**
- **Classics and macro-tariff papers:**
  - Dornbusch (1974), JIE 4(2): 177–185;
  - Eichengreen (1981), JIE 11(3): 341–359, exact title added;
  - Lindé & Pescatori (2019), JIMF 95: 52–69;
  - Barattieri, Cacciatore & Ghironi (2021), JIE 129: 103417;
  - Erceg, Prestipino & Raffo (2023), AEJ: Macro 15(4): 104–140.
- **Trade-policy and IMF Staff Papers items:**
  - Winters & Chang (2000), JIE 51(2): 363–377;
  - Artus & Rhomberg (1973), IMF SP 20(3): 591–611;
  - Armington (1969), IMF SP 16(1): 159–178;
  - Johnson, REStud 21(2): 142–153, year **1953**;
  - Freund, Mattoo, Mulabdic & Ruta, published in JIE 152 (2024): 104011.
- **Previously unidentified items, now identified:**
  - ECB WP 3117: Jouvanceau, Darracq Pariès, Dieppe & Kockerols (2025);
  - BIS WP 1316: Zhao (2025);
  - PIIE WP 25-13: McKibbin, Noland & Shuetrim (2025);
  - "Känzig et al.": den Besten & Känzig (2026), NBER WP 34852;
  - Jiang et al. (2025): Jiang, Krishnamurthy, Lustig, Richmond & Xu, "Dollar Upheaval," Stanford GSB RP 4241;
  - Cardani et al. (2025): VoxEU column, 12 May 2025;
  - Fadinger et al.: CEPR DP 21855 (2026).
- **Status changes (2025–26):**
  - Kalemli-Özcan, Soylu & Yildirim: **AEA P&P 116: 47–52 (2026)**, key `kalemliozcan2026`;
  - Acharya & Laarits: NBER WP 34640 is dated **January 2026**, key `acharya2026`;
  - Ignatenko et al.: JIE 157 (2025);
  - Auray, Devereux & Eyquem's NBER paper: now *IMF Economic Review* (2026, online first).
- **Still working papers** (WP versions kept): Itskhoki–Mukhin, Ostry–Lloyd–Corsetti, Bianchi–Coulibaly, Werning–Lorenzoni–Guerrieri, Darracq Pariès et al., Li et al. (2022), and the ECB, BIS and PIIE papers.

**Not fully confirmed** (fields omitted rather than guessed)
- `fajgelbaum2026`: BPEA volume and pages not yet assigned.
- `auray2026`: online-first, no volume or pages.
- `alfaro2023`: Jackson Hole proceedings pages not found.
- `krugman1991`: pp. 9–23 taken from the old bib.
- Classic books: not checked against publisher pages.
- **`monacelli2025`** ("slides only" in the lit review): I substituted the CEPR DP 20142 paper "Tariffs and Monetary Policy". **Authors please confirm.** It is not cited in the paper text.

**Corrections to the lit review and the old bib**
- Costinot et al. (2015) is in *QJE*, not *REStud*.
- The old bib had Ostry–Lloyd–Corsetti's authors in the wrong order.
- Bond's co-author is *Constantinos* Syropoulos.
- The Alfaro–Chor VoxEU update is dated 2026.
- Ohyama's title is "On the Stability of…".

## (c) Results in the md that my computations contradict or qualify

1. **Table 1, N = 5, ordinary-η composite: 3.77 → 3.76** (exact 3.7648). The paper uses 3.76.
2. **Leading coefficient of the bystander numerator.**
   - The md (and the old draft) states c₂ = b_AB b_AC b_CA b_CB (1−h_A)(1−h_C) y_A y_C.
   - With the paper's flows f_ij = α_T(1−h_i)b_ij y_i, the coefficient is **α_T² ×** that product. Verified on 20 random baselines: ratio = 0.16 = 0.4².
   - The sign claim is unaffected. The paper now shows the α_T² factor (§4.3 and App. C.3).
3. **Example (c)** roots are 8.66 / 22.86, not 8.52 / 23.31 (see (a)). The qualitative conclusion is unchanged.
4. **Table 3 NEER thresholds:** 3.97 and 3.66, not 3.98 and 3.67. Rounding only.
5. **The 3.34 vs 3.98 discrepancy (reconciled).** Both come from the economy with β_AB = 0.2 and L_B ≈ 0.22, at US-like parameters:

   | weighting | fixed baseline (solved at ρ̄ = 3.96) | primitives fixed (baseline re-solved at each ρ) |
   |---|---|---|
   | import weights b_A (aggregate ToT, welfare-relevant) | 3.351 (3.344 with L_B = 0.22, as in ex. (b)) | 3.399 |
   | trade weights w_A (NEER) | 3.976 | 3.975 |
   | bilateral dν_C (for reference) | 2.511 | 2.589 |

   - **The gap is weighting, not method.** In this economy A imports little from B (b_AB = 0.095) but B imports a lot from A, so B's trade weight is w_AB = 0.15. The favorable move against the target therefore counts for more in the NEER than in the import-weighted terms of trade, and the aggregate ToT condition fails at a lower ρ.
   - Holding the baseline fixed versus re-solving it moves each threshold by at most 0.05.
   - **In the paper:** Table 3 gains a column with the import-weighted R_{A|B} threshold (3.97 / 3.40 / 3.20), and §4.3 explains the gap in one paragraph. The draft did not have this column, so **authors should confirm** they want it.
6. **Calibration labels in App. C and §4.3.**
   - The md's App. C numbers and the §4.3 sensitivities (+3.70, +0.99, −0.20, +5.31) are at (α_D, α_T, η) = (0.7, 0.6, 1.5). The exceptions are 2.70 at τ = 1.45 and the Table 3 numbers, which are US-like.
   - The md's build note says unspecified numbers are US-like, so I labelled each calibration explicitly and report US-like values alongside: sensitivities +4.06, +1.23, −0.32, +6.61.
7. **§4.5 factual details corrected against the official record** (`data/raw/tariffs2025/tariff_timeline.csv`, Federal Register and SCTC announcements):
   - China's February/March responses were **product-specific** (energy and agriculture, 10–15%), not absent. The text now says "without across-the-board retaliation".
   - Vietnam's 20% applied from **August 7**, not July. The July 2 deal was the announcement.
   - US rates on "most others" in late 2025 were **10–20%**: the 10% default, 15% EU all-in including MFN, 20% Vietnam. The md said 15–20%.
   - The 145% peak on China took effect **April 10**. Steps: 30 on Apr 5, 104 on Apr 9.
   - The Geneva truce took effect **May 14**.
8. **FX numbers.** The md's March/April values came from Yahoo data. Official FRED monthly averages give slightly different numbers with the same signs; see (a).
9. **Nothing in the theory is contradicted.** Every proposition, the composite reduction and Lemma 4.1 check out numerically.

### US–China–ROW in the q₂ sign grid (report only; not added to the paper)

Script: `code/checks/us_china_row.py`.

**Data (2024)**
- US-reported imports by origin (Census, revised): b_US,CN = 0.135.
- China-reported imports by origin (GACC): b_CN,US = 0.063.
- ROW imports from the US and China, as residuals of US and China exports: b_ROW,US = 0.386.
- PPP GDP (IMF WEO Oct 2026): L = (1, 1.30, 4.45) for (US, CN, ROW).

**Results**
- **Grid coordinates.** S_B/S_C = 0.29 and b_AB = 0.135. With S_A = S_C = 1, β_AB = 0.239 reproduces that import share. This falls in the **q₂ > 0 ("eventual reversal") region** of Table 2, with aggregate-ToT root ρ* = **3.81**.
- **Fully calibrated three-country network.**
  - Setup: β calibrated so the balanced free-trade baseline matches all six observed origin shares at ρ̄ = 3.96; sizes from PPP; US-like α_D, α_T, η.
  - Result: q₂ > 0, q₀ < 0. The aggregate ToT condition fails for ρ > **4.66**, and the bilateral bystander threshold is 4.01. MML holds.
  - Variant with the US home share set to its measured goods-absorption value (h_US ≈ 0.68): ρ* = 4.50 and bystander threshold 3.87.
- **Reading.** US–China–ROW sits in the eventual-reversal region, but the aggregate threshold, about 4.5–4.7, is above the bilateral one and at the upper end of the central empirical range for ρ (2–4).
- **Caveats.**
  - The model baseline is balanced, while the data are not.
  - Mirror-trade gaps are large: US-reported imports from China are 440 bn, China-reported exports to the US 525 bn. Using China-reported flows would raise b_US,CN.
  - Home shares are model-implied.
- **Authors to decide** whether any of this goes in the paper.

## (d) Remaining TODOs

**`\todo` items in `paper/main.pdf`** (all in Online Appendix D, `sections/appendix_D_online.tex`):
1. Sector-specific factors: threshold 3.96 → **3.83** at γ = 0.5 (earlier draft; not recomputed).
2. Small-bystander threshold **8.76** …
3. … → **5.27** at γ = 2/3 (earlier draft, under its Vietnam calibration; not recomputed).
4. Trade imbalance: 3% deficit raises the threshold to **4.6–5.1** (not recomputed).
5. Combined real-rate, deficit-adjusted, discrete-tariff threshold **≈ 3.5** (3.55; not recomputed).

Recomputing items 1–5 needs two extensions of `code/model/`:
- a Ricardo–Viner technology, Y_T = A_T L_T^γ, with rents rebated;
- a transfer-financed imbalance.

Items 2–3 also need the old draft's Vietnam calibration.

**For the authors**
- Confirm the new Table 3 column (import-weighted threshold) and the rebalanced incomes used for example (c).
- Confirm `monacelli2025` (CEPR DP 20142); it is not cited in the text.
- **Length.** The main text is about 27 pages (pp. 2–28), slightly below the 30–35 target. The draft's content is fully rendered. I did not add material beyond the requested literature subsection.
- The Figure 7 near-uniform phase is shaded from August 7, when the framework rates took effect; the November 10 cut on China completes it. Adjust if the authors prefer November 10.
- `README.md` still describes the old three-country result: "ρ* = 3[1 + α_D(η−1) − α_T(1−α_D)] … ρ* ≈ 4" and the flat-σ "impossibility". I left it unchanged as instructed. It should be updated before circulation, since the GitHub repo is public (`literature_review.md`, bottom line 6).
- `notes/local_elasticity_representation.md` is untracked. I did not touch or commit it.
- **Data housekeeping.**
  - `data/raw/trade2024/bea_NipaDataA.txt` (12 MB) is git-ignored.
  - The FX fetch script `code/data/fetch_fx_2025.py` caches raw files under `data/raw/fx2025/`.
  - VND comes from BIS monthly data. The August 2025 monthly average is missing in the source, so the figure has a gap.
  - The H.10 China weight used is 10.897% (Feb 2026 vintage, which the Fed applies retroactively).
