# Revision Framing Memo

**Paper:** Trade Tariffs and Exchange Rates: Revisiting Conventional Wisdom in a Three-Country Framework

**Purpose:** Record the reasoning behind the repositioning of the paper, the new framing of the theoretical results, and the agreed statement of the contribution. Companion to the referee report (`referee_report_tariffs_fx.md`) and the derivation script (`threecountry_threshold.py`).

---

## 1. Where the current draft went wrong

Three problems, of decreasing severity.

**The headline result is not produced.** The draft claims that a selective tariff can depreciate A's currency against the untariffed third country, but no figure and no calibration exhibits it. Figure 6 reports $\Delta\log e_{AC} = 0.00$ at $\sigma = 2$; Table 4 Panel A reports $\Delta e_{AC} < 0$ in all eight configurations, including Vietnam at $\sigma = 8$.

**The opponent is the wrong one.** The draft positions itself against Lerner–Metzler–Mundell (1961) — the textbook prior, not the frontier. In this model class the exchange rate is the common-currency relative wage, an object the quantitative trade literature computes routinely and the PTA literature has studied under the name "terms of trade" since Viner.

**The calibration doesn't support the abstract.** Sign agreement in Regime 2 holds for two of eight configurations, both safe-haven currencies; the six failures sit in an appendix.

The rest of this memo is about the first two. The third is a rewriting and recalibration task, detailed in the referee report.

---

## 2. Why the result was unreachable: the impossibility finding

The draft's specification uses a single elasticity $\sigma$ across all tradable varieties. That parameter is doing double duty. Raising it strengthens substitution between B and C in A's basket (trade diversion, pushing toward depreciation against C), but simultaneously strengthens substitution between foreign and domestic goods (conventional expenditure switching, pushing toward appreciation) and C's substitution toward cheapened B goods (redirection). The draft is trying to reach a threshold with a parameter that also raises it.

Separating the two margins — $\eta$ for home-vs-import, $\rho$ for across foreign origins — and differentiating the balanced-trade conditions at the symmetric free-trade point gives

$$\left.\frac{d\log e_{AC}}{d\tau}\right|_{\tau=0} = \frac{\rho - \rho^*}{3\big[3\alpha_D(\eta-1)+\rho+1\big]}, \qquad \rho^* = 3\big[1 + \alpha_D(\eta-1) - \alpha_T(1-\alpha_D)\big]$$

Imposing $\rho = \eta = \sigma$ recovers the draft's specification and yields

$$\rho^* - \sigma = \sigma(3\alpha_D - 1) + 3 - 3\alpha_D - 3\alpha_T(1-\alpha_D)$$

The threshold chases $\sigma$ at rate $3\alpha_D$, so a crossing exists only if $\alpha_D < 1/3$ — a home share of tradable expenditure below one-third, which no actual economy satisfies.

> **Proposition (impossibility).** In a flat CES with a common elasticity across all tradable varieties, the conventional appreciation result holds for every $\sigma > 0$ whenever $\alpha_D \ge 1/3$.

The draft's calibration ($\alpha_D = 1/3$, $\alpha_T = 3/4$) sits exactly on the knife edge, with a constant gap of $+0.50$ and $d\log e_{AC}/d\tau = -1/(12\sigma) \to 0^-$. Figure 6 is not a near-crossing; it is an asymptote the specification cannot reach.

**This is the paper's story about the literature, not just a technical fix.** Anyone extending the two-country model to three with a standard Armington structure — the obvious first thing to try — would have found the conventional result surviving and concluded the multilateral extension was uninteresting. The connection to the PTA literature was invisible because the standard specification conflates the two elasticities that make it visible. This belongs in the framing, and it makes the contribution look inevitable in hindsight.

At realistic parameters ($\alpha_D = 0.80$, $\alpha_T = 0.40$, $\eta = 1.5$), $\rho^* = 3.96$ — inside the range of measured cross-origin elasticities. The threshold falls monotonically in tariff size (to 2.70 at $\tau = 1.45$), so the local result is a conservative upper bound. It rises as the third country shrinks (Vietnam: 8.76), which is a substantive finding for the calibration section, since Vietnam is currently presented as the natural home for the mechanism when in fact it faces the highest bar.

