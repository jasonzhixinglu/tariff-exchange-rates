# Streamlined Derivation Blueprint

## Objective

Rewrite the current `model_derivations_rewrite` into a substantially tighter set of theoretical derivations.

Preserve the conceptual sequencing of the current rewrite, which is superior to the original general-N-first organization:

1. Model and the two substitution margins
2. Two-country benchmark
3. Three-country model and bilateral ambiguity
4. General disturbance-adjustment representation
5. Aggregation and the NEER
6. General symmetric N
7. Alternative tariff configurations
8. Real exchange rates
9. Asymmetry
10. Relation to the canonical PTA model
11. Conclusion

The new version should retain the economic insights and generality caveats introduced by the rewrite, but remove most of the extended exposition surrounding the mathematics.

The target is a derivation-centered theoretical document, not a pedagogical essay.

## General Writing Rule

Use the following rhythm throughout:

**Motivation (1 short paragraph) -> derivation -> formal result -> interpretation (1 short paragraph).**

Do not separately preview, derive, restate, and then explain the same result.

Whenever the equations make a point transparent, let the equations carry the argument.

A typical subsection should therefore look like:

### X.X Descriptive title

One short paragraph stating what is being derived and why.

[Equations and derivation.]

**Result X.X.** Precise mathematical statement of the result.

One short paragraph interpreting the result economically and, where necessary, stating its scope.

Then move on.

## 1. Introduction

Target: approximately 1 page.

State the question immediately: how does the conventional two-country result that an import tariff appreciates the tariffing country's currency change in a multilateral setting?

State the central answer concisely:

- A unilateral tariff always appreciates A against the tariff target in the symmetric benchmark.
- With a third country, A can depreciate against an untreated country when cross-origin substitution is sufficiently strong.
- The bilateral ambiguity reflects foreign-supplier reallocation.
- Under symmetry, this reallocation cancels from the numerator of A's NEER response, so the conventional appreciation result survives in aggregate.
- With N countries, diversion toward each individual bystander is diluted, raising the bilateral reversal threshold.
- Asymmetry qualifies the exact NEER result.
- The canonical Viner-Mundell result emerges when margins opposing foreign-supplier diversion are removed.

Retain a very concise statement of the hierarchy of generality:

- General differentiable equilibrium: disturbance versus adjustment, $F$ and $J$.
- General economic mechanism: home-versus-foreign adjustment versus foreign-supplier reallocation.
- Nested CES: $\eta$ and $\rho$ provide constant-elasticity representations of these margins.
- Symmetric nested CES: exact thresholds and exact NEER cancellation.

Do not provide an extended roadmap.

## 2. Economic Environment

### 2.1 Production

State technology, prices, wages, and the normalization.

Keep interpretation to at most one paragraph.

### 2.2 Preferences

Present the two-layer demand system.

Immediately define:

- $\eta$: home-versus-import substitution.
- $\rho$: substitution across foreign origins.

Explain in 2-4 sentences why the distinction is inactive at N=2 and becomes active at N>=3.

Retain the caveat that analogous margins can exist outside nested CES, while the exact constant-elasticity representation is model-specific.

### 2.3 Policy, income, and trade balance

Derive tariff-inclusive prices, expenditure shares, tariff revenue, income, bilateral flows, and trade balance.

Avoid extensive verbal discussion between equations.

### 2.4 Exchange-rate concepts

Define nominal bilateral rates, relative wages, terms of trade, real exchange rates, NEER, and REER.

State the wage-exchange-rate-terms-of-trade equivalence once and move on.

## 3. Two Countries: Conventional Wisdom

Begin directly with N=2.

Derive the equilibrium tariff response:

$$
\frac{d\log e_{AB}}{d\tau}
=
-\frac{\rho_1^*}{D_2}.
$$

Show why $\rho_1^*>0$.

Then connect $D_2>0$ directly to the textbook Marshall-Lerner condition:

$$
\epsilon_X+\epsilon_M>1.
$$

**Result.** Under Marshall-Lerner, a unilateral import tariff appreciates the tariffing country's currency.

Interpretation: at fixed exchange rates the tariff creates a surplus for A; under Marshall-Lerner an appreciation eliminates it.

Keep the exact Cobb-Douglas solution if useful as a compact verification, but do not allow it to interrupt the main argument.

