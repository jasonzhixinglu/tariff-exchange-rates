# Streamlined Derivation Structure

## Objective

Rewrite the current `model_derivations_streamlined` into a shorter, more derivation-centered theoretical note.

The current version is still too expository and too organized around a pedagogical progression from two countries to three countries and only afterward to the general framework.

The new version should instead:

1. Introduce the general N-country environment and equilibrium machinery first.
2. Derive the general local representation of tariff disturbances and exchange-rate adjustment.
3. Then study the implications of that general framework for:
   - N = 2,
   - N = 3,
   - general symmetric N.
4. Treat the NEER result as the natural aggregate counterpart of the bilateral results.
5. Move secondary results into a compact extensions section.
6. Reduce the introduction, conclusion, and interpretive prose substantially.

The target should be a compact theoretical derivation note rather than a pedagogical exposition.

A reasonable target length is approximately 11-13 pages, excluding any appendices.

---

# 1. Introduction

Target: approximately half a page.

State only the central question and main result.

Suggested content:

- In a two-country model, an import tariff appreciates the tariffing country's currency under the Marshall-Lerner condition.
- In a multilateral setting, a discriminatory tariff also reallocates expenditure across foreign suppliers, so bilateral exchange-rate responses need not share the same sign.
- The paper characterizes this distinction in an N-country model.
- Under symmetry, the bilateral response against an untreated country can reverse when cross-origin substitution is sufficiently strong, but the tariffing country's effective exchange rate continues to appreciate.
- The exact NEER result relies on the symmetric nested-CES environment; the disturbance-adjustment decomposition and the distinction between aggregate and cross-origin adjustment are more general.

Do not include:
- a long bullet list of all later results,
- a detailed roadmap,
- the four-level hierarchy as a separate exposition block,
- detailed discussion of asymmetry, real rates, trade wars, or PTA theory.

Move directly to the model.

---

# 2. N-Country Model and Equilibrium

This section should contain all common machinery used later.

## 2.1 Production and preferences

Present:

- production of tradables and non-tradables,
- producer-price normalization,
- wages,
- the nested demand system,
- definitions of $\alpha_T$, $\alpha_D$, $\eta$, $\rho$, and $\beta_{ij}$.

State concisely:

- $\eta$ governs substitution between domestic and imported tradables,
- $\rho$ governs substitution across foreign origins conditional on importing.

One short qualification is sufficient:

The two margins are economically more general than nested CES, while the constant-elasticity representation and exact closed forms derived below are model-specific.

Define the symmetric benchmark here.

## 2.2 Prices, expenditure, income, and trade balance

Present without extended exposition:

- tariff-inclusive bilateral prices,
- import and tradable price indices,
- expenditure shares,
- tariff revenue and income,
- bilateral border flows,
- trade balances,
- balanced-trade closure.

Keep only enough prose to define each object.

## 2.3 Exchange-rate concepts

Define:

- $e_{ij}$ and the sign convention,
- $\nu_j=d\log e_{Aj}$,
- relative wages,
- terms of trade,
- bilateral real exchange rates,
- NEER and REER.

State once that nominal exchange rates, common-currency relative wages, and inverse terms of trade move one-for-one under the production normalization.

## 2.4 General linearization

Linearize the N-country equilibrium at a balanced free-trade baseline.

Derive:

$$
dp_{ij}=\nu_j-\nu_i+dt_{ij},
$$

the changes in price indices, expenditure shares, income, and trade balances.

Stack the system as:

$$
J\,d\nu+G\,d\tau=0.
$$

For a tariff experiment $d\tau=a\,d\tau$, define:

$$
F=Ga,
$$

so that:

$$
J\,d\nu=-F\,d\tau,
$$

and therefore:

$$
\frac{d\nu}{d\tau}=(-J)^{-1}F.
$$

Interpret this in no more than one short paragraph:

- $F$ is the vector of trade-balance disturbances created by the tariff at unchanged exchange rates.
- $J$ describes how trade balances respond to exchange rates.

State explicitly that this local disturbance-adjustment representation is more general than the nested-CES specification.

## 2.5 Multilateral Marshall-Lerner condition

Derive only what is needed to establish the sign structure of the adjustment mechanism.

Using homogeneity, Walras' law, and gross substitutability, establish the sufficient conditions under which $-J$ is a nonsingular M-matrix:

$$
(-J)^{-1}\geq0.
$$

State the sign rule:

$$
\operatorname{sign}
\left(
\frac{d\nu_i}{d\tau}
\right)
=
\operatorname{sign}
\left(
\sum_j \omega_{ij}F_j
\right),
\qquad
\omega_{ij}=((-J)^{-1})_{ij}\geq0.
$$

Interpretation:

Bilateral ambiguity comes from mixed-sign tariff disturbances $F$, not from a perverse exchange-rate adjustment mechanism.

Do not include extended matrix-theory discussion beyond what is needed for this result.

---

# 3. Tariff Responses: Two, Three, and N Countries

This is the main comparative-statics section.