---

## 3. The new framing

### 3.1 Positioning: a connection, illustrated

The paper points out that the PTA literature bears directly on the conventional tariff–exchange-rate wisdom, and illustrates that connection with minimal theory in a three-country setting.

Deliberately modest. The alternative — claiming a discovery about two literatures talking past each other — invites the "is this actually new?" fight the paper cannot win on the mechanism alone. Under the modest framing the threshold result becomes a bonus rather than a load-bearing promise.

The substantive content of the connection:

- An isolated tariff by A on B is formally a preferential arrangement in favour of C. Up to the level of the external tariff and revenue treatment, "raise $\tau_{AB}$, hold $\tau_{AC} = 0$" and "cut $\tau_{AC}$, hold $\tau_{AB}$ fixed" are the same discriminatory wedge.
- The PTA literature has tracked the third-country consequences of that wedge since Viner (1950), through Mundell (1964) on tariff preferences and the terms of trade, Kemp–Wan (1976), and the Bagwell–Staiger (1999, 2002) terms-of-trade externality framework.
- Its object of interest is welfare, but the mechanism it tracks — and the intermediate object in nearly every proposition — is the bilateral terms of trade.
- Adding labour with linear technology makes producer prices unit labour costs, so the terms of trade *is* the relative wage; denominating in currencies makes it the nominal rate. Three names for one number.
- Empirical support for the channel already exists: Chang & Winters (2002) measure excluded-country price responses to Mercosur.

The FX-attribution debate has not touched any of this, because it inherited a two-country prior. When the dollar weakened in April 2025, the inference ran: two-country theory predicts appreciation, the dollar depreciated, therefore something non-trade did it. That inference is unsound for reasons the trade literature has known for decades but has never had occasion to state in exchange-rate terms.

### 3.2 Scope and modelling choices

A single confident subsection, placed **before** the three-country model, not after. Each restriction defended by purpose, not confessed as a limitation.

**Long run.** The paper characterizes the real exchange rate consistent with a stationary external position. This rules out nominal rigidities, which govern the speed of adjustment, and portfolio flows, which govern deviations during the transition. Balanced trade is the NFA $= 0$ normalization of the intertemporal budget constraint; a country with non-zero NFA runs a permanent balance servicing it, which shifts the level but not the comparative static.

**One factor** — a *separate* justification, not a consequence of the long-run choice. Ruling out nominal and financial frictions gets you to a static real model; it does not by itself force a single factor. One factor is what makes producer prices unit labour costs, hence makes the terms of trade *equal* the relative wage rather than merely correlated with it. That exactness is what licenses the translation. State the two arguments independently.

**No capital.** Domestic capital accumulation mainly concerns adjustment dynamics and shifts steady states slightly — second-order for a long-run sign result. Distinguish this in one clause from the international financial account, which is a different and deeper departure: accumulation shifts steady states, a financial account replaces the equilibrium condition.

**Three countries.** The country-count trilemma:

| | heterogeneity | closed-form results |
|---|---|---|
| symmetric $n$-country | ✗ | ✓ |
| quantitative $n$-country | ✓ | ✗ |
| three-country | ✓ | ✓ |

Symmetric $n$-bloc models (Krugman 1991; Bond–Syropoulos 1996; Yi 2000) buy tractability by removing exactly the heterogeneity the 2025 episode requires — you cannot ask "what if C is small and highly substitutable while D is large and not." Quantitative models (Caliendo–Parro; Ossa; Costinot–Rodríguez-Clare) buy heterogeneity at the cost of propositions. Three countries is the smallest setting in which discrimination is possible at all — you need a tariffed and an untariffed foreign partner — and generically the largest in which sign conditions remain analytically available. The Jacobian is $2\times 2$; at $n = 4$ the cofactor expansion yields nothing interpretable. Our own asymmetric-size threshold already degrades to an unenlightening quadratic root, which illustrates the point at $n = 3$.

