# Revision Plan — Response to Referee Report (August 2026)

**Paper:** *Trade Tariffs and Exchange Rates: Revisiting Conventional Wisdom in a Three-Country Framework* (Lu & Milkov)
**Referee recommendation:** Reject in current form; encouraged resubmission after major revision.
**Inputs:** (1) referee report (`referee_report_tariffs_fx.md`); (2) referee's derivation script (`threecountry_threshold.py`); (3) **framing memo** (`revision_framing_memo.md`, received 2026-08-23) — repositions the contribution as *a connection to the PTA literature, illustrated*; see §4a below for its adoption and our verified amendments.
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

## 4a. The framing memo: adoption, verified amendments, and disagreements

The framing memo (2026-08-23) is **adopted as the controlling statement of the paper's positioning**, superseding §4's framing where they differ. Its core moves and our assessment:

### Adopted
1. **Connection-first positioning.** The headline is: *the PTA literature bears directly on the tariff–exchange-rate question, and we illustrate the connection with minimal theory.* The isolated tariff **is** formally a preferential arrangement in favor of C ("raise τ_AB, hold τ_AC=0" ≡ "cut τ_AC, hold τ_AB" up to level/revenue). Deliberately modest: ρ* becomes a bonus, not a load-bearing novelty claim. The impossibility theorem is retained as *the paper's story about the literature* — the standard Armington specification conflates the two elasticities that make the connection visible, which is why the obvious first extension finds nothing and why the connection went unstated. (Our current intro/§2.3, written before the memo, lead with "we characterize the sign in closed form" — they need a re-lean, not a rewrite; the content is compatible.)
2. **Scope-and-modelling-choices section placed BEFORE the three-country model**, defenses by purpose: long-run object; one factor as a *separate* justification (exactness of e = ToT = relative wage licenses the translation); no capital (accumulation ≠ financial account); three countries via the country-count trilemma (symmetric-n loses heterogeneity, quantitative-n loses propositions, n=3 is the smallest with discrimination and the largest with closed forms); the cost stated plainly in one sentence (a single untariffed aggregate cannot show simultaneous appreciation/depreciation across partners — which defines the follow-up: ρ* as a pair-by-pair diagnostic).
3. **Specification discipline**: two-level nest necessary and sufficient; no bilateral-elasticity heterogeneity (undisciplinable); the natural-language trap (China–Vietnam vs US–China *is* the ρ-vs-η gap); home bias = credibility fix, nest = result (∂ρ*/∂α_D = 3[(η−1)+α_T] > 0 — verified); configuration-specific ρ justified because each configuration is a self-contained three-country world (adopt as the Phase 3 rationale, replacing narrative assignment).
4. **Long-run real framing** converts calibration failures into predictions and gives the principled reason for extending the FX window (resolves D3 in favor of "both").
5. **Contribution statement** (memo §6) adopted as canonical, subject to amendment (b) below.
6. Additional citations to wire in: Viner (1950), Mundell (1964, tariff preferences & ToT), Kemp–Wan (1976), Bagwell–Staiger (2002), Chang & Winters (2002, Mercosur excluded-country prices — empirical anchor), Krugman (1991), Yi (2000).

