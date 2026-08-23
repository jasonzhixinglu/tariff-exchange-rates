# Revision Plan — Response to Referee Report (August 2026)

**Paper:** *Trade Tariffs and Exchange Rates: Revisiting Conventional Wisdom in a Three-Country Framework* (Lu & Milkov)
**Referee recommendation:** Reject in current form; encouraged resubmission after major revision.
**Status of this document:** Living tracking document. Check off items as completed; record decisions and verified numbers here so the revision has a single source of truth.

---

## 1. The one-paragraph reframe

The referee's verdict is harsh on the current draft but generous on the underlying project: *"There is a good paper here, but it is a different paper from the one submitted."* The revision should be understood not as damage control but as an upgrade of the contribution. The current draft claims an ambiguity ("the sign of e_AC can flip") that it never exhibits and — as the referee proves and we have independently verified — **cannot** exhibit under its own single-elasticity specification. The revised paper replaces a claimed-but-absent numerical possibility with two sharp analytical results:

> **Proposition 1 (impossibility).** In the flat single-elasticity CES, the conventional appreciation result survives the move to three countries *as a theorem*: for any σ > 0, whenever home bias α_D ≥ 1/3, an isolated tariff cannot depreciate A's currency against the untariffed third country. The flat-CES intuition is precisely why the profession has stayed anchored on the two-country prior.
>
> **Proposition 2 (threshold).** Once the home-vs-import elasticity η and the cross-origin elasticity ρ are separated in a two-layer nest, reversal occurs iff ρ > ρ* = 3[1 + α_D(η−1) − α_T(1−α_D)]. At US-realistic parameters ρ* ≈ 4 — comfortably inside measured cross-origin elasticities (FLOR 2018, Broda–Weinstein 2006, Fajgelbaum et al. 2024). The reversal is not a knife-edge curiosity; it is attainable at standard parameters, but *only* once the two margins are separated.

Everything the paper cares about survives and gets stronger: the trade-war amplification result stays unambiguous (with a corrected comparative static), the policy payoff for the 2025 attribution debate stands, and the two results together tell a cleaner story than "ambiguity": **the conventional wisdom fails not because a third country exists, but because home-vs-import and cross-origin substitution are different margins.**

---

## 2. Understanding the referee report

Three independently disqualifying problems, plus a constructive fix handed to us nearly complete.

### 2.1 The headline result is never produced (§3.1, §5.3)

- Figures 4–6 show Δlog e_AC = −0.15, −0.05, 0.00 at σ = 0.5, 1, 2: monotonically approaching zero from below, never crossing. Section 3.2.2's claim of reversal at high σ cites a figure showing 0.00, not a positive number.
- Table 4 Panel A (the isolated-tariff regime that maps onto the theory): Δe_AC < 0 in **all eight** configurations, including Vietnam at σ = 8.
- Referee's diagnosis: a single σ does double duty — it strengthens diversion (toward reversal) but simultaneously strengthens home-vs-import expenditure switching (against it). Imposing ρ = η = σ makes the threshold chase σ at rate 3α_D, so a crossing requires α_D < 1/3, which no economy satisfies. The paper's symmetric calibration (α_D = 1/3) sits exactly on the knife edge with d log e_AC/dτ = −1/(12σ) → 0⁻. Figure 6 shows an **asymptote**, not a near-crossing.

### 2.2 The novelty claim is not defensible as stated (§3.3)

- With one factor, linear technology, P_Ti = 1, and balanced trade, e_ij **is** the common-currency relative wage and simultaneously the terms of trade. That object is the routine output of Caliendo–Parro (2015), Ossa (2014), Costinot–Rodríguez-Clare (2014); third-country terms-of-trade effects of *discriminatory* tariffs are the core of the PTA literature (Bagwell–Staiger, Bond–Syropoulos, Ornelas).
- The paper positions itself against Lerner–Metzler–Mundell — the textbook prior, not the frontier.
- What the referee concedes **is** genuinely new (this becomes the stated contribution):
  1. The closed-form analytical threshold ρ* and its comparative statics (elasticity gap, home bias, size).
  2. The impossibility result under a single elasticity.
  3. Unambiguous trade-war joint depreciation, sign independent of the elasticity.
  4. The *translation*: the trade literature reports ŵ and welfare; nobody in it says "therefore the dollar should depreciate against the euro." That inferential step, and the correction it implies for the 2025 attribution debate, is defensible even though the equilibrium object is familiar.