## 4. Three Countries: Bilateral Ambiguity

This is the first central multilateral derivation.

Introduce A, B, C and the tariff $d\tau=dt_{AB}$.

Derive the two-equation system and solve explicitly for $\nu_B$ and $\nu_C$.

Display prominently:

$$
\frac{d\log e_{AB}}{d\tau}
=
-\frac{\rho+3\rho_1^*}{3D}<0,
$$

$$
\frac{d\log e_{AC}}{d\tau}
=
\frac{\rho-3\rho_1^*}{3D}.
$$

**Result.** A always appreciates against B but depreciates against C iff

$$
\rho>3\rho_1^*.
$$

Interpret in one paragraph: the tariff shifts expenditure away from B; sufficiently strong cross-origin substitution redirects enough of it toward C to make C appreciate relative to A.

Retain the single-elasticity impossibility result, but present it as a short corollary rather than a long separate discussion.

## 5. Disturbance and Adjustment in General Equilibrium

Only now introduce the general linear representation:

$$
J\,d\nu+G\,d\tau=0.
$$

For a tariff experiment $d\tau=a\,d\tau$, define

$$
F=Ga,
$$

and therefore

$$
\frac{d\nu}{d\tau}=(-J)^{-1}F.
$$

Give the interpretation once:

- $F$: trade-balance disturbances at unchanged exchange rates.
- $J$: exchange-rate adjustment mechanism.

Develop the multilateral Marshall-Lerner condition sufficiently to establish when $-J$ is a nonsingular M-matrix and hence

$$
(-J)^{-1}\geq0.
$$

Then state the sign rule.

**Result.** Exchange-rate responses are nonnegative weighted combinations of the components of $F$. Opposite-signed bilateral responses therefore require mixed-sign trade-balance disturbances.

Connect this immediately back to the three-country case:

- $F_B<0$.
- $F_C$ can become positive because of diversion.
- Bilateral ambiguity comes from $F$, not from failure of the adjustment mechanism.

Avoid extended matrix-theory exposition beyond what is necessary to establish the result.

## 6. Aggregation: The NEER

This should remain a prominent section but be concise.

From the three-country solution derive:

$$
\frac{\nu_B+\nu_C}{2}
=
-\frac{\rho_1^*}{D}d\tau,
$$

$$
\nu_B-\nu_C
=
-\frac{2\rho}{3D}d\tau.
$$

**Result.** Under symmetry, a unilateral tariff appreciates A's NEER for every $\rho$ satisfying the equilibrium condition, even when the bilateral rate against C reverses.

Interpretation in one compact paragraph:

$\rho$ governs the relative allocation of adjustment across foreign currencies. Its direct terms cancel in the aggregate numerator, although $\rho$ remains in the denominator and therefore affects the magnitude of the NEER response. The two-country result is therefore best interpreted as an effective home-versus-foreign result that is also bilateral only because there is one foreign country.

Immediately state the caveat:

The exact cancellation is a property of the symmetric nested-CES environment. The distinction between aggregate home-versus-foreign adjustment and foreign-supplier reallocation is more general.

Do not repeat this interpretation elsewhere.

## 7. General Symmetric N: Dilution

Derive the reduced two-equation system for B and a representative bystander C.

Obtain:

$$
\frac{d\log e_{AB}}{d\tau}<0,
$$

$$
\frac{d\log e_{AC}}{d\tau}
=
\frac{\rho-N\rho_1^*}{ND_N}.
$$

**Result.** Bilateral reversal occurs iff

$$
\rho>N\rho_1^*.
$$

Interpretation: diversion is spread over N-2 bystanders, so increasingly strong cross-origin substitution is required to reverse any one bilateral exchange rate.

Then derive immediately:

$$
\frac{d\nu_A^E}{d\tau}
=
-\frac{\rho_1^*}{D_N}<0.
$$

State that N changes the magnitude but not the sign of the symmetric NEER response.

Keep the single-elasticity impossibility result compactly as a corollary.

## 8. Alternative Tariff Configurations

Use linearity/superposition rather than re-deriving the system.

### 8.1 Broad tariff

Derive the broad-tariff response and state why the cross-origin reallocation margin becomes inactive.

### 8.2 Symmetric trade war

Derive:

$$
\frac{d\log e_{AB}}{d\tau}\bigg|_w=0
$$