**The cost, stated plainly.** With a single untariffed aggregate the model cannot represent simultaneous appreciation against some partners and depreciation against others — arguably what happened in April 2025, and what Table 4 shows the data doing. One sentence, no hedging. It also defines the natural follow-up: use $\rho^*$ as a pair-by-pair diagnostic inside a calibrated many-country model.

### 3.3 Specification: what the nest is and is not

The two-level nest ($\eta \ne \rho$) is **necessary and sufficient** for the reversal. Foreign suppliers remain symmetric substitutes for one another at elasticity $\rho$; only the home-vs-foreign margin is separated.

Non-symmetric *bilateral* elasticities (China–Vietnam closer than China–Germany) are **not required** and should be avoided: they need a three-level nest or CRESH and introduce parameters that cannot be disciplined. Varying $\rho$ across configurations already handles the Vietnam-vs-Canada distinction, since each configuration is a self-contained three-country world — and this is a cleaner justification for configuration-specific elasticities than the current narrative assignment.

Note the natural-language trap: "Chinese and Vietnamese goods are closer substitutes than US and Chinese goods" sounds like bilateral heterogeneity but is exactly the $\rho$-vs-$\eta$ gap. US–Chinese is home-vs-foreign; Chinese–Vietnamese is foreign-vs-foreign.

**Home bias is a recalibration, not a modelling change, and it does not substitute for the nest.** $\partial\rho^*/\partial\alpha_D = 3[(\eta-1) + \alpha_T] > 0$: raising home bias *raises* the bar, modestly. Its job is credibility — killing the "the US spends 16.5% of income on Chinese goods" objection and bringing the Table 4 magnitudes down from the absurd. The nest's job is the result. Fixing $\alpha_D$ alone under a single $\sigma$ leaves the paper strictly worse off, since the gap then grows at rate $3\alpha_D - 1 > 0$.

### 3.4 Real versus nominal

The object is the long-run **real** rate. With non-tradables, $q_{AC} = e_{AC}P_C/P_A$ and $P_i = P_{T_i}^{\alpha_T}P_{N_i}^{\alpha_N}$. Since $P_{N_i} = A_{T_i}/A_{N_i}$ is pinned by productivities and moves one-for-one with the wage, $q$ and $e$ move together but not identically — the CES tradable index responds to the tariff and to relative wages. Report $\Delta q$ alongside $\Delta e$ in the tariff experiments and confirm $\rho^*$ is unchanged; if it differs, that is itself a result.

A Balassa–Samuelson-flavoured observation worth one sentence: since $P_N$ is a pure productivity ratio untouched by the tariff, all real-exchange-rate action runs through tradables. This also answers the objection that non-tradables are inert — they are inert *for the mechanism* but govern the mapping from $e$ to $q$, which is now a stated object rather than a nuisance.

Adopting the long-run real framing explicitly converts the calibration section's failures from embarrassments into predictions: if the object is the long-run real rate, the April 2025 safe-haven pattern is exactly what the model should miss, and saying so in advance is far stronger than conceding it afterward. It also gives a principled reason to extend the comparison window — not because more data is better, but because the model's object only becomes visible as the transition plays out.

---

## 4. Errors to fix regardless of framing

1. **Eq. (28)** has a spurious $e_{ik}$ in the export term; with $P_{T_i} = 1$ in $i$'s currency, export value in $i$'s currency is $C_{T_ik}$, as eq. (9) correctly states. Implementing (28) literally gives $\log e_{AB} \approx -369$, so this is a typo, not a code bug.
2. **Eqs. (26)–(27) contradict §3.1.2.** The denominator $D_k$ is a flat-CES price index over all four goods; §3.1.2 and eq. (23) specify a Cobb–Douglas outer nest. These coincide only at $\sigma = 1$ — consistent with our replication matching the reported $\sigma = 1$ equilibrium to two decimals but diverging at $\sigma = 0.5$ and $\sigma = 2$. Determine which the code implements. Note $\alpha_N$ is not inert under the flat version.
3. **§3.2.3's magnitude claim has the wrong sign** in the draft's own specification: under a single $\sigma$ the trade-war depreciation is *decreasing* in the elasticity ($+0.094 \to +0.046$ as $\sigma: 1.5 \to 10$). It increases only when $\eta$ is held fixed and $\rho$ rises ($+0.016 \to +0.252$) — another argument for the nest.
4. **§2.2 restatement.** Lemmas 2.1–2.2 are Marshall–Lerner in different clothing. State that plainly; it is cleaner and sets up §3 better, since the interesting point is that bilateral Marshall–Lerner does not pin down the multilateral sign.

