# Revision Change Log

Companion to `REVISION_PLAN.md` (which tracks *what needs doing and why*). This file records, in specific terms, **every change actually made** during the referee-response revision — code, data, paper, notebooks, dashboard — and is updated continuously as the revision progresses. Newest entries at the bottom of each section. Commit hashes refer to the `main` branch.

---

## 1. Code changes

### 1.1 `src/tariff_exchange_rates/economy.py` — corrected flat-CES model (commit `3fc971a`, 2026-08-22)

Three changes to `compute_allocation()`:

1. **Tariff-revenue / income formula (equilibrium-relevant bug fix).**
   - *Before:* `income = wages * labor / (1 − Σ_j alpha_T[j] · τ_ij/(1+τ_ij))` — the rebate wedge used the fixed preference weights `alpha_T[j]`.
   - *After:* the wedge uses **realized, price-dependent CES expenditure shares**: `shares_T[i,j] = alpha_T[j]^σ Pc[i,j]^(1−σ) / Σ_k alpha_T[k]^σ Pc[i,k]^(1−σ)` (computed in log space via `logsumexp`), giving `income = wages · labor / (1 − alpha_T_total · Σ_j shares_T[i,j] · τ_ij/(1+τ_ij))`. Still closed-form (shares don't depend on income).
   - *Why:* the old formula is exact **only at σ = 1**. At σ ≠ 1 it mismeasures tariff revenue and shifted equilibria — producing a spurious sign reversal of log e_AC at σ ≳ 1.9 (the paper's claimed headline result). Corrected equilibria match the referee's independent replication to 4 decimal places at σ = 0.5/1/2/5.
   - *Effect (symmetric baseline, isolated τ_AB = 1, log e_AC):* σ=0.5: −0.1488 → −0.1133; σ=2: **+0.0048 → −0.0163**; σ=5: **+0.0218 → −0.0013**. σ=1 unchanged (−0.0488).

2. **Budget consistency of the CES demand branch (levels-only fix; no effect on equilibria).**
   - *Before:* at σ ≠ 1 tradable spending summed to `income` (instead of `alpha_T_total · income`), so total spending was `(1 + alpha_N) · income`; the CES branch was discontinuous with the CD branch at σ = 1 by the factor `1/alpha_T_total` (= 4/3 at the symmetric baseline).
   - *After:* `demand_T = alpha_T_total * shares_T * income / Pc`. Budget exhausts exactly; branches continuous. TB=0 loci unchanged (uniform scaling cancels).

3. **Tradable price index (reported RERs only; no effect on equilibria).**
   - *Before:* CES index used unnormalized weights `alpha_T[j]^σ` — not equal to 1 at unit prices, and divergent as σ → 1.
   - *After:* weights normalized within the bundle (`b_j = alpha_T[j]^σ / Σ_k alpha_T[k]^σ`); index is HD1, equals 1 at unit prices, and its σ → 1 limit is the CD index with weights `alpha_T/alpha_T_total`. Removed a duplicate `alpha_T_total` assignment.

### 1.2 `dashboard/src/lib/modelJs.js` — JS port of fix 1.1 (commit `3fc971a`)

Same three corrections mirrored: added `ALPHA_T_TOTAL`; shares computed first (`shares[i][j]`), income wedge uses `ALPHA_T_TOTAL * shares[i][j]`, demand scaled by `ALPHA_T_TOTAL`. Verified exact parity with Python trade balances at test points (e.g. σ=2, (e_AB, e_AC) = (0.8, 0.95): TBs agree to full printed precision).

### 1.3 `tests/test_economy.py` — new (commit `3fc971a`)

15 tests pinning the corrected flat-CES model:
- budget constraint holds at σ ∈ {0.5, 1, 2, 8};
- CES branch continuous with CD branch at σ = 1 (demand and price level);
- price index homogeneous of degree one;
- Walras (TB_A = 0 at solved equilibrium);
- σ = 1 equilibrium unchanged by the fix (−0.2719, −0.0488);
- corrected equilibria match the referee's replication values at σ = 0.5/1/2/5 (abs tol 5e-5);
- **no sign reversal**: log e_AC ≤ 0 for σ ∈ {0.3, …, 50} (numerical footing for the impossibility proposition);
- finite-difference slope equals analytic −1/(12σ) at the paper's calibration (rel tol 1e-3);
- two-country closed form e(τ) = [1/(1+τ)]·[1/(1 − α_TB·τ/(1+τ))] reproduced by the solver at τ ∈ {0, 0.2, 0.5, 1, 1.45}.

### 1.4 `scripts/verify_referee_claims.py` — new (commit `3fc971a`)

Reproduces and asserts every quantitative claim in the referee report plus repo-specific findings: §1 income-bug before/after table; §2 impossibility at the paper's calibration (slope −1/(12σ), gap ρ*−σ ≡ +0.50); §3 nested-model threshold (analytic vs numeric slope, ρ* grid, size table 8.76/4.32/4.24/3.78, large-tariff thresholds — both cumulative (referee's §5.6 definition, reproduced exactly: 3.55/3.19/2.86/2.70 at τ=0.2/0.5/1.0/1.45) and marginal (3.23/2.69/2.26/2.07)); §4 trade-war comparative static (decreasing in flat σ, increasing in nested ρ); §5 income-fix effect on the published calibration; `--symbolic` re-derives ρ* via sympy from our own model setup. Includes a standalone nested-model implementation used as the reference for the package module.