### Verified amendments (memo open items resolved by computation, 2026-08-23)
- **(a) ρ* for the real rate differs — and it is a result, as the memo anticipated.** At the benchmark (α_D=.8, α_T=.4, η=1.5, equal sizes): **ρ*(q) = 4.93 vs ρ*(e) = 3.96**. The CPI-real threshold is higher because the tariff mechanically raises A's tariff-inclusive price index, absorbing part of the nominal depreciation (d log q = d log e + d log P_C − d log P_A with dP_A > 0 at fixed e). Both thresholds sit inside the measured cross-origin range. Paper treatment: propositions stated for e (= relative wage = ToT, the clean object); a short result reports ρ*(q) > ρ*(e) with the mechanical-CPI intuition and the Balassa–Samuelson remark (P_N is a pure productivity ratio, so all real-rate action runs through tradables — non-tradables are inert *for the mechanism* but govern the e→q mapping).
- **(b) The NFA-neutrality sentence in memo §3.2 is wrong and must not go into the paper as written.** Memo claims non-zero NFA "shifts the level but not the comparative static." Numerically it shifts the threshold substantially: with a permanent A trade deficit of 3% of income, ρ* rises from 3.96 to 4.64–5.10 (depending on whether the counterpart surplus is B's or C's); at 6%, to 7.07; an A *surplus* of 3% lowers it to 3.42. A US-scale deficit therefore makes the reversal meaningfully harder, and the bilateral composition of the imbalance matters. The correct defense of balanced trade is our general-baseline proposition: the threshold structure (reversal iff ρ > larger root of a quadratic in observables) is intact at *any* baseline, including imbalanced ones — the *location* moves with the baseline, and we can report it. This is a better sentence for the scope section and an honest new sensitivity result for the calibration (the US runs ~3% deficits).

### Disagreements / nuances (ours)
- **Do not undersell the impossibility theorem.** The memo's own §2 calls it "the paper's story about the literature"; keep it as Proposition 1 with full prominence — the modest headline and a sharp theorem are compatible.
- **The general-baseline quadratic is not "unenlightening."** The memo (§3.2) uses it as evidence that closed forms die beyond symmetry. In fact it factors interpretably (c₂ = b_AB·b_AC·b_CA·b_CB(1−h_A)(1−h_C)y_A y_C > 0; common factor b_AB(1−h_A)y_A; c₀ contains the symmetric threshold with h_A ↦ α_D) and is stated in *observables* — which is precisely what enables the memo's own proposed follow-up (ρ* as a pair-by-pair diagnostic in a many-country world) and the NFA sensitivity in (b). Present it as a feature (sufficient-statistics diagnostic), while agreeing that n = 4 cofactor expansions are hopeless.
- **Memo §4 (errors to fix) is already fully executed** in the 2026-08-23 paper tranche, including the resolution of its open question in item 2: the code implemented *neither* stated structure — the discrepancy was the tariff-revenue income formula (exact only at σ=1), now fixed and disclosed in a footnote.

### Referee follow-up (2026-08-24), resolved
1. **Country-count argument** (their flag on our quadratic pushback): stated safely in 4.11 as follows — the structural fact is that the linearized numerator N(ρ) has degree n−1 (Jacobian entries linear in ρ), so n=3 is the largest n at which a single threshold is guaranteed (quadratic, positive leading coefficient, single crossing verified over ρ ∈ (0.2, 14)); at n=4 the cubic admits multiple sign changes, and a numeric scan **found them** (two asymmetric 4-country configurations with double crossings in d log e_AC/dτ over ρ). The argument is dimensional *and* now demonstrated by counterexample; do not claim n=4 closed forms are merely "messy."
2. **Joint deficit × real-rate thresholds** (their "worth doing before committing to 'inside the measured range'"): computed. Marginal, 3% split deficit: ρ*(e) = 4.83, **ρ*(q) = 6.05** (their ~6 guess confirmed; range 5.65–6.64 by deficit composition). BUT the tariff-size effect dominates at episode scale: **cumulative at τ = 1.45: ρ*_cum(q) = 3.55 (3% deficit), 4.55 (6%)**; at τ = 0.20: ρ*_cum(q) = 5.22. → The paper must **episode-qualify** the claim: for 2025-scale tariffs the all-in (real-rate, deficit-adjusted, discrete-tariff) threshold is ≈3.5 — comfortably inside measured cross-origin elasticities; for marginal tariffs at a US-scale deficit it is ≈5–6.6 — inside only at the upper end of estimates. Never state "inside the measured range" unqualified. (Numbers to be promoted into `verify_framing_memo_checks.py` when writing 4.13; RV is still expected to lower all of these.)