The cases below should be presented as specializations of the general system in Section 2, not as separate models constructed from scratch.

## 3.1 Two countries

Specialize the general equilibrium system to N = 2.

Define:

$$
m=\alpha_T(1-\alpha_D),
$$

$$
\rho_1^*
=
1+\alpha_D(\eta-1)-\alpha_T(1-\alpha_D),
$$

$$
D_2=2\alpha_D(\eta-1)+1.
$$

Derive:

$$
\frac{d\log e_{AB}}{d\tau}
=
-\frac{\rho_1^*}{D_2}.
$$

Show compactly that:

$$
\rho_1^*>0,
$$

and that:

$$
D_2
=
\epsilon_X+\epsilon_M-1.
$$

Result:

Under the Marshall-Lerner condition, a unilateral import tariff appreciates the tariffing country's currency.

The interpretation should be no more than a few sentences.

Move the exact finite-tariff Cobb-Douglas solution to an appendix unless it is needed elsewhere.

## 3.2 Three countries

Now specialize the same framework to A, B, and untreated bystander C under symmetry.

Derive the two-equation system directly and obtain:

$$
\frac{d\log e_{AB}}{d\tau}
=
-\frac{\rho+3\rho_1^*}{3D_3}<0,
$$

$$
\frac{d\log e_{AC}}{d\tau}
=
\frac{\rho-3\rho_1^*}{3D_3},
$$

$$
\frac{d\log e_{BC}}{d\tau}
=
\frac{2\rho}{3D_3}>0.
$$

State the impact disturbances:

$$
F_B<0,
$$

$$
F_C\propto \rho-\rho_1^*.
$$

Result:

A always appreciates against tariff target B, while A depreciates against untreated C iff:

$$
\rho>3\rho_1^*.
$$

Interpret the difference between the impact threshold $\rho_1^*$ and equilibrium threshold $3\rho_1^*$ through the general sign rule.

Do not repeat the general $F$-$J$ framework here; simply apply it.

The single-elasticity impossibility result can appear as a short corollary or footnote.

## 3.3 General symmetric N

Let A tariff B and let the remaining N-2 countries be symmetric bystanders.

Derive the reduced system and obtain:

$$
D_N
=
N\alpha_D(\eta-1)+(N-2)\rho+1,
$$

$$
\frac{d\log e_{AB}}{d\tau}
=
-
\frac{
N\rho_1^*+(N-2)\rho
}{
ND_N
}
<0,
$$

$$
\frac{d\log e_{AC}}{d\tau}
=
\frac{
\rho-N\rho_1^*
}{
ND_N
},
$$

$$
\frac{d\log e_{BC}}{d\tau}
=
\frac{
(N-1)\rho
}{
ND_N
}
>0.
$$

Result:

The bystander bilateral rate reverses iff:

$$
\rho>N\rho_1^*.
$$

Interpretation:

Trade diversion is spread across N-2 bystanders, so stronger cross-origin substitution is required to reverse any individual bilateral exchange rate.

Call this dilution, but do not devote a separate exposition section to it.

The exact linearity of the threshold in N should be identified as a symmetric nested-CES result.

---

# 4. Bilateral versus Effective Exchange Rates

This section should present the central aggregate result immediately after the bilateral results.

Using the general symmetric N solution:

$$
\frac{d\nu_A^E}{d\tau}
=
\frac{
\nu_B+(N-2)\nu_C
}{
N-1
}
=
-\frac{\rho_1^*}{D_N}<0.
$$

Also show:

$$
\nu_B-\nu_C
=
-
\frac{
(N-1)\rho
}{
ND_N
}
d\tau.
$$

Result:

Under symmetry, a unilateral tariff appreciates the tariffing country's NEER for every N and every $\rho$ satisfying the equilibrium condition, even when some bilateral exchange rates reverse.

Interpretation should be concise:

- $\rho$ governs the relative distribution of exchange-rate adjustment across foreign partners.
- Its direct terms cancel from the NEER numerator under symmetry.
- $\rho$ remains in $D_N$, so it still affects the magnitude of the aggregate response.
- The two-country appreciation result therefore survives multilateralization as an effective, rather than universally bilateral, result.

State immediately:

The exact cancellation is specific to the symmetric nested-CES environment. The distinction between aggregate home-versus-foreign adjustment and reallocation across foreign suppliers is more general.

Do not include a separate empirical-location discussion here unless it is essential to the paper.

---

# 5. Extensions

Keep this section compact. These are extensions of the main results, not equal-weight components of the central argument.

## 5.1 Alternative tariff configurations

Use linearity and superposition.

### Broad unilateral tariff

Show that treating all foreign suppliers symmetrically eliminates tariff-induced cross-origin reallocation.

Derive the common bilateral response and the NEER response.

State:

Bilateral ambiguity arises from discrimination across foreign suppliers, not protection itself.

### Symmetric trade war

Derive:

$$
\frac{d\log e_{AB}}{d\tau}\bigg|_w=0,
$$