and the bystander/NEER response.

Highlight the threshold

$$
\rho>\rho_1^*,
$$

and its independence from N.

Interpretation: retaliation cancels the belligerents' bilateral component, leaving the bystander diversion margin to determine their effective exchange rates.

Keep this section derivational and short.

## 9. Real Exchange Rates

Derive the bilateral real-rate expression and the corresponding threshold.

Then derive the REER.

State the main result: under the maintained parameter restrictions, the unilateral tariff produces real effective appreciation, with the direct CPI effect reinforcing the nominal effective appreciation.

Avoid extensive discussion unless the real-rate result differs economically from the nominal result.

## 10. Asymmetry

Begin with the general statement:

The $J$-$F$ framework does not require symmetry; the exact closed-form thresholds and NEER cancellation do.

### 10.1 General asymmetric baseline

State the general three-country numerator result and explain briefly that the threshold becomes a function of bilateral shares, sizes, and the trade network.

Do not reproduce unnecessary algebra if it does not yield additional economic insight.

### 10.2 Structured asymmetry

Introduce the $\kappa$ parameterization because it gives a comparable notion of target importance across N.

Derive the large-N result and finite-N sign condition.

State clearly:

- $\kappa=1$: exact symmetric NEER result.
- $\kappa>1$: effective appreciation is robust in the relevant region.
- $\kappa<1$: sufficiently strong cross-origin substitution can reverse the NEER.
- The reversal threshold is of order N.

Interpretation: when the tariff target receives little NEER weight, depreciations against many bystanders can outweigh appreciation against the target.

End with one sentence:

The symmetric NEER result is exact under symmetry and approximately robust within this structured asymmetric family; robustness to arbitrary asymmetric trade networks is not claimed.

## 11. Relation to the Canonical PTA Model

Keep this section, but shorten it substantially.

Derive the Viner-Mundell competing-exporter result:

$$
\frac{dq_B}{dt_B}<0,
\qquad
\frac{dq_C}{dt_B}>0.
$$

Then explain the relationship to the present model in one compact subsection.

The canonical model removes margins that oppose diversion toward C:

1. B and C are competing exporters rather than full trading partners.
2. A does not produce the imported good, removing home substitution.
3. Quasilinearity removes income effects.

Therefore the Viner-Mundell sign is not a competing result. It corresponds to an environment in which the reversal threshold cannot bind.

Retain the decomposition of the threshold only if it directly demonstrates these economic forces. Compress the broader literature survey.

## 12. Conclusion

Target: no more than 3-5 paragraphs.

Summarize only the main logical chain:

1. Two countries: tariff appreciation under Marshall-Lerner.
2. Three countries: foreign-supplier reallocation makes bilateral responses ambiguous.
3. General equilibrium: $F$ describes the disturbance and $J$ the adjustment.
4. Under symmetry: aggregation removes the direct foreign-reallocation component, preserving NEER appreciation.
5. General N: diversion toward individual bystanders is diluted.
6. Asymmetry and tariff configuration determine the limits of the aggregate result.

End with the distinction between aggregate home-versus-foreign adjustment and reallocation across foreign suppliers.

Do not introduce new results in the conclusion.

# Editing Rules

1. Preserve all correct derivations and definitions unless restructuring requires moving them.
2. Do not simplify away mathematical steps needed to verify a result.
3. Remove prose that merely repeats what an equation or formal Result already establishes.
4. Avoid explaining the same intuition both before and after a derivation.
5. Use short transitions between sections.
6. Prefer precise economic terminology over pedagogical analogies.
7. Preserve the distinction between results that are general, nested-CES-specific, and symmetry-specific.
8. Do not claim that the NEER sign is generally invariant outside the symmetric benchmark.
9. Preserve technically important qualifications about $\rho$: it cancels from the NEER numerator under symmetry but remains in $D_N$ and therefore affects magnitude.
10. Preserve the distinction between the general $J$-$F$ framework and the special closed forms obtained under symmetry.
11. Do not add new literature, new results, or new model extensions.
12. The target length should be approximately 20-22 pages, but mathematical completeness takes priority over hitting an exact page count.
13. The final product should read like compact theoretical derivation notes suitable for an economics paper appendix or technical companion, while retaining the improved conceptual sequence of the current rewrite.