### New work items from the memo (folded into the phases below)
- [x] **M1** ρ*(q) vs ρ*(e) — computed (amendment a); paper write-up pending (→ 4.13).
- [x] **M2** NFA robustness TB_i = −b_i — computed (amendment b); paper write-up pending (→ 4.15, 3.10).
- [ ] **M3** Literature diligence: do Ossa (2014) or the PTA terms-of-trade papers state the third-country ambiguity as a proposition? Cite-and-lean or say-explicitly-not accordingly (honest either way).
- [ ] **M4** Scope section drafted before the model (→ 4.11); intro/§2.3/abstract re-leaned to connection-first (→ 4.12); Δq reported alongside Δe in experiments and calibration (→ 4.13, code support exists — solver already returns log_q); natural-language trap + home-bias/nest division of labor into §3.3–3.4 (→ 4.14); NFA sensitivity paragraph (→ 4.15); configuration-specific-ρ rationale into §4 (→ 3.9); new PTA citations (→ 5.5).
- [ ] **M5** Ricardo–Viner ρ* re-derivation — same as D1 (prototype next).

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
- [x] **1.2** General sizes **and** general asymmetric baselines: `scripts/derive_general_threshold.py` derives d log e_AC/dτ|₀ = N(ρ)/D by share-based linearization at *any* free-trade baseline described by observables (y_i common-currency incomes, h_i home shares, b_ij import-bundle origin shares, α_T). N is quadratic in ρ with c2 = b_AB·b_AC·b_CA·b_CB·(1−h_A)(1−h_C)·y_A·y_C > 0 ⇒ ρ* is the larger root and "reversal iff ρ > ρ*" holds at any baseline. All coefficients share the factor b_AB(1−h_A)y_A (A's import exposure to B); c0 contains 1 + h_A(η−1) − α_T(1−h_A), the symmetric ρ*/3 with h_A ↦ α_D. Symmetric case reduces exactly to the referee's formula. Validated to ~1e-5 against brute force (8.76/4.32/4.24/3.78). Because it's stated in baseline observables, this covers asymmetric preference weights too — it is the sufficient-statistics form for the paper.
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
- [x] **3.8** Reconcile Table 2 vs Table 3 (α_TB 0.236 → 0.235 fixed in main text) and the incorrect Appendix C note (fixed) — done in the 2026-08-23 paper tranche.
- [ ] **3.9** (memo) Configuration-specific ρ rationale: each configuration is a self-contained three-country world, so ρ legitimately varies by configuration — replace the narrative-assignment justification with this argument when rebuilding §4.2.
- [ ] **3.10** (memo M2) NFA sensitivity in the calibration: report ρ* at the imbalanced (US-deficit) baseline via the general-baseline threshold — computed benchmark values: 3% A-deficit ⇒ ρ* 4.64–5.10 (vs 3.96 balanced), 6% ⇒ 7.07, 3% surplus ⇒ 3.42.
- [ ] **3.11** (memo) Report Δq alongside Δe in the calibration outputs (solver already returns log_q; extend `precompute_calibration_panel.py` and the results figure).

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
- [x] **4.10** Flag trade-war e_AB-unchanged as a knife-edge — done in the 2026-08-23 tranche (with the asymmetric-war boundary added).
- [ ] **4.11** (memo) New "Scope and Modelling Choices" section placed **before** the three-country model: long-run object; one-factor exactness as a separate justification; capital-accumulation vs financial-account distinction; country-count trilemma (table); the single-aggregate cost stated plainly + pair-by-pair-diagnostic follow-up. Use the corrected NFA sentence (general-baseline structure intact; location moves — see §4a amendment b), NOT the memo's "level but not comparative static" claim.
- [ ] **4.12** (memo) Re-lean intro, §2.3, abstract, and conclusion to connection-first positioning (PTA connection as headline; isolated tariff ≡ preferential arrangement stated formally; impossibility as the story of why the connection was invisible; memo §6 statement as the canonical contribution, amended per §4a).
- [ ] **4.13** (memo M1) Real-rate result: state propositions for e; add the ρ*(q) = 4.93 > ρ*(e) = 3.96 result with the mechanical-CPI intuition, the Balassa–Samuelson sentence, and the non-tradables-inert-for-the-mechanism point; report Δq alongside Δe in the tariff experiments.
- [ ] **4.14** (memo) §3.3–3.4 additions: the natural-language trap (China–Vietnam vs US–China is the ρ-vs-η gap); home-bias-vs-nest division of labor with ∂ρ*/∂α_D = 3[(η−1)+α_T] > 0; two-level nest necessary-and-sufficient statement (no bilateral heterogeneity).
- [ ] **4.15** (memo M2) NFA robustness paragraph (scope section and/or §3.3): threshold structure intact at imbalanced baselines via the general-baseline proposition; location shifts reported.

### Phase 5 — Minor comments sweep (referee §7)

- [ ] **5.1** State once, early: e is a relative wage in a real model with no nominal anchor.
- [ ] **5.2** Percent-change convention (positive = depreciation of first-named currency) moved from figure notes to text.
- [ ] **5.3** Figure 1 tariff legend overlap fixed.
- [ ] **5.4** §2.2 opening cross-reference ("Section 2" → "Section 2.1").
- [x] **5.5** Bibliography additions — 13 entries added 2026-08-23 (Caliendo–Parro, Ossa, Costinot–Rodríguez-Clare, Bagwell–Staiger 1999, Bond–Syropoulos, Ornelas, Itskhoki–Mukhin, EKNR, CDP, Corsetti–Lloyd–Ostry 2025, Werning et al. 2025, Kalemli-Özcan et al. 2025, Obstfeld 2025). *Still to add (memo):* Viner (1950), Mundell (1964), Kemp–Wan (1976), Bagwell–Staiger (2002), Chang & Winters (2002), Krugman (1991), Yi (2000) — wire in with items 4.11–4.12. FLOR recitation check remains (Phase 3).
- [ ] **5.6** README + dashboard About text updated to the new narrative (README currently states the old claim).

### Phase 6 — Response to referee

- [ ] **6.1** Point-by-point response letter. Tone: accept the diagnosis, document the fix. Where we found *more* than the referee (the income-formula bug explaining the replication discrepancy; the ROW sign flip under the corrected model; the asymmetric impossibility observation), say so plainly — it demonstrates the revision is load-bearing, not cosmetic.

---

## 6. Open decisions (user input needed)

| # | Decision | Resolution |
|---|---|---|
| D1 | Ricardo–Viner extension (4.7) | **DECIDED (user, 2026-08-23): implement**, conditional on results aligning nicely and not adding excess complexity. Plan: numeric prototype first (Y_T = A·L_T^γ); write §3.4 only if the threshold comparative static is clean (expected: upward-sloping export supply in C lowers ρ*). |
| D2 | ROW configuration (3.7) | **DECIDED (delegated to us, 2026-08-23): keep ROW and construct the matched index** — strip the CNY component out of the Fed H.10 broad dollar index using published weights and renormalize, giving a "world minus US minus China" trade-weighted rate. Note: under the share-linear corrected model ROW performs well (+2.43 vs AE-index +2.18), strengthening the case for keeping it with a defensible index. Implementation in Phase 3 (`fetch_fx_data.py`). |
| D3 | FX comparison window (3.6) | Extend through end-2025, reframe as illustration, or both. Current recommendation: both. *(open)* |
| D4 | Flat CES in main text as Prop. 1's vehicle, nest as main spec? | Yes (referee's structure) — being implemented in the Phase 4 rewrite. |

Additional convention decision (ours, 2026-08-23): the paper and code use the **share-linear CES convention** throughout (utility weights α^(1/σ); weights = unit-price expenditure shares). `economy.py` switched accordingly (commit `41305c4`); symmetric results invariant; calibration panel/figure regenerated.

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