and:

$$
\frac{d\log e_{AC}}{d\tau}\bigg|_w
=
\frac{\rho-\rho_1^*}{D_N}.
$$

Then derive the NEER.

Result:

The belligerents' effective rates depreciate iff:

$$
\rho>\rho_1^*,
$$

independently of N.

Interpret in one paragraph: retaliation cancels the direct bilateral component between A and B, leaving the bystander reallocation margin decisive.

## 5.2 Real exchange rates

Derive the common bilateral real-rate expression:

$$
d\log q_{Aj}
=
\left(
1-\frac{mN}{N-1}
\right)\nu_j
-
\frac{m}{N-1}d\tau.
$$

Present the real bilateral threshold and REER result compactly.

Main result:

The direct CPI effect makes real bilateral reversal harder than nominal reversal and reinforces effective appreciation.

Do not expand this section unless real rates are important for the main paper.

## 5.3 Asymmetry

Begin with:

The $J$-$F$ framework remains valid without symmetry; the exact thresholds and NEER cancellation do not.

### General asymmetric baseline

State the general three-country sign condition sufficiently to show that the bystander numerator becomes a polynomial in $\rho$ whose coefficients depend on bilateral shares, country sizes, and home shares.

The main point:

Away from symmetry, no universal bilateral threshold exists.

Avoid unnecessary algebra if the full expressions are already in an appendix.

### Structured asymmetry

Introduce the $\kappa$ parameterization only because it gives a tractable way to study target importance across N.

State:

- $\kappa=1$ reproduces symmetry.
- $\kappa>1$ corresponds to an over-weighted tariff target.
- $\kappa<1$ corresponds to an under-weighted target.

Present the large-N result and the finite-N reversal threshold.

Main conclusion:

The symmetric NEER result is exact under symmetry and approximately robust within this structured asymmetric family, but sufficiently small target weight combined with sufficiently strong cross-origin substitution can reverse the NEER.

Do not claim robustness to arbitrary asymmetric trade networks.

---

# 6. Relation to the Canonical PTA Model

Keep this section short.

## 6.1 Competing exporters

Present the canonical importer-two-exporter setup and derive:

$$
\frac{dq_B}{dt_B}<0,
\qquad
\frac{dq_C}{dt_B}>0.
$$

State the Viner-Mundell result.

## 6.2 Relation to the present model

Explain concisely why the canonical result is sharper.

The canonical environment removes margins that oppose diversion toward C:

1. B and C are competing exporters rather than full trading partners.
2. A does not produce the imported good, eliminating home substitution.
3. Quasilinearity removes income effects.

Therefore the unconditional Viner-Mundell sign is not a competing mechanism. It corresponds to a restricted environment in which the bilateral-reversal threshold cannot bind.

Retain the threshold decomposition only if it materially clarifies these three forces.

Compress or move the broader literature mapping to a footnote or appendix.

---

# 7. Conclusion

Target: approximately half a page.

Summarize only the central derivational result:

- The general equilibrium response is $(-J)^{-1}F$.
- At N = 2 this reduces to the standard Marshall-Lerner appreciation result.
- At N >= 3, discriminatory tariffs generate foreign-supplier reallocation and potentially mixed bilateral responses.
- Under symmetry, the bystander reversal threshold is $N\rho_1^*$.
- Aggregation removes the direct reallocation term from the NEER numerator, preserving effective appreciation.
- Configuration and asymmetry determine the limits of this aggregate result.

End with the distinction between:

- aggregate home-versus-foreign adjustment, and
- reallocation across foreign suppliers.

Do not restate every extension.

---

# General Editing Rules

1. Preserve all correct derivations and notation unless restructuring requires moving them.
2. Reuse existing equation labels where practical, but prioritize internal consistency of the new file.
3. Do not re-derive the same common objects separately in the N = 2, N = 3, and general-N sections.
4. All common machinery belongs in Section 2.
5. Treat N = 2, N = 3, and general N as specializations of the same equilibrium framework.
6. Let equations carry the argument.
7. Avoid the sequence: motivate -> preview result -> derive -> restate result -> explain result again.
8. For most results, use: derivation -> formal result -> one short interpretation.
9. Remove pedagogical transitions such as "before deriving this, it is useful to ask..." unless they are strictly necessary.
10. Remove repeated explanations of the two substitution margins.
11. Remove repeated explanations of $F$ and $J$ after Section 2.
12. Remove repeated caveats about symmetry; state them at the specific result where they matter.
13. Move nonessential robustness checks, exact special cases, long literature comparisons, and secondary derivations to an appendix where appropriate.
14. Do not add new results or alter the economics.
15. Preserve the distinction between:
    - the general disturbance-adjustment representation,
    - the broad economic distinction between aggregate and cross-origin adjustment,
    - nested-CES closed forms,
    - symmetry-specific exact thresholds and cancellations.
16. Aim for approximately 11-13 pages in the main text.
17. The final document should read like compact theoretical derivation notes or a theory appendix, not like lecture notes.