### 1.5 `src/tariff_exchange_rates/nested.py` — new (commit `7c9df2d`)

Nested (η, ρ) three-country model, **plain-weight CES convention** (matching the paper's stated utility):
- `compute_allocation_nested(params, exchange_rates, tariffs)`: CD outer (`alpha_T`) → CES(η) over {home, import bundle} with per-country home share `alpha_D` → CES(ρ) over foreign origins with weight matrix `beta` (rows sum to 1; default 1/(n−1)). Tariff revenue from realized shares; returns same structure as the flat model plus `shares`.
- `solve_3country_nested`: multi-start hybr solver with size-aware initial guess `log(L_i/L_0)`.
- `rho_star_symmetric(alpha_D, alpha_T, eta)` = 3[1 + α_D(η−1) − α_T(1−α_D)].
- `rho_star_numeric(...)`: general threshold by Brent root-finding; `cumulative=False` (marginal: slope zero at τ0) or `cumulative=True` (total change zero over [0, τ0] — the referee's §5.6 definition).
- `d_log_eAC_dtau`, `make_params_nested` helpers.
- Exported from `__init__.py`.

### 1.6 `tests/test_nested.py` — new (commit `7c9df2d`)

18 tests: budget/shares/Walras consistency; **collapse to the flat model at ρ = η** (weight-convention conversion `alpha_flat ∝ w^(1/σ)`, equilibria equal to 1e-8); collapse reproduces the paper's symmetric flat values; ρ* spot values (3.96; 2.50; gap +0.50); analytic slope (ρ − ρ*)/(3[3α_D(η−1)+ρ+1]) matches numeric to 1e-6 at four parameter points; genuine reversal at ρ = 4.5 > ρ* = 3.96 (log e_AC > 0 while log e_AB < 0); referee size table; large-tariff cumulative thresholds; trade war increasing in ρ with spot value +0.2006 at ρ = 6.

### 1.7 `scripts/derive_general_threshold.py` — new (commits `7c9df2d`, rewritten `bda4b3d`)

General-baseline threshold via **share-based linearization** (hat algebra). First version (direct symbolic Jacobian at a general wage baseline) was abandoned: terms like v^(1−ρ) make the numerator non-polynomial in ρ. Final version linearizes the two balanced-trade conditions in (dν_B, dν_C, dτ) with nested-CES share responses expressed through baseline observables:

- Observables: common-currency incomes y_i (**note:** must be e_Ai·w_i·L_i — an own-currency version of this was a bug caught by validation, off by ~1.5 on the Vietnam threshold), home shares h_i of tradable expenditure, import-bundle origin shares b_ij, α_T.
- Result: d log e_AC/dτ|₀ = N(ρ)/D, N quadratic in ρ, with **c₂ = b_AB·b_AC·b_CA·b_CB·(1−h_A)(1−h_C)·y_A·y_C > 0** (verified symbolically) ⇒ ρ* is the larger root and "reversal iff ρ > ρ*" holds at any baseline. All coefficients share the factor b_AB(1−h_A)y_A; c₀ contains the factor 1 + h_A(η−1) − α_T(1−h_A) (the symmetric ρ*/3 with h_A in place of α_D).
- Symmetric reduction (h_i = α_D, b_ij = 1/2, y_i = 1) equals (ρ − ρ*)/(3[3α_D(η−1)+ρ+1]) exactly (sympy-verified).
- Validation: hat-algebra ρ* vs brute-force at (α_D=.80, α_T=.40, η=1.5, L_B=1.21): Vietnam 8.7588/8.7588, EU 4.3222/4.3222, equal 4.2383/4.2383, ROW 3.7829/3.7829 (diffs ≤ 2.3e-5).
- Factored quadratic coefficients written to `output/general_threshold_symbolic.txt` (paper appendix source).

---

## 2. Data & artifact regeneration (commit `4451c62`, 2026-08-22)

All under the corrected model:

| Artifact | Change |
|---|---|
| `data/theory_grid.json` | 12,288 equilibria re-solved (4^6 tariff grid × σ ∈ {1,2,8}, symmetric baseline). Isolated-tariff points: max e_AC = 0.999972 — **no reversal anywhere**. 1 of 27 war points (τ_AB=1.5, τ_BA=0.25, σ=1) has e_AC = 0.9955 < 1: lopsided wars can appreciate the heavy tariffer vs C. |
| `data/calibration_panel.json` | 8 configs re-solved. Notable Regime-2 Δe_AC changes: EU +7.29→+5.58, VNM +6.38→+4.66, **ROW +0.87→−0.14 (sign flip)**, Taiwan +22.81→+19.24, India +22.10→+18.43, Canada +24.05→+21.22. |
| `output/*.pdf` and `Exchange_Rate_Tariffs/*.pdf` | All Section 2–4 figures regenerated (calibration figure via `scripts/regenerate_calibration_figure.py`; locus figures via re-executed section 3 notebook) and copied into the paper directory (untracked by git per `.gitignore`). |
| `dashboard/public/data/*` | Synced from `data/`; `dashboard/dist` rebuilt (`npm run build`). |
| `scripts/regenerate_calibration_figure.py` | Label fix `σ=8 → σ=6` for the EU config (pre-existing uncommitted edit by the author, committed alongside since the regenerated figure uses it). |

## 3. Notebook changes (commit `4451c62`)

`notebooks/section3_three_country_model.ipynb` — narrative corrected where it asserted the spurious reversal, then re-executed end-to-end (all figures regenerated):
- intro cell: added a revision note explaining the income-formula bug and the impossibility result; removed the "breaks down" framing;
- §4.4 markdown: kept the two-forces exposition; conclusion changed from "sign depends on σ" to "diversion never dominates under a common elasticity";
- σ=2 cell: comment/title changed from "diversion dominates, A depreciates against C" to "diversion strengthens: appreciation against C shrinks toward zero"; re-executed output now e_AC = 0.9838 (was 1.0048);
- σ-scan cell: crossing detection (`crosses 1.0 near σ ≈ 1.86`) replaced by an impossibility check (`max e_AC = 0.997112 ≤ 1`); figure title updated;
- summary table: "Isolated tariff (high σ) → **Depreciates**" row replaced with "Appreciates (toward zero as σ↑)"; added the ρ* threshold statement.

`notebooks/section4_calibration.ipynb` — re-executed under the corrected model (no narrative edits yet; Phase 3 will rebuild this notebook).

## 4. Documentation changes

- `REVISION_PLAN.md` — new (commit `e07c8a0`); updated continuously (commits `3fc971a`, `4451c62`, `2171bb9`): Phase 0 complete, Phase 1 items 1.1/1.2/1.4/1.6 complete, Phase 2 items 2.1–2.3 complete; new findings recorded (§3.6 weight-convention inconsistency and mis-hit calibration targets; cumulative vs marginal large-tariff thresholds; trade-war asymmetry boundary).
- `README.md` (commit `58bcfe8`): Overview rewritten from the old claim ("trade war … reversing the conventional two-country appreciation result") to the two-result narrative (impossibility + threshold ρ*); repo-structure section updated with `nested.py`, `tests/`, and the two new scripts.
- `REVISION_CHANGES.md` — this file (2026-08-23).

## 5. New findings during the revision (beyond the referee report)

Documented in detail in `REVISION_PLAN.md` §3.1, §3.6 and Phase 0 notes; in brief:
1. **Root cause of the paper–referee discrepancy**: the tariff-revenue income formula (code bug), not just the manuscript's eq. (26)–(27) inconsistency.
2. **ROW Regime-2 sign flip** under the corrected model — removes one of the abstract's two claimed directional successes.
3. **Referee's §5.6 = cumulative threshold**; the marginal threshold is lower still. Both computed.
4. **Weight-convention inconsistency**: paper's utility (α^(1/σ)) vs paper's demand formula and code (α^σ) — coincide only at σ = 1 or symmetric weights. Under the stated utility, the symmetric impossibility boundary α_D < 1/3 is sharp (crossing at predicted σ* = 2.75) and robust to size asymmetry.
5. **Calibration targets mis-hit at σ ≠ 1** (EU config at σ = 6: realized China share 0.188 vs target 0.165) — recalibration must invert the demand system at the baseline equilibrium.
6. **Trade-war asymmetry boundary**: sufficiently lopsided wars appreciate the heavy tariffer against the bystander; near-symmetry qualifier needed for the proposition (Regime 2's 1.45/1.25 is comfortably inside the joint-depreciation region).
7. **Sufficient-statistics threshold** (ours, extending referee §5.5): the general-baseline quadratic N(ρ) with positive leading coefficient; ρ* = larger root, valid for arbitrary sizes and asymmetric preferences.

---

## 6. Paper changes (`Exchange_Rate_Tariffs/paper_draft.tex`)

Conventions: all new or modified paper text is wrapped in blue markup (`\rev{...}` for inline text, `revblock` environment for whole paragraphs/subsections; color `RevBlue`, RGB 0,0,205) so the referee and co-author can see exactly what changed. Pure deletions are recorded here rather than marked in the PDF. As of 2026-08-23 the paper directory is **tracked in git** (commit `c622821` = pre-revision baseline; `.gitignore` now excludes only `literature_review/`, compiled paper PDFs, and LaTeX build artifacts), so `git diff c622821 -- Exchange_Rate_Tariffs/paper_draft.tex` shows the full revision diff.

### 2026-08-23 — first paper tranche (Phase 4 core)

**Preamble.** Added `corollary` theorem env; `RevBlue` color, `\rev{}` macro, `revblock` environment.

**Abstract.** Fully rewritten (blue): impossibility theorem first, threshold ρ* second, near-symmetric trade war, calibration as illustration (five-of-six signs claim replaced the old "correctly predicts the direction" claim), closing inference for the 2025 attribution debate. Old abstract's "prediction is not robust … response becomes ambiguous" framing deleted.

**Introduction.**
- After the 2025-literature paragraph: added (blue) engagement with Kalemli-Özcan–Soylu–Yildirim (2025, uncertainty channel), Werning–Lorenzoni–Guerrieri (2025, cost-push), and Corsetti–Lloyd–Ostry (2025, BoE SWP 1139) — whose unilateral-vs-retaliation event-study pattern is exactly the model's configuration dependence.
- Deleted the "we challenge the two-country conventional wisdom on different grounds" paragraph and the two paragraphs following it (single-elasticity mechanism claims; old results roadmap). Replaced (blue, 3 paragraphs): equilibrium object = relative wage computed routinely by Caliendo–Parro/Ossa/Costinot–Rodríguez-Clare + PTA literature; what we add (sign characterization + impossibility + translation); impossibility intuition; nested threshold with comparative statics; trade war.
- Roadmap paragraph rewritten (blue).

**Section 2.2 (robustness).**
- Fixed cross-reference: "Section 2" → new label `sec:twocountry_cw` (Section 2.1).
- Added (blue): explicit statement that Lemma 2.2 is Marshall–Lerner, Lemma 2.1 its tariff analogue; "holds wherever Marshall–Lerner holds" framing; setup for the multilateral insufficiency point.
- Lemma 2.1: "or more generally" corrected to "or, under the weaker sufficient condition", with an explanatory clause (referee §3.8 minor).
- Closing paragraph replaced (blue): honest Marshall–Lerner statement + bridge to Section 3.

**New Section 2.3 "The Exchange Rate as a Relative Wage"** (`sec:relwage`, all blue): derivation of e ∝ relative wage ∝ terms of trade; no-nominal-anchor statement (referee §7 terminology); positioning vs quantitative trade and PTA literatures; explicit statement of the three things added (referee §3.3/§6).

**Section 3 opening.** "Robustness … its breakdown cannot be attributed to modeling choices" replaced (blue): Marshall–Lerner holds bilaterally throughout; the question is what it leaves undetermined.

**Section 3.1.2 (households/tariffs) — equation corrections.**
- Eq. (24) demand: α_Tj^σ → α_Tj (share-linear, consistent with the stated utility weights α^(1/σ)); added sentence fixing the convention.
- Price index: weights α_Tj^σ → α_Tj/α_T (normalized, =1 at unit prices).
- NEW eq. `eq:realized_shares` defining realized income shares ς_ij; income equation rewritten to use ς_ij with the statement that it is closed-form because shares are price-only; explicit note that the fixed-weight version is exact only at σ=1, with a footnote disclosing that an earlier version used the fixed-weight formula and that it generated a spurious sign reversal (referee §4.2 + our income-bug finding).
- Labor allocation equation: flat-CES denominator (with α_N^σ P_N^(1−σ)) replaced by the CD-outer form L_N/L = α_N·I/(wL).
- Market clearing: D_k corrected to the within-tradables denominator Σ_m α_Tm((1+τ)e)^(1−σ) — no α_N term (referee §4.2); demand under the α_T·I_k scaling.
- Eq. (28) trade balance: spurious e_ik removed from the export term (now C_{T_i k} at producer price); surrounding sentence corrected; import-term explanation added (tariff wedge is a domestic transfer) (referee §4.1).

**Section 3.2.2 (isolated tariff).** Third-force (home expenditure switching) added to the two-forces discussion (blue); "does not depreciate relative to C" low-σ sentence corrected; the σ=2 reversal claim ("depreciates relative to C, reversing the conventional two-country prediction") **deleted** and replaced (blue) with the corrected pattern: log e_AC = −0.11 (σ=0.5) → −0.016 (σ=2), monotone toward zero from below, asymptote-not-crossing statement with forward reference to `sec:impossibility` (referee §3.1).

**Section 3.2.3 (trade war).** Replaced closing paragraph (blue): e_AB stability flagged as knife-edge (symmetric case only; the calibration violates it) (referee §7); near-symmetry qualifier with the lopsided-war boundary (our theory-grid finding) and the note that Regime 2 (1.45/1.25) is inside the joint-depreciation region; magnitude comparative static corrected — decreasing in flat σ, increasing in nested ρ (referee §4.3); Corsetti–Lloyd–Ostry empirical anchor added.

**NEW Section 3.3 "An Impossibility Result and a Reversal Threshold"** (`sec:impossibility`, all blue):
- Proposition 3.1 (Impossibility): displayed slope −[σ(3α_D−1)+3(1−α_D)(1−α_T)]/(3[3α_D(σ−1)+σ+1]); α_D ≥ 1/3 ⇒ appreciation at every σ; −1/(12σ) at the baseline calibration; asymptote discussion; grid-verified global statement; footnote on why the point was overlooked.
- Nested (η, ρ) preferences defined; FLOR/Broda–Weinstein/Fajgelbaum empirical anchor for ρ > η.
- Proposition 3.2 (Reversal threshold): slope (ρ−ρ*)/(3[3α_D(η−1)+ρ+1]), boxed ρ* = 3[1+α_D(η−1)−α_T(1−α_D)]; stability condition stated as such (referee §5.2).
- Comparative statics; ρ* = 3.96 at US-realistic parameters.
- NEW Figure `threshold_figure.pdf` (two panels: equilibrium response vs ρ with thresholds marked and the flat-CES asymptote; ρ* vs home bias with measured-elasticity band). Generated by new `scripts/make_threshold_figure.py`.
- NEW Table `tab:rhostar_grid`: Panel A ρ* over (α_D, η); Panel B by third-country size (Vietnam 8.76 / EU 4.32 / equal 4.24 / ROW 3.78) and by tariff size (cumulative threshold 3.55/3.19/2.86/2.70) (referee §5.4–5.6).
- Third-country size paragraph: Vietnam-is-hardest point (reverses the original draft's presentation).
- Large-tariff paragraph: threshold falls with τ, local bound conservative.
- General-baselines paragraph: quadratic N(ρ), positive leading coefficient, pointer to new Appendix.

**Section 3.4 (old 3.3, mechanisms).** "our baseline CES structure captures this in reduced form through the single parameter σ" **deleted** (now false); replaced (blue) with references to Props 3.1/3.2 and the appendix threshold's dependence on expenditure shares.

**Section 4 (calibration).**
- Sign convention moved from figure notes into the text (blue) (referee §7).
- Results discussion (two paragraphs) fully rewritten (blue) with corrected share-linear model values — R1: EU (−5.39, −0.44), VNM (−8.27, −0.49), ROW (−2.76, −0.78); R2: EU (−2.50, +3.57), VNM (−3.39, +2.42), ROW (−1.81, +2.43) — honest five-of-six-signs statement, Vietnam failure tied to safe-haven flows *and* to the size result of §3.3, explicit Itskhoki–Mukhin horizon caveat, and explicit statement that world-export-share preferences understate home bias (referee §3.5, §3.6, §3.9). "Correctly predicts the direction … most salient finding" framing deleted.
- Table 2: Vietnam α_TB 0.236 → 0.235 (reconciles with appendix; referee §7).
- Appendix C: "slightly different σ values" note corrected to "same parameter values"; fit-summary paragraph rewritten (blue); all 48 model-column values in `tab:app_regimes` replaced with corrected values (blue); caption notes the recomputation.

**Conclusion.** First two paragraphs rewritten (blue): impossibility + threshold narrative, corrected calibration claim, inference payoff, Corsetti–Lloyd–Ostry, and the discipline point (single-elasticity calibrations cannot capture the mechanism).

**NEW Appendix "The Reversal Threshold at a General Baseline"** (`app:threshold`, all blue): hat-algebra linearization (share log-changes, income differential, the two dTB conditions), Proposition (general-baseline threshold) with the c₂ formula and larger-root statement, symmetric reduction, validation note, replication-package pointer.

**References (`references.bib`).** Added 13 entries: caliendo2015, ossa2014, costinot2014, bagwell1999, bond1996, ornelas2005, itskhoki2021, eaton2016, caliendo2019, corsetti2025 (BoE SWP 1139), werning2025 (NBER 33772), kalemli2025 (NBER 34728), obstfeld2025 (VoxEU). eaton2016/caliendo2019/obstfeld2025 reserved for the forthcoming §3.4 extension discussion.

**Build.** Compiles clean (pdflatex ×3 + bibtex): 39 pages, zero warnings, all citations resolved.

**Still pending in the paper** (tracked in `REVISION_PLAN.md`): Ricardo–Viner extension subsection (D1 — prototype first); Figure 2–7 compression (4.8); Figure 1 legend overlap (5.3); §4.2 (η, ρ) sourcing and grid reporting (Phase 3); matched ROW index (D2); extended FX window (D3).

### 2026-08-23 — framing memo received, assessed, and folded into the plan

- **`revision_framing_memo.md`** (author's notes on motivation/framing/contribution) copied into the repo and adopted as the controlling positioning statement — the paper's headline becomes *"the PTA literature bears directly on the tariff–exchange-rate question; we illustrate the connection with minimal theory,"* with the impossibility theorem as the story of why the connection was invisible. Full adoption/amendment record in `REVISION_PLAN.md` §4a; new work items M1–M5 and checklist entries 3.9–3.11, 4.11–4.15 added there.
- **New script `scripts/verify_framing_memo_checks.py`** resolving the memo's two computable open items:
  1. **ρ*(q) vs ρ*(e)** (memo §3.4): they differ — **ρ*(q) = 4.93 vs ρ*(e) = 3.96** at the benchmark. The tariff mechanically raises A's tariff-inclusive CPI, absorbing part of the nominal depreciation, so real depreciation against C requires more diversion. Both inside the measured cross-origin range. Goes into the paper as a result (item 4.13).
  2. **NFA robustness** (memo §3.2): the memo's claim that non-zero NFA "shifts the level but not the comparative static" is **contradicted numerically** — with TB_i = −b_i, a permanent 3% A-deficit raises ρ* from 3.96 to 4.64–5.10 (composition-dependent), 6% → 7.07, 3% surplus → 3.42. The correct defense of balanced trade is the general-baseline proposition (structure invariant, location baseline-dependent), and the US-deficit sensitivity becomes an honest calibration result (items 4.15, 3.10).
- Recorded disagreements (plan §4a): keep the impossibility theorem prominent; the general-baseline quadratic is a sufficient-statistics *feature* (it enables the memo's own pair-by-pair-diagnostic follow-up and the NFA sensitivity), not an "unenlightening root"; memo §4's four errors were already fixed in the first paper tranche.
- D3 (FX window) considered resolved by the memo's long-run-real framing: extend the window **and** frame as the transition becoming visible.

### 2026-08-24 — referee follow-up absorbed (no paper edits yet)

- **n=4 single-crossing failure demonstrated**: numeric scan of a 4-country nested model found two asymmetric configurations with double sign changes in d log e_AC/dτ over ρ. Combined with the degree argument (N(ρ) has degree n−1), the three-country scope claim is now stated as demonstrated, not rhetorical. Wording guidance in `REVISION_PLAN.md` §4a "Referee follow-up".
- **Joint thresholds computed** (deficit × real rate × tariff size): marginal ρ*(q) at 3% split deficit = 6.05 (referee's guess ~6 confirmed); cumulative at τ=1.45 = **3.55** (3% deficit) / 4.55 (6%); at τ=0.20 = 5.22. Consequence: the "inside the measured range" claim must be episode-qualified everywhere it appears (abstract/intro/§3.3/§4). Numbers recorded in the plan; to be promoted into `scripts/verify_framing_memo_checks.py` alongside the 4.13 write-up.

### 2026-08-24 — Ricardo–Viner extension (D1/M5) implemented

- **New `scripts/rv_prototype.py`**: sector-specific-factors model (Y_T = A·L_T^γ, rents rebated, labor mobile within country; 5-equation system: 3 N-clearing + TB_B, TB_C; logistic transform for L_T; analytic symmetric free-trade start L_T = γα_T L/(1−α_T+γα_T)). Validation at γ=1: reproduces baseline nested model exactly (ρ* = 3.9600; Walras and variety-clearing at machine precision).
- **Results**: ρ* falls with DRS — equal sizes 3.96 → 3.83 (γ: 1 → 0.5), cumulative τ=1.45 threshold 2.70 → 2.67; the big effect is the **compressed size gradient**: Vietnam 8.76 → 6.07 (γ=0.8) → 5.27 (γ=2/3), EU 4.32 → 4.09, ROW unchanged. Small supply-constrained third countries are partially rehabilitated as reversal venues.
- **Paper (`paper_draft.tex`)**: corrected the original draft's supply-side sentence in the mechanisms subsection — it claimed increasing marginal costs in C "dampen the diversion effect," but the currency implication is the opposite (quantity constraint concentrates incidence in C's price = currency, lowering ρ*); a correction beyond the referee's list. Added new subsubsection "Sector-Specific Factors: Upward-Sloping Export Supply" (`sec:rv`, blue): model, two results with the γ-table, minimal-structure converse ("none of the sign results require diminishing returns"), and "The boundary of the exercise" paragraph (EKNR/CDP dynamics; Obstfeld–Rogoff temporary-vs-permanent; persistence caveat with Kalemli-Özcan et al.). Compiles clean: 40 pp, 0 warnings.

### 2026-08-24 — Phase 3: calibration rebuilt (import shares, nested model, extended data)

**Data pipeline:**
- `scripts/fetch_fx_data.py` extended: windows now include H2-2025 and Dec-2025 averages (D3); new **matched ex-China ROW index** (D2) — Fed H.10 broad nominal index (FRED DTWEXBGS) with the CNY component stripped at the Fed's published weight 10.897% and renormalized. Key data: EUR Apr +3.36 → Dec +8.16; RMB Apr −1.51 → Dec +1.94; matched ex-CN index Apr **−0.95** (vs the mismatched AE index's +2.18) → Dec +2.27.
- New `data/calibration_inputs.json`: verified 2024 bilateral goods flows (importer-reported: US Census, GACC, Eurostat, VN customs) and nominal GDPs, with per-number source notes and flagged caveats (VN processing trade; KOR/TWN/EU GDP vintage to re-verify).
- New `scripts/calibrate_nested.py` → `data/calibration_nested.json`: country-specific preferences from import shares over GDP; α_T = 0.40; **demand system inverted at the model's free-trade equilibrium** (damped multiplicative fixed point, share fit ≤ 1e-6); configurations EU / VNM / VNM_adj (50% processing adjustment) / ROW; ρ grid 1.5–8 at η = 1.5; Δe and Δq for both regimes; per-config reversal thresholds.

**Headline results:** US home bias now 0.91–0.95 (kills the referee's §3.6 objection). EU config: model (Δe_AB, Δe_AC) = (−0.80, +3.45) at ρ=2.0 vs April data (−1.51, +3.36); (+0.29, +9.44) at ρ=2.6 (the Li et al. ratio) vs December data (+1.94, +8.16) — one elasticity in the central band rationalizes both horizons in sequence. Cumulative reversal thresholds at τ=1.45 nearly identical across configs: 2.97 / 3.10 / 2.98. ROW (matched index) April fits at ρ≈3 with both signs right. Vietnam raw shares give α_D=0.175 (processing artifact) and explosive magnitudes — reported as a single-bystander upper bound with the adjusted variant (α_D=0.553). December comparisons read as direction-of-transition evidence only (post-May de-escalation).

**Paper (`paper_draft.tex`), all blue:** §4.2 rewritten (import-share calibration, inversion, new Table 2 with α_D by country, grid-based (η,ρ) with Li et al./Broda–Weinstein anchors and the self-contained-world rationale for config-specific ρ; world-export-share construction and hand-assigned σ deleted); §4.3 rewritten around new figure `calibration_nested_results.pdf` (model curves vs ρ against April/December data lines, thresholds marked; generated by new `scripts/make_calibration_figure_nested.py`); matched-index construction in text; results discussion (EU both-horizon fit; ROW wrinkle; Vietnam upper-bound framing; Δq wedge; ≈3 threshold regularity; R1 concentration signature); caveats paragraph updated (single-aggregate scope cost; December read qualitatively). Intro: added darracq2026 (ECB WP 3213) and liqiu2022 (CEPR DP17409) with the explicit "neither provides the analytical sign characterization" distinction — resolves memo item M3 for the quantitative adjacency. 2 bib entries added. Compiles clean: 41 pp, 0 warnings.

**Appendix C** (6 extra configs) still on the old calibration — flagged in the paper footnote and here; rebuild needs China-bilateral data for JPN/KOR/MEX/CAN/TWN/IND (open item).

### 2026-08-24 — window/regime consistency fix and calibration audit (user-directed)

- **The one problem fixed:** each data window is now compared to the tariff vector actually in force in that window. Regime 3 (Dec 2025: τ_AB=0.20, τ_BA=0.10, τ_AC = EU 0.15 / VNM 0.20 / ROW ~0.15; rates verified: Geneva truce + Nov-10 fentanyl cut, July frameworks) added to `calibrate_nested.py` with per-config τ_AC; announced-rate April variant (regime2a: EU 0.20, VNM 0.46) computed for the replication package.
- **Vietnam reclassified**: not a bystander (46% announced Apr 2, 20% in force from July = December China rate). At Regime-3 rates the model predicts dollar +3.5–4.6% vs the dong against +4.8% observed — the dong is a test of classification (who is tariffed how much), not of the bystander mechanism. Announced-rate check: even at 46%, April dong still appreciates in the model (145% on China dominates) — April dong strength stays outside the trade channel (noted honestly).
- **December finding (per user's direction to keep both windows):** at December's near-uniform rates the model predicts mild dollar appreciation vs everyone (EU −4.9, ROW −6.4, VNM −4.6 at ρ=2.6); data show euro +8.2, ex-CN index +2.3, dong −4.8. Paper states plainly: the prevailing December tariffs cannot account for the observed multilateral dollar weakness through the trade channel (candidates: expected re-escalation, safe-haven erosion, monetary policy) — the inference discipline cuts both ways. "Transition toward the long-run" framing removed.
- **Home-bias audit (user query):** trio "home" includes non-trio goods (within US tradables: CHN 3.8%, EU 5.2%, all-foreign 28%); excluded-basket treatment gives α_D=0.889 and moves results by tenths; the α_D=0.72 all-foreign world is the ROW config. Clarification paragraph added to §4.2. Bystander-validity audit of all 9 configurations recorded (Canada/Mexico/India tariffed and/or retaliating — appendix rebuild deferred per user).
- Paper: Regime-3 row in the regimes table; new Regime-3 appendix paragraph; §4.3 restructured into April-vs-R2 / Vietnam-classification / December-vs-R3 paragraphs; figure restricted to April-vs-R2; caveats updated. 42 pp, 0 warnings.

### 2026-08-24 — final writing pass (Phase 4 completion)

- **Abstract v2, intro re-lean, conclusion v2** (all blue): connection-first positioning per the framing memo — PTA connection as the headline ("three names for one number"; isolated tariff ≡ preferential arrangement stated formally), impossibility as the reason the connection was invisible, episode-qualified threshold claims (~4 marginal / ~3 at 2025 scale), calibration sentence updated to the April-vs-R2 + December-discipline story, conclusion ends on "a sign condition that can decline to explain things."
- **New §2.4 "Scope and Modelling Choices"** (`sec:scope`, blue): long-run defense with the corrected NFA statement (structure invariant, location moves: 3% deficit ⇒ 3.96→4.6–5.1; all-in 2025 threshold ≈3.5); one-factor exactness as separate justification; capital-accumulation vs financial-account distinction; country-count trilemma with the degree-(n−1) argument and the demonstrated n=4 double-crossing (footnote); the single-aggregate cost + pair-by-pair-diagnostic follow-up.
- **§2.3 augmented**: Viner 1950, Mundell 1964, Kemp–Wan 1976, Bagwell–Staiger 2002, Chang–Winters 2002 wired in with the formal tariff≡preference identity. 7 bib entries added (incl. Krugman 1991, Yi 2000 for the scope section).
- **§3.3 additions**: ∂ρ*/∂α_D formula + home-bias/nest division of labor; the natural-language trap; episode-qualified range statement; new "The real exchange rate" paragraph (ρ*(q)=4.93 vs ρ*(e)=3.96, Balassa–Samuelson remark, non-tradables inert-for-the-mechanism).
- **Figures 2–7 compressed** into one 2×3 multipanel (`loci_multipanel.pdf`, new `scripts/make_loci_multipanel.py`); all references updated to panel letters; old six figure environments removed (referee §3.2/4.8).
- **Figure 1 legend fixed**: `plot_tb_locus` now uses a standard legend instead of overlapping inline right-end labels; figure regenerated (referee §7).
- Compiles clean: 42 pp, 0 warnings; 33 tests pass.

### 2026-08-24 — language simplification pass (user-directed)

Full editorial pass over all revision (blue) text, at the user's request, to plain declarative prose in the style of the original draft: short sentences; em-dash asides removed (one remains, in a citation list, converted to parentheses); intensifiers cut (precisely/exactly/comfortably/genuinely/deliberately); rhetorical constructions removed ("three names for one number", "the race is unwinnable", "It is tempting to extrapolate... It does not", "sobering implication", "an honest wrinkle", "a sign condition that can decline to explain things", "cutting in both directions", "confessing limitations"). All content, numbers, citations, and propositions unchanged. Sections touched: abstract, intro (4 paragraphs + roadmap), 2.2 (3 passages), 2.3, 2.4 (all), 3 opening, 3.2.2, 3.2.3, 3.3 (all prose + captions), 3.4 (6 passages), 4.1–4.3 (all revision text + figure caption), appendix Regime 3 (already plain), appendix threshold, appendix C summary, conclusion. Length 42 → 40 pages. Compiles clean, 0 warnings.