### 2.3 The calibration does not support the abstract (§3.5–3.7, 3.9)

- Regime 2 predicts Δe_AC > 0 in all 8 configurations; data show it in 2 (EU, Japan) — both safe havens, i.e. the financial pattern the model abstracts from. Six failures relegated to Appendix C reads as selective reporting.
- Magnitudes are order-of-magnitude misses (+24.05% Canada, +22.81% Taiwan, +17.45% Japan).
- Expenditure shares calibrated from world *export* shares imply the US spends 70% more on Chinese tradables than its own (α_TA = 0.097 vs α_TB = 0.165); actual US expenditure on Chinese goods is ~1–2% of consumption. Zero home bias inflates the diversion mechanism.
- σ is hand-assigned per configuration by narrative, and it controls the sign of the headline result.
- Long-run balanced-trade predictions compared to one month of nominal FX data — the horizon where disconnect (Itskhoki–Mukhin) is strongest.

### 2.4 Equation and claim errors (§4)

- **Eq. (28):** spurious e_ik in the export term; internally inconsistent with eq. (9). Manuscript typo — the code is correct.
- **Eqs. (26)–(27):** D_k is the price-index denominator of a *flat* CES over all four goods, contradicting the stated nested CD-outer/CES-inner structure. They coincide only at σ = 1.
- **§3.2.3:** trade-war depreciation magnitude is claimed increasing in σ; in the single-σ model it is **decreasing**. It is increasing in ρ in the nested model — another argument for the nest.
- **§2.2 robustness:** Lemmas 2.1–2.2 are Marshall–Lerner in different clothing; restate honestly as "the result holds wherever Marshall–Lerner holds," which sets up Section 3 better (bilateral ML does not pin down the multilateral sign).

### 2.5 The constructive proposal (§5)

Two-layer nest: Cobb–Douglas outer (tradables share α_T); CES over {home, import bundle} with macro elasticity η; CES across foreign origins with micro elasticity ρ. Delivers:

- ρ* = 3[1 + α_D(η−1) − α_T(1−α_D)] at the symmetric point; reversal iff ρ > ρ*. Denominator 3[3α_D(η−1)+ρ+1] > 0 for η ≥ 1 is the local stability condition.
- ρ* grid lands in 2.5–5.5 across the realistic (α_D, η) box.
- ρ* is **decreasing in L_C** (small C appreciates sharply per unit of diverted demand): Vietnam ρ* = 8.76, EU 4.32, ROW 3.78 at (α_D=.80, α_T=.40, η=1.5, L_B=1.21). Vietnam is the *hardest* configuration, not the easiest — the current draft has this backwards.
- ρ* **falls monotonically in tariff size** (3.96 → 2.70 at τ=1.45, equal sizes): the local threshold is a conservative bound; the 2025-scale tariffs make reversal easier. Report this — it pre-empts the "your threshold is local" objection.
- Resist going further (three-level nest, CRESH): the two-level nest delivers the result and richer heterogeneity cannot be disciplined by available estimates.

---

## 3. Independent verification (what we ran and found)

All referee claims checked against the repo; scripts in the session scratchpad, to be promoted into `scripts/`/tests during Phase 0.

### 3.1 We found the *cause* of the paper–referee replication discrepancy: a code bug

`src/tariff_exchange_rates/economy.py` (~line 99) computes disposable income as

```
I_i = w_i L_i / (1 − Σ_j α_T[j] · τ_ij/(1+τ_ij))        # eq. (25), "exact for all σ"
```

This closed form is **only exact at σ = 1**. Under the inner CES the expenditure share on variety j is price-dependent, not the fixed weight α_Tj, so tariff revenue is mis-measured whenever σ ≠ 1 and consumer prices differ from 1. The correct fixed point uses realized CES shares:

```
I_i = w_i L_i / (1 − Σ_j s_ij(p) · τ_ij/(1+τ_ij)),   s_ij(p) = realized expenditure share
```

The same bug is in the dashboard port `dashboard/src/lib/modelJs.js` (~line 59). All published figures, `data/theory_grid.json`, and `data/calibration_panel.json` were generated with the buggy formula.