---

## 5. Proposed structure

1. **Introduction.** Motivation from the 2025 attribution debate. Positioning as a connection to the PTA literature, illustrated.
2. **Two-country benchmark.** Retained; §2.2 restated as Marshall–Lerner.
3. **New: the equivalence.** $e \propto$ relative wage $\propto$ terms of trade. Situate against Viner, Mundell (1964), Kemp–Wan, Bagwell–Staiger, Chang–Winters, and the quantitative trade literature. Say explicitly what is being added.
4. **New: scope and modelling choices** (§3.2 above), placed *before* the model.
5. **Three-country model**, restructured around two propositions:
   - *Proposition 1 (impossibility)* — lead with this.
   - *Proposition 2 (threshold)* — $\rho^*$, with comparative statics in home bias, macro elasticity, third-country size, and tariff magnitude.
   - Trade war: unambiguous, magnitude increasing in $\rho$ (corrected).
   - Compress Figures 2–7 into one multi-panel figure plus a threshold plot.
6. **Calibration**, rebuilt: import-share-based expenditure weights, country-specific preferences, $(\eta,\rho)$ pairs from the literature, results over a grid with $\rho^*$ marked, all configurations in the main text, extended comparison window, $\Delta q$ alongside $\Delta e$.
7. **Conclusion.** The inferential payoff.

---

## 6. The contribution, as stated

> The exchange rate in this class of models is the common-currency relative wage, and therefore the bilateral terms of trade — the object the preferential-trade-agreement literature has studied since Viner. A selective tariff is formally a preference in favour of the untariffed partner, so that literature bears directly on the tariff–exchange-rate question, and we illustrate the connection with minimal theory in the smallest multilateral setting.
>
> Doing so yields two results. First, the connection is invisible under the standard Armington specification: with a common elasticity across all tradable varieties, the conventional appreciation result survives the three-country extension *as a theorem*, for every $\sigma$, at any plausible home bias. Second, it fails once the home-vs-import and cross-origin elasticities are separated, and we derive the exact threshold $\rho^*$ at which it does. At US-realistic parameters $\rho^* \approx 4$, inside the range of measured cross-origin elasticities, and the threshold falls as tariffs grow.
>
> Consequently, bilateral appreciation against a tariffed partner can coexist with depreciation against untariffed ones, and observed multilateral depreciation during a tariff episode cannot be attributed to financial or convenience-yield channels on the strength of the two-country prior alone. The results characterize the long-run real exchange rate consistent with a stationary external position; short-horizon dynamics require nominal rigidities and a financial account, which is why the 2025 data agree in sign only where safe-haven demand did not dominate.

---

## 7. Open items

- Re-derive $\rho^*$ under Ricardo–Viner ($Y_{T_i} = A_{T_i}L_{T_i}^{\gamma}$, $\gamma < 1$) to formalize the export-supply channel currently only discussed verbally in §3.3. Expect $\rho^*$ to fall.
- Re-solve with $TB_i = -b_i$ for exogenous $b_i$ to confirm the threshold is robust to non-zero steady-state NFA.
- Confirm $\rho^*$ is unchanged when stated for $q$ rather than $e$.
- Check whether Ossa (2014) or the PTA terms-of-trade papers state the third-country ambiguity as a proposition. If yes, cite and lean harder on $\rho^*$ and the trade-war case; if no, say so explicitly.
- Verify the attribution of $\sigma \approx 6$ to Amiti–Redding–Weinstein; Fajgelbaum et al. (2020) or Feenstra–Luck–Obstfeld–Russ (2018) are the more natural anchors.