**Symmetric baseline, isolated tariff τ_AB = 1, log e_AC:**

| σ | repo code (buggy) | corrected | paper figure | referee's replication |
|---|---|---|---|---|
| 0.5 | −0.1488 | −0.1133 | −0.15 | −0.113 |
| 1 | −0.0488 | −0.0488 | −0.05 | −0.049 |
| 2 | **+0.0048** | −0.0163 | 0.00 | −0.016 |
| 5 | **+0.0218** | −0.0013 | — | −0.001 |

The referee's numbers match the *corrected* model exactly. The apparent sign flip at σ ≳ 1.9 in our code (and interactively visible in the dashboard) **is a numerical artifact of the income bug**. Under the correct model log e_AC asymptotes to 0⁻ and never crosses at the symmetric calibration, and at the paper's asymmetric calibrations *as coded* (checked EU config up to σ = 20 — but see the weight-convention caveat in §3.6 below: under the paper's *stated* utility, an α_D < 1/3 calibration does cross, exactly as the symmetric theory predicts).

Note the paper's Figure 6 reports 0.00 (roughly the truth) while the buggy code gives +0.005 — so the figures' provenance vs. the current code state should be audited in Phase 0 (`notebooks/section3_three_country_model.ipynb`).

### 3.2 Referee's threshold verified

Ran the referee's `threecountry_threshold.py` (symbolic + numeric): analytic d log e_AC/dτ matches the nonlinear solve to 6 decimals at every point tested; ρ* formula, the size table (Vietnam 8.76 / EU 4.32 / ROW 3.78), and the ρ*−σ ≡ +0.50 constant-gap result at the paper's calibration all reproduce.

### 3.3 Trade-war comparative static (§4.3) verified

Single-σ: log e_AC = +0.094 → +0.046 as σ: 1.5 → 10 (**decreasing** — paper's claim is wrong). Nested with η = 1.5: +0.016 → +0.252 as ρ: 1.5 → 10 (increasing — the claim is right only in the nest).

### 3.4 Effect of the income-formula fix on the published calibration (Δe_AC, %)

| Config, regime | published | corrected |
|---|---|---|
| EU, Regime 1 | −0.40 | −0.53 |
| EU, Regime 2 | +7.29 | +5.58 |
| VNM, Regime 2 | +6.38 | +4.69 |
| ROW, Regime 2 | +0.87 | **−0.14** |

The ROW sign flips under the corrected model, removing one of the two directional "successes" claimed in the abstract (advanced-economy trade-weighted index, +2.18% in data). **The calibration problem is slightly worse than the referee reports.** This must be handled forthrightly in the response letter; the rebuilt calibration (Phase 3) supersedes these numbers anyway.

### 3.5 Equation errors confirmed

Eq. (28): code implements the correct (producer-price) export term, so the manuscript e_ik is a typo. Eqs. (26)–(27): code implements the nested structure (equivalent up to a scale factor irrelevant to shares), so the manuscript's flat-CES D_k is the error; make the text match the nested spec and the σ=1 replications line up to two decimals.

### 3.6 Weight-convention inconsistency and mis-hit calibration targets (found in Phase 1/2 probing)

The paper's stated inner-CES utility uses weights α_Tj^(1/σ), which implies expenditure shares ∝ α_Tj·p^(1−σ) (*plain* convention). The paper's demand formula (24) and the code instead use shares ∝ α_Tj^σ·p^(1−σ). The two coincide only at σ = 1 or under symmetric weights — which is why every symmetric-baseline result matches the referee regardless. Consequences:

- **The asymmetric impossibility picture depends on the convention.** Under plain weights (the stated utility), the symmetric boundary is sharp and verified numerically: with α_D = 0.267 < 1/3, the flat-CES crossing appears at exactly the predicted σ* = 2.75, and size asymmetry does *not* kill it (checked L configurations from (1,1,1) to (1, 1.21, 3.51), all cross at σ = 6). Under the α^σ convention the calibrated configurations never cross. Proposition 1 must state its weight convention explicitly.
- **The calibrated model misses its own calibration targets at σ ≠ 1.** In the EU configuration at σ = 6, realized baseline US expenditure shares are (0.094, 0.188, 0.118) against targets (0.097, 0.165, 0.138) — China off by +14%, EU by −14%. Phase 3 recalibration must invert the demand system so shares match at the free-trade *equilibrium* (standard practice), not plug data shares in as weights.

---

## 4. The revised paper's narrative (constructive framing)

The referee's §6/§8 sketch, adopted with our additions. The pitch:

> In a minimal multilateral setting, the conventional two-country appreciation result survives a flat-CES extension **as a theorem**: with a common elasticity it cannot be overturned at any plausible home bias — which is why moving from two to three countries has not, by itself, disturbed the textbook prior. It fails only once the home-vs-import elasticity η and the cross-origin elasticity ρ are separated, and we derive the exact threshold ρ* at which it fails. At US-realistic parameters ρ* ≈ 4, well within measured cross-origin elasticities, so bilateral appreciation against a tariffed partner can coexist with depreciation against untariffed ones. In a bilateral trade war the ambiguity resolves: both belligerents depreciate against the bystander unambiguously, with magnitude increasing in ρ. Consequently, observed multilateral dollar depreciation during a tariff episode cannot be attributed to financial or convenience-yield channels on the strength of the two-country prior alone.

Framing principles for the rewrite:

1. **Lead with the impossibility theorem, not the ambiguity.** "The conventional result survives flat CES as a theorem and fails only when the two elasticities are separated" is sharper, explains why the point was overlooked, and turns the referee's most damaging finding into our Proposition 1.
2. **Own the equivalence e = relative wage = terms of trade** in a prominent early subsection (new §2.5). State what the quantitative trade literature already computes, and what we add: the closed-form sign characterization and the translation into exchange-rate language for the 2025 attribution debate. Doing this ourselves is far better than having a referee do it.
3. **Restate the robustness section honestly** as "the result holds wherever Marshall–Lerner holds" — cleaner, and it sets up the punchline that bilateral ML does not pin down the multilateral sign.
4. **Defend the minimal structure deliberately** (not in a caveat list): the paper establishes a *sign* result, and the stripped-down setting shows the flip requires no dynamics, no capital, no financial frictions. Engage Ricardo–Viner, EKNR/CDP, and the intertemporal (temporary-vs-permanent tariff) literatures as the boundary of the exercise.
5. **Calibration as disciplined illustration, not horse race.** Country-specific import-share preferences, (η, ρ) from the literature, results over a grid with ρ* marked, all configurations in the main text, and either an extended data window or explicitly no directional-validation claim.
6. **Turn size comparative statics into content:** Vietnam has the highest assigned elasticity but the highest threshold — small countries are the hardest place to see the reversal. This reverses the current draft's presentation and is a quotable, policy-relevant point.

---

## 5. Work plan

### Phase 0 — Fix and verify existing code *(prerequisite for everything)*

- [x] **0.1** Fix income/tariff-revenue fixed point in `src/tariff_exchange_rates/economy.py`: solve for I_i using realized CES expenditure shares (still closed-form — shares don't depend on income). *Also fixed while there:* the CES demand branch spent all income on tradables (budget violated by 1+α_N; discontinuous with the CD branch by 1/α_T — scale error, cancels in TB=0 so no effect on equilibria but corrupts levels), and the tradable price index used unnormalized weights (diverges as σ→1; now normalized, HD1, branch-consistent — affects reported RERs only).
- [x] **0.2** Mirror the fix in `dashboard/src/lib/modelJs.js` (verified exact parity with Python TBs at test points).
- [x] **0.3** Regression tests in `tests/test_economy.py` (15 passing): budget consistency; CES↔CD continuity; σ=1 equilibria unchanged; corrected model matches referee replication to 4 dp at σ = 0.5/1/2/5; no sign reversal over σ ∈ [0.3, 50]; finite-difference slope matches analytic −1/(12σ) at the paper's calibration; two-country closed form; Walras; price-index HD1. (Nested-model analytic-slope test to be added with Phase 2.)
- [x] **0.4** Figure provenance audited: the saved notebook outputs show e_AC = 1.0048 at σ=2 and print "e_AC crosses 1.0 near σ ≈ 1.86" — all Section 3 figures and the paper's Fig. 6 "0.00" (= rounded log 0.0048) came from the buggy code. Notebook narrative (intro, §4.4, σ-scan, summary table) asserted the spurious reversal; patched to the corrected story and re-executed cleanly (σ=2 isolated: e_AC = 0.9838; max e_AC over σ-grid = 0.9971 < 1).
- [x] **0.5** Regenerated: `data/calibration_panel.json`, `data/theory_grid.json`, `output/*.pdf` + copies in `Exchange_Rate_Tariffs/`, section 3 + 4 notebooks re-executed. No sign reversal anywhere in the single-σ model — numerical footing for Prop. 1 confirmed. (Dashboard `public/data` + `dist` rebuild tracked as 0.7.)
- [x] **0.6** `scripts/verify_referee_claims.py` reproduces and asserts every referee claim + repo findings (sections 1–5, `--symbolic` for the sympy ρ* derivation). All checks pass.
- [ ] **0.7** Copy regenerated JSONs to `dashboard/public/data/` and rebuild `dashboard/dist` (`npm run build`) so the deployed dashboard reflects the corrected model.

**New findings from Phase 0 (beyond §3):**
- **Trade-war asymmetry boundary:** on the regenerated theory grid, 1 of 27 flat-CES war points has e_AC < 1 — the most lopsided war (τ_AB=1.5, τ_BA=0.25, σ=1), where the dominant tariffer behaves like the isolated case and mildly *appreciates* vs C (−0.45%) while B still depreciates. The trade-war proposition's "unambiguous joint depreciation" needs a near-symmetry qualifier (extends the referee's §7 knife-edge remark about e_AB). Relevant to the calibration: Regime 2 has τ_AB=1.45 vs τ_BA=1.25 — comfortably inside the joint-depreciation region.
- The referee's §5.6 large-tariff table is the **cumulative** threshold (ρ such that the total Δlog e_AC over [0,τ] is zero) — reproduced exactly (3.55/3.19/2.86/2.70 at τ = 0.2/0.5/1.0/1.45). The **marginal** threshold (slope zero at τ) is lower still (3.23/2.69/2.26/2.07). Report both in the paper; cumulative is the policy-relevant one for a discrete tariff.
- Corrected calibration-panel values (flat CES, for reference until Phase 3 supersedes): EU R2 Δe_AC +5.58, VNM R2 +4.66, ROW R2 −0.14, Taiwan R2 +19.24, India R2 +18.43 — magnitudes still far too large, reinforcing the home-bias recalibration case (§2.3).

### Phase 1 — Derive the theory

- [x] **1.1** ρ* re-derived symbolically from our own model setup (sympy, `scripts/verify_referee_claims.py --symbolic`): matches 3[1 + α_D(η−1) − α_T(1−α_D)] exactly; slope denominator 3[3α_D(η−1)+ρ+1] confirmed.
- [ ] **1.2** General sizes: `scripts/derive_general_threshold.py` (symbolic derivation at a general baseline, in progress) — target: threshold as root of a quadratic in ρ with coefficients in baseline shares, validated against brute-force 8.76/4.32/4.24/3.78. Asymmetric preference weights after that.
- [ ] **1.3** Proposition 1 (impossibility) — numerically mapped, statement pending: under plain weights, symmetric boundary α_D < 1/3 is sharp (crossing at predicted σ* = 2.75 for α_D = 0.267; verified robust to size asymmetry), and α_D ≥ 1/3 kills the crossing at every σ tested (up to 50). Must state weight convention (see §3.6). Formal proof for the proposition text remains.
- [x] **1.4** Large-tariff thresholds computed under **both** definitions — cumulative (referee's §5.6: 3.96 → 2.70 over τ: 0 → 1.45, reproduced exactly) and marginal (3.96 → 2.07, lower still). Report both; cumulative is policy-relevant for a discrete tariff.
- [ ] **1.5** Stability condition 3α_D(η−1)+ρ+1 > 0 stated as such (write-up task, Phase 4).
- [x] **1.6** Trade-war comparative statics verified: joint depreciation, magnitude increasing in ρ (nested: +0.016 → +0.252 over ρ 1.5 → 10) and decreasing in σ (flat: +0.094 → +0.046); asserted in `tests/test_nested.py`.

### Phase 2 — Implement the two-layer nest

- [x] **2.1** `src/tariff_exchange_rates/nested.py`: CD outer (α_T) → CES(η) over {home, M_i} → CES(ρ) over foreign origins; country-specific α_D and β weights; plain-weight convention (matches the paper's stated utility; see §3.6).
- [x] **2.2** `solve_3country_nested`, `rho_star_symmetric`, `rho_star_numeric` (marginal + cumulative definitions, general sizes/weights/tariff levels), `d_log_eAC_dtau`.
- [x] **2.3** `tests/test_nested.py` (18 passing): collapse to flat CES at ρ=η, analytic slope to 1e-6, referee tables 5.5/5.6/4.3, genuine reversal at ρ = 4.5 > ρ* = 3.96.
- [ ] **2.4** Rebuild dashboard around (η, ρ) with ρ* marked on the theory panel; keep a flat-CES toggle to demonstrate the impossibility result interactively. *(The dashboard becomes a genuine asset here: the threshold is visible.)*
- [ ] **2.5** Regenerate theory grid for the nested model.

### Phase 3 — Rebuild the calibration

- [ ] **3.1** Recalibrate expenditure shares from **bilateral import shares in each country's absorption**, country-specific preferences (drop common-preference assumption and world-export-share construction). Realistic US home bias α_D ≈ 0.8.
- [ ] **3.2** Source (η, ρ) from Feenstra–Luck–Obstfeld–Russ (2018) [macro vs micro wedge — currently miscited in support of σ=2], Broda–Weinstein (2006), Fajgelbaum et al. (2020, 2024). Fix the Amiti–Redding–Weinstein attribution (pass-through paper, not cross-origin elasticity).
- [ ] **3.3** Report results over a ρ grid per configuration with ρ* marked; no hand-assigned point values driving signs.
- [ ] **3.4** Include the large-tariff ρ*(τ) result (1.4) in the calibration section.
- [ ] **3.5** All configurations in the main text; no appendix relegation of failures.
- [ ] **3.6** Extend FX comparison window through end-2025 (`scripts/fetch_fx_data.py`) **and** reframe as magnitude/mechanism illustration rather than directional horse race. Be explicit that safe-haven/financial channels dominate at monthly horizons (Itskhoki–Mukhin) and that this is the boundary of the model.
- [ ] **3.7** Resolve ROW: **[DECISION — see §6]** drop it or construct a matched "world minus US and China" trade-weighted index.
- [ ] **3.8** Reconcile Table 2 vs Table 3 (α_TB 0.236 vs 0.235) and the incorrect Appendix C note about "slightly different σ values."

### Phase 4 — Rewrite the paper

- [ ] **4.1** Abstract: referee's §8 language as the skeleton (see §4 above). No "correctly predicts the direction" claim unless the rebuilt calibration actually supports it.
- [ ] **4.2** Introduction: drop "we challenge the conventional wisdom on different grounds"; state the contribution as the sign characterization + the inference correction. Motivation stays: the 2025 dollar-depreciation attribution debate is real and current.
- [ ] **4.3** New §2.5 (half page): e ∝ relative wage ∝ terms of trade; situate vs. Caliendo–Parro, Ossa, Costinot–Rodríguez-Clare, PTA literature; say exactly what is new.
- [ ] **4.4** §2.2 restated as Marshall–Lerner; fix the "or more generally" logic slip in Lemma 2.1's export condition.
- [ ] **4.5** §3 restructured: Prop. 1 (impossibility) first, Prop. 2 (threshold ρ*) with comparative statics (α_D, η, α_T, L_C, τ), then trade war (corrected magnitude claim).
- [ ] **4.6** Fix eq. (28) (drop e_ik from export term; align with eq. (9)); make eqs. (26)–(27) match the implemented nested structure; note α_N inert under CD outer (state what N buys or drop it).
- [ ] **4.7** New §3.4: Ricardo–Viner extension (Y_T = A·L^γ, γ<1) formalizing the export-supply channel; explicit boundary discussion of dynamic (EKNR, CDP) and intertemporal (Obstfeld–Rogoff Ch. 4; temporary vs permanent tariffs) literatures; deliberate defense of the minimal structure. **[DECISION — see §6]**
- [ ] **4.8** Compress Figures 2–7 into one multi-panel locus figure + one d log e_AC/dτ-vs-ρ plot with ρ* marked.
- [ ] **4.9** Conclusion: the inferential payoff stated directly (bilateral appreciation ≠ broad strength; multilateral depreciation ≠ evidence of financial channels by itself).
- [ ] **4.10** Flag trade-war e_AB-unchanged as a knife-edge (requires τ_AB = τ_BA and equal size; calibration has neither), not a result.

### Phase 5 — Minor comments sweep (referee §7)

- [ ] **5.1** State once, early: e is a relative wage in a real model with no nominal anchor.
- [ ] **5.2** Percent-change convention (positive = depreciation of first-named currency) moved from figure notes to text.
- [ ] **5.3** Figure 1 tariff legend overlap fixed.
- [ ] **5.4** §2.2 opening cross-reference ("Section 2" → "Section 2.1").
- [ ] **5.5** Bibliography additions: Itskhoki & Mukhin (2021); Caliendo & Parro (2015); Ossa (2014); Costinot & Rodríguez-Clare (2014); Bagwell & Staiger + PTA terms-of-trade (Bond–Syropoulos, Ornelas); Broda & Weinstein (2006); Eaton–Kortum–Neiman–Romalis (2016); Caliendo–Dvorkin–Parro (2019); Obstfeld (2025); Werning et al. (2025); Feenstra–Luck–Obstfeld–Russ (2018) recited correctly.
- [ ] **5.6** README + dashboard About text updated to the new narrative (README currently states the old claim).

### Phase 6 — Response to referee

- [ ] **6.1** Point-by-point response letter. Tone: accept the diagnosis, document the fix. Where we found *more* than the referee (the income-formula bug explaining the replication discrepancy; the ROW sign flip under the corrected model; the asymmetric impossibility observation), say so plainly — it demonstrates the revision is load-bearing, not cosmetic.

---

## 6. Open decisions (user input needed)

| # | Decision | Options | Notes |
|---|---|---|---|
| D1 | Ricardo–Viner extension (4.7) | (a) Implement fully (Y = A·L^γ): referee "recommends implementing"; tractable; likely *lowers* ρ*, strengthening the result. (b) Verbal + defense of minimal structure only, park as future work. | Referee explicitly recommends (a) but the load-bearing revision is Props. 1–2. Could be staged: (b) for structure, (a) if time allows. |
| D2 | ROW configuration (3.7) | (a) Drop it. (b) Construct a matched "world minus US−China" trade-weighted index. | The corrected model flips ROW's Regime-2 sign anyway (−0.14%), so its "success" is gone regardless. Leaning (a) unless the matched index is cheap to build. |
| D3 | FX comparison window (3.6) | Extend through end-2025, reframe as illustration, or both. | Current recommendation: both. |
| D4 | Do we keep the flat-CES model in the main text as Prop. 1's vehicle, with the nest as the main specification? | Yes (referee's structure) — but confirm how much of old §3 survives. | Referee's §6 sketch keeps flat CES for Prop. 1, nest for Prop. 2. |

---

## 7. Key verified numbers (quick reference)

- **ρ\* formula:** ρ* = 3[1 + α_D(η−1) − α_T(1−α_D)]; slope denominator 3[3α_D(η−1)+ρ+1].
- **US-realistic:** α_D=0.80, α_T=0.40, η=1.5 ⇒ ρ* = 3.96. Range over realistic box: 2.5–5.5.
- **Impossibility gap** at paper's calibration (α_D=1/3, α_T=3/4): ρ*−σ ≡ +0.50 for all σ; d log e_AC/dτ = −1/(12σ).
- **Size:** ρ* = 8.76 (Vietnam, L_C=.055), 4.32 (EU, .86), 4.24 (equal), 3.78 (ROW, 3.51).
- **Large tariffs:** ρ* falls 3.96 → 2.70 as τ: 0 → 1.45 (equal sizes).
- **Trade war (τ=.5, equal):** nested η=1.5: +0.016 → +0.252 over ρ: 1.5 → 10 (increasing); single-σ: +0.094 → +0.046 (decreasing).
- **Income-bug corrections (symmetric, τ_AB=1):** σ=2: +0.0048 → −0.0163; σ=5: +0.0218 → −0.0013.
- **Calibration corrections (Δe_AC, %):** EU R2 +7.29 → +5.58; VNM R2 +6.38 → +4.69; ROW R2 +0.87 → **−0.14** (sign flip).
