# Rewrite Blueprint: Trade Tariffs and Exchange Rates in a Multilateral World

## Purpose

This document provides the narrative architecture and draft prose for rewriting the existing model derivations while preserving the full algebra and mathematical content.

The rewrite should be organized around one progressive question:

> The two-country model predicts that a unilateral import tariff appreciates the tariffing country's currency. What exactly survives when the economy becomes multilateral?

The recurring conceptual distinction is:

\[
\boxed{\text{aggregate home-versus-foreign adjustment}}
\qquad\text{versus}\qquad
\boxed{\text{reallocation across foreign suppliers}}.
\]

The first margin governs the aggregate value of the tariffing country's currency. The second determines how the adjustment is distributed across individual foreign partners.

The proposed sequence is deliberately more pedagogical than the current derivation-first structure:

1. State the economic question and main answer.
2. Define only the model ingredients needed to understand the mechanisms.
3. Recover the two-country result.
4. Add a third country and expose the new multilateral margin.
5. Use the three-country case to motivate the general disturbance-adjustment framework.
6. Generalize to \(N\) countries.
7. Explore tariff configurations, real rates, asymmetry, and the PTA connection.
8. Conclude by returning to the distinction between aggregate adjustment and foreign-supplier reallocation.

The algebra should remain detailed. The change is in when it appears and what question each derivation is answering.

---

# 1. Introduction: What Survives from the Two-Country Model?

A familiar result in international economics is that an import tariff appreciates the currency of the country imposing it. The intuition is clearest in a two-country world. At the initial exchange rate, a tariff reduces import demand and creates a trade surplus for the tariffing country. Provided the Marshall-Lerner condition holds, an appreciation is required to restore trade balance.

In a multilateral world, however, this statement is incomplete. Once there is more than one foreign supplier, a tariff does not only change the tariffing country's demand for foreign goods in aggregate. It also changes the allocation of that demand across foreign countries. Expenditure displaced from the tariffed country can be diverted toward untreated trading partners, changing their trade balances and exchange rates as well.

This creates a distinction that does not exist in the two-country model: the tariffing country may appreciate against the country it tariffs while depreciating against some third countries. The bilateral statement that "a tariff appreciates the currency" therefore need not survive multilateralization.

The central result of this paper is that a closely related aggregate statement does. In the symmetric \(N\)-country model, a unilateral tariff always appreciates the tariffing country's nominal effective exchange rate, even when some individual bilateral exchange rates move in the opposite direction. Cross-origin substitution determines how the exchange-rate adjustment is distributed across foreign partners, but it does not overturn the sign of the aggregate response.

The results can be understood through a distinction that will recur throughout the analysis:

\[
\boxed{\text{aggregate home-versus-foreign adjustment}}
\qquad\text{versus}\qquad
\boxed{\text{reallocation across foreign suppliers}}.
\]

The two-country model contains only the first observable margin because there is only one foreign supplier. A multilateral model contains both. Bilateral exchange rates reflect both margins, whereas aggregation across trading partners largely removes the second. In this sense, the conventional two-country result is best understood as an aggregate result that happens also to be bilateral when there is only one foreign country.

The analysis develops this argument progressively. We first recover the conventional two-country result and connect it exactly to the Marshall-Lerner condition. We then add a single untreated country. This is the smallest environment in which foreign-supplier reallocation exists, and it is enough to generate the central bilateral ambiguity. We show that the tariffing country always appreciates against the target but can depreciate against the untreated country when cross-origin substitution is sufficiently strong. We then ask what happens to the overall value of the tariffing country's currency and show that the bilateral ambiguity disappears from the nominal effective exchange rate.

Only after these mechanisms are visible do we return to the general \(N\)-country system. The general framework separates the trade-balance disturbance created by the tariff from the exchange-rate adjustment that eliminates it, and the \(N\)-country solution shows that the same distinction survives at arbitrary dimension. Increasing the number of countries dilutes trade diversion toward any individual bystander, but leaves the sign of the effective response unchanged under symmetry.

We subsequently examine how the result depends on the tariff configuration and on symmetry. A broad tariff eliminates the foreign-supplier reallocation margin; reciprocal retaliation can instead make it decisive even for effective exchange rates. Asymmetric trade exposure breaks the exact cancellation underlying the symmetric result but preserves it to leading order. Finally, we relate the mechanism to the canonical theory of preferential trade agreements. The familiar Viner-Mundell result emerges as a special environment in which the forces opposing trade diversion toward the untreated exporter have been removed.

---

# 2. Economic Environment: Two Margins of Substitution

## 2.1 Production and Prices

Consider \(N\) countries indexed by \(i\). Each country produces a country-specific tradable and a nontradable using labor. The production side is deliberately simple: with linear technology and perfect competition, producer prices are pinned down by unit labor costs. Relative adjustment can therefore be represented entirely through exchange rates.

**[INSERT CURRENT TECHNOLOGY EQUATIONS AND PRICE NORMALIZATION.]**

Because wages are fixed in domestic currency, movements in nominal exchange rates, common-currency relative wages, and inverse terms of trade move one-for-one. The nominal exchange-rate results below can therefore also be read as relative-wage or terms-of-trade results.

## 2.2 Preferences: Home Versus Foreign and Foreign Versus Foreign

The demand side contains the distinction that drives the results. Consumption has two nested margins. At the upper tradable nest, households substitute between the domestic tradable and an aggregate of imported goods with elasticity \(\eta\). Within the import aggregate, households substitute across foreign origins with elasticity \(\rho\).

**[INSERT CURRENT PREFERENCE NESTS.]**

These two elasticities correspond directly to the two forms of adjustment studied below. The elasticity \(\eta\) governs the **home-versus-foreign margin**: following a tariff, how much expenditure moves between domestic and imported tradables? The elasticity \(\rho\) governs the **foreign-supplier reallocation margin**: conditional on importing, how readily does expenditure move from the tariffed exporter toward untreated foreign suppliers?

This distinction is irrelevant in a two-country model because there is only one foreign supplier. It becomes economically active as soon as a third country is introduced.

Special cases such as \(\rho=\eta\), \(\eta=1\), and equal trade weights should be introduced after these roles are clear rather than before the reader knows why the elasticities matter.

## 2.3 Tariffs, Income, Trade Flows, and Closure

A tariff changes consumer prices but tariff revenue is rebated lump-sum. Trade balances are measured at producer prices, so tariff revenue is a domestic transfer rather than an international payment.

**[INSERT CURRENT PRICE-INDEX, EXPENDITURE-SHARE, INCOME, AND BORDER-FLOW EQUATIONS.]**

The model is closed by requiring trade balance in every country. There are no internationally traded assets, so a tariff-induced disturbance to trade flows must ultimately be eliminated through relative-price adjustment. With producer prices fixed in domestic currency, the \(N-1\) independent exchange rates perform this adjustment.

This closure is important for interpreting everything that follows. A tariff first changes trade flows at the existing exchange rates. Exchange rates then move until the resulting trade imbalances disappear.

## 2.4 Exchange-Rate Concepts and Sign Convention

**[INSERT DEFINITIONS OF \(e_{ij}\), TERMS OF TRADE, REAL EXCHANGE RATES, NEER, AND REER.]**

State the sign convention prominently: a rise in \(e_{ij}\) is a depreciation of country \(i\) against country \(j\). Thus a negative response of \(e_{Aj}\) to A's tariff is an appreciation of A against \(j\).

The NEER should be defined here for completeness, but its economic role should not be developed until the three-country bilateral ambiguity has created a reason to care about aggregation.

---

# 3. Two Countries: The Conventional Appreciation Result

## 3.1 Why a Tariff Appreciates the Currency

Begin with countries A and B, with A imposing a small tariff on imports from B. There is only one exchange rate and only one foreign supplier. The distinction between aggregate foreign adjustment and reallocation across foreign countries therefore does not yet exist.

At unchanged exchange rates, the tariff reduces A's imports from B and creates a trade-balance disturbance. Equilibrium requires the exchange rate to move so that trade balance is restored.

**[INSERT THE FULL TWO-COUNTRY DERIVATION.]**

The solution is

\[
\frac{d\log e_{AB}}{d\tau}
=
-\frac{\rho_1^*}{D_2},
\]

where

\[
\rho_1^*
=
1+\alpha_D(\eta-1)-\alpha_T(1-\alpha_D)
=
\alpha_D\eta+(1-\alpha_D)(1-\alpha_T)>0.
\]

The decomposition of \(\rho_1^*\) is economically useful. The first term captures substitution toward the home tradable, while the second captures expenditure absorption associated with the nontradable share. Both imply that the tariff creates an adjustment requiring an appreciation of A, provided the exchange-rate adjustment mechanism has the conventional sign.

The denominator,

\[
D_2=2\alpha_D(\eta-1)+1,
\]

is precisely the Marshall-Lerner margin.

## 3.2 Connection to the Textbook Marshall-Lerner Condition

**[INSERT THE EXISTING REDUCED-FORM EXPORT/IMPORT ELASTICITY DERIVATION.]**

The condition

\[
D_2>0
\]

is exactly equivalent to

\[
\epsilon_X+\epsilon_M>1.
\]

The conventional result therefore contains two separate ingredients. The tariff creates a trade-balance disturbance of an unambiguous sign, and the Marshall-Lerner condition ensures that appreciation is the exchange-rate movement that eliminates it.

With only two countries, both ingredients are scalar and the conclusion is unambiguous:

> **A unilateral import tariff appreciates the tariffing country's currency against its only trading partner.**

The natural question is what happens when "its only trading partner" becomes "one of several trading partners."

## 3.3 Optional Exact Cobb-Douglas Benchmark

**[INSERT THE EXISTING EXACT \(\eta=1\) SOLUTION.]**

This subsection can be retained as a useful exact benchmark, but it should not interrupt the transition to the three-country economics.

---

# 4. Three Countries: Where Multilateralism First Matters

This is the central pedagogical section of the paper.

## 4.1 What Changes When We Add an Untreated Country?

Introduce a third country C, initially symmetric with B, but leave C untariffed. A continues to impose the tariff only on B.

This apparently small change introduces an economic margin that cannot exist in the two-country model. Expenditure that A no longer directs toward B need not return entirely to A's domestic good. It can instead be redirected toward C.

The tariff therefore has two conceptually different effects:

\[
\underbrace{\text{change in A's demand for foreign goods as a whole}}
_{\text{home-versus-foreign adjustment}}
\]

and

\[
\underbrace{\text{change in the allocation of foreign demand between B and C}}
_{\text{foreign-supplier reallocation}}.
\]

The second margin is governed by \(\rho\). It is the source of the new bilateral results.

## 4.2 Impact Effects Before Exchange Rates Move

Before solving for exchange rates, ask what the tariff does to trade balances at the initial rates.

Holding exchange rates fixed, B necessarily loses from A's tariff: its exports to A fall. Hence its impact trade-balance disturbance is negative.

For C, however, there are opposing effects. C gains because some of A's expenditure is diverted away from B toward C. This force becomes stronger as \(\rho\) rises. But C also loses because B's income falls and B reduces its demand for C's goods. Moreover, some of A's expenditure can switch toward A's domestic tradable rather than toward C.

Consequently the impact effect on C is ambiguous. In the symmetric three-country model, it is proportional to

\[
\rho-\rho_1^*.
\]

This is the first indication of the role played by cross-origin substitution: sufficiently strong substitutability among foreign suppliers makes the untreated country a beneficiary of the tariff at unchanged exchange rates.

But a positive impact effect on C is not yet sufficient for A to depreciate against C. Exchange rates jointly restore all countries' trade balances, so C's eventual exchange-rate response also reflects its exposure to B's deterioration.

**[INSERT THE THREE-COUNTRY PRICE-INDEX, INCOME, TRADE-BALANCE, AND LINEAR-SYSTEM DERIVATION.]**

## 4.3 Bilateral Equilibrium Responses

The solution is

\[
\frac{d\log e_{AB}}{d\tau}
=
-\frac{\rho+3\rho_1^*}{3D}<0,
\]

\[
\frac{d\log e_{AC}}{d\tau}
=
\frac{\rho-3\rho_1^*}{3D},
\]

and

\[
\frac{d\log e_{BC}}{d\tau}
=
\frac{2\rho}{3D}>0.
\]

Three results emerge.

First, A always appreciates against the tariff target B. The familiar bilateral result therefore survives for the country directly affected by the tariff.

Second, B always depreciates against the untreated country C. The tariff lowers demand for B relative to C, and equilibrium requires a corresponding deterioration in B's relative price.

Third, and most importantly, A's exchange rate against C is ambiguous:

\[
\frac{d\log e_{AC}}{d\tau}>0
\quad\Longleftrightarrow\quad
\rho>3\rho_1^*.
\]

When cross-origin substitution is sufficiently strong, trade diversion toward C is large enough that C appreciates not only against B but also against A. The country imposing the tariff therefore **appreciates against its target while depreciating against an untreated trading partner**.

This is the precise point at which the literal two-country conventional wisdom fails.

## 4.4 The Meaning of the Bilateral Threshold

The threshold \(3\rho_1^*\) should be interpreted as the point at which foreign-supplier reallocation becomes strong enough to dominate the forces working against C.

The trade-diversion gain rises with \(\rho\). Opposing it are the reduction in B's demand for C, substitution in A toward its own domestic tradable, and the equilibrium interaction across trade balances.

This is not a failure of Marshall-Lerner logic. The ambiguity arises because the tariff creates a mixed pattern of trade-balance disturbances across countries.

That observation motivates a more general way to organize the comparative statics, which we introduce only after the three-country mechanism is visible.

---

# 5. Disturbance and Adjustment: The General Multilateral Framework

The three-country case suggests a general decomposition. A tariff first creates a vector of trade-balance disturbances at unchanged exchange rates. Exchange rates then move to eliminate those disturbances.

Linearizing trade balance around a balanced free-trade equilibrium gives

\[
J\,d\nu+G\,d\tau=0.
\]

For a particular tariff experiment \(d\tau=a\,d\tau\), define

\[
F\equiv Ga.
\]

The equilibrium response is

\[
\frac{d\nu}{d\tau}=(-J)^{-1}F.
\]

The two objects have distinct economic meanings.

The vector \(F\) is the **impact disturbance**: how the tariff changes each country's trade balance when exchange rates are held fixed.

The matrix \(J\) is the **adjustment mechanism**: how trade balances respond when exchange rates move.

Thus the comparative static can be read as

\[
\text{tariff}
\longrightarrow
\text{trade-balance disturbances }F
\longrightarrow
\text{exchange-rate adjustment }(-J)^{-1}F.
\]

## 5.1 General Linearization

**[INSERT THE CURRENT GENERAL PRICE, SHARE, INCOME, FLOW, AND TRADE-BALANCE DIFFERENTIALS AND THE \(Jd\nu+Gd\tau=0\) SYSTEM.]**

## 5.2 The Multilateral Marshall-Lerner Condition

For the familiar comparative statics to operate normally, exchange-rate depreciation must improve the trade balance of the depreciating country. In a two-country model this is the scalar Marshall-Lerner condition. With several exchange rates, the corresponding condition applies to the whole adjustment system.

Under the multilateral Marshall-Lerner condition, \(-J\) is a nonsingular M-matrix and

\[
(-J)^{-1}\geq0.
\]

**[INSERT THE FORMAL RESULT.]**

The important economic implication is the sign rule:

\[
\frac{d\nu}{d\tau}=(-J)^{-1}F.
\]

Each exchange-rate response is a nonnegative weighted combination of the initial trade-balance disturbances.

This clarifies the source of bilateral ambiguity. It does not come from a perverse adjustment matrix. It comes from the direction of \(F\). A discriminatory tariff always worsens the target's trade balance, but a bystander's impact effect can be positive or negative depending on whether trade diversion dominates the loss of demand associated with the target's deterioration.

The three-country threshold is therefore an explicit example of a general sign rule.

## 5.3 Technical Matrix Properties

**[INSERT OR RELOCATE THE EXISTING HOMOGENEITY, WALRAS' LAW, GROSS SUBSTITUTABILITY, DIAGONAL DOMINANCE, IRREDUCIBILITY, M-MATRIX, AND TATONNEMENT-STABILITY ARGUMENTS.]**

These details should remain in the document for rigor, but can be marked as a technical subsection or moved to an appendix if they interrupt the economic narrative.

---

# 6. Aggregation: Why the Conventional Result Survives in the NEER

The three-country bilateral results create a natural question. If A appreciates against B but can depreciate against C, what happens to the overall value of A's currency?

With symmetric trade weights, A's nominal effective exchange-rate response is the average of its bilateral responses.

**[INSERT THE THREE-COUNTRY AGGREGATE/RELATIVE DECOMPOSITION.]**

The solution can be written as

\[
\frac{\nu_B+\nu_C}{2}
=
-\frac{\rho_1^*}{D}d\tau,
\]

and

\[
\nu_B-\nu_C
=
-\frac{2\rho}{3D}d\tau.
\]

These expressions reveal the structure of the result.

The first is the **aggregate component**. It determines the average value of A's currency against the rest of the world.

The second is the **relative component**. It determines how that adjustment is distributed between B and C.

Cross-origin substitution \(\rho\) directly drives the relative component. As B and C become closer substitutes, the tariff produces progressively more appreciation of C relative to B. Eventually this reallocation can reverse A's bilateral rate against C.

But the same \(\rho\)-terms enter the bilateral responses with opposite signs and cancel when they are aggregated. Therefore

\[
\boxed{
\frac{d\nu_A^E}{d\tau}
=
-\frac{\rho_1^*}{D}<0.
}
\]

A unilateral tariff always appreciates A's nominal effective exchange rate.

This gives a different interpretation of the familiar two-country result. In a two-country world, there is no distinction between a bilateral exchange rate and an effective exchange rate. The conventional appreciation result therefore appears bilateral. Once additional trading partners are introduced, the bilateral and aggregate concepts separate. The bilateral result can fail because foreign-supplier reallocation affects different partners differently, while the aggregate result survives because that reallocation cancels across partners.

> **The two-country appreciation result is therefore best understood as an aggregate home-versus-foreign result, rather than a prediction that the tariffing country must appreciate against every foreign currency.**

This is one of the central conceptual results of the paper.

---

# 7. General \(N\): Dilution and Aggregation

The three-country model contains the essential economics. Generalizing to \(N\) countries allows us to ask how the same mechanisms change as the number of potential alternative suppliers grows.

Suppose A tariffs B and the remaining \(N-2\) countries are symmetric bystanders. Because all bystanders have the same response, the system again reduces to the exchange rate against B and a representative bystander.

Before deriving the result, the economics suggests a prediction. The tariff still diverts expenditure away from B, but that diversion is now divided among \(N-2\) alternative foreign suppliers. Any individual bystander should therefore receive less of the diversion gain as \(N\) rises. Bilateral reversal should become progressively harder even though the aggregate foreign reallocation need not disappear.

## 7.1 Reduced \(N\)-Country System

**[INSERT THE EXISTING GENERAL SYMMETRIC \(N\)-COUNTRY REDUCED SYSTEM AND ITS INVERSION.]**

The bilateral responses are

\[
\frac{d\log e_{AB}}{d\tau}
=
-\frac{N\rho_1^*+(N-2)\rho}{ND_N}<0,
\]

\[
\frac{d\log e_{AC}}{d\tau}
=
\frac{\rho-N\rho_1^*}{ND_N},
\]

and

\[
\frac{d\log e_{BC}}{d\tau}
=
\frac{(N-1)\rho}{ND_N}>0.
\]

## 7.2 The Bilateral Threshold as Dilution

A depreciates against an untreated bystander iff

\[
\boxed{\rho>N\rho_1^*.}
\]

The threshold rises linearly with \(N\). The reason is dilution. With one bystander, expenditure diverted away from B has only one alternative foreign destination. With \(N-2\) bystanders, the same foreign reallocation is spread across many suppliers. Each individual bystander therefore receives a smaller diversion gain, and stronger cross-origin substitutability is required to generate enough appreciation to reverse its bilateral rate against A.

This is a statement about how adjustment is distributed across foreign partners, not about the aggregate value of A's currency.

## 7.3 Effective Exchange-Rate Aggregation

Averaging A's bilateral exchange rates gives

\[
\boxed{
\frac{d\nu_A^E}{d\tau}
=
-\frac{\rho_1^*}{D_N}<0.
}
\]

The cancellation observed with three countries is therefore not accidental. It holds for every \(N\geq2\).

The companion relative component is

\[
\nu_B-\nu_C
=
-\frac{(N-1)\rho}{ND_N}d\tau.
\]

The general \(N\)-country model therefore sharpens the decomposition:

\[
\text{home-versus-foreign adjustment}
\quad\longrightarrow\quad
\text{effective exchange rate},
\]

whereas

\[
\text{reallocation across foreign suppliers}
\quad\longrightarrow\quad
\text{dispersion in bilateral exchange rates}.
\]

Cross-origin substitution affects the magnitude of the aggregate response through equilibrium adjustment, but under symmetry it cannot change its sign. Its qualitatively new role is to redistribute the adjustment across foreign partners.

This is the precise sense in which the conventional appreciation result survives multilateralization.

## 7.4 Single-Elasticity Restriction and Impossibility Result

**[INSERT THE EXISTING \(\rho=\eta=\sigma\) RESULT.]**

Interpret this result as a restriction on the model's ability to generate strong foreign-supplier reallocation. When a single elasticity simultaneously governs home-versus-foreign and foreign-versus-foreign substitution, the cross-origin margin cannot become independently strong enough to produce the bilateral reversal over a broad class of home-biased calibrations.

## 7.5 Correspondence Across \(N\)

Retain the existing summary table, updated to match the new section numbering. Use it as a compact map of which objects change with dimensionality and which do not.

---

# 8. What Depends on the Tariff Configuration?

The preceding results concern a discriminatory unilateral tariff. Different tariff configurations activate the two margins differently.

## 8.1 Broad Unilateral Protection

Suppose A raises tariffs uniformly against every foreign supplier. There is then no tariff-induced reallocation across foreign countries because all origins are treated identically. The cross-origin substitution margin is therefore inactive.

**[INSERT THE EXISTING BROAD-TARIFF SUPERPOSITION RESULT.]**

Every bilateral exchange rate appreciates by the same amount, and the bilateral and effective responses coincide.

The comparison with the discriminatory tariff is instructive. Bilateral ambiguity is not generated by protection per se. It is generated by **discrimination across foreign suppliers**.

## 8.2 Reciprocal Trade War

Now suppose B retaliates with an equal tariff on A.

**[INSERT THE EXISTING SYMMETRIC-WAR RESULT.]**

By symmetry, the A-B exchange rate does not move. Adjustment instead occurs against the untreated countries. The effective exchange rate of each belligerent depreciates when

\[
\rho>\rho_1^*.
\]

Thus the unconditional NEER appreciation result is a property of a unilateral tariff, not of tariffs generically. Retaliation cancels the direct bilateral component between A and B, leaving the foreign-supplier reallocation margin to determine the belligerents' exchange rates against the rest of the world.

This also explains why the war threshold is much lower than the unilateral bilateral-reversal threshold. The latter requires diversion to become strong enough to overcome the direct appreciation against B. In a symmetric war that bilateral component is removed by symmetry.

---

# 9. Real Exchange Rates

The nominal results provide the cleanest statement of the underlying mechanism. Real exchange rates add a direct consumer-price effect because the tariff raises the tariffing country's price index even before the nominal exchange rate moves.

## 9.1 Bilateral Real Rates

**[INSERT AND CONSOLIDATE THE EXISTING \(N=2\), \(N=3\), AND GENERAL-\(N\) BILATERAL REAL-EXCHANGE-RATE EXPRESSIONS.]**

Explain that the bilateral real-rate threshold can lie above the nominal bilateral threshold because the direct tariff-induced increase in A's consumer prices works toward real appreciation.

## 9.2 Effective Real Rates

**[INSERT THE EXISTING REER RESULTS.]**

The effective real appreciation is even more robust than the nominal effective appreciation because the tariff directly raises A's consumer price level in addition to the nominal exchange-rate adjustment.

---

# 10. Asymmetry: How Much of the Aggregation Result Survives?

The exact cancellation underlying the symmetric NEER result relies on a correspondence between bilateral responses and the weights with which those responses enter the effective exchange rate. Actual trade networks are asymmetric, so the natural question is whether symmetry is essential to the economics or only to the exact closed form.

At a general balanced baseline, the disturbance-adjustment decomposition remains unchanged:

\[
d\nu=(-J)^{-1}F\,d\tau.
\]

Asymmetry therefore does not introduce a new economic channel. It changes the weights placed on the same channels.

## 10.1 General Asymmetric Baseline

**[INSERT THE EXISTING GENERAL \(N=3\) ASYMMETRIC NUMERATOR-QUADRATIC RESULT.]**

The bilateral response against the bystander depends on the full trade network. A country well positioned to replace B in A's import basket receives more of the diversion effect. A country heavily exposed to the fall in B's income receives more of the offset. Sufficiently strong cross-origin substitution nevertheless generates the reversal whenever the relevant bilateral trade links are present.

## 10.2 Scaling Exposure with \(\kappa\)

To compare asymmetry across different \(N\), it is not useful to hold B's absolute import share fixed, because the symmetric bilateral share itself shrinks like \(1/(N-1)\). Instead, let B's bilateral weight be \(\kappa\) times the symmetric bilateral share.

Thus \(\kappa=1\) is symmetry, \(\kappa>1\) makes B disproportionately important, and \(\kappa<1\) makes B disproportionately small.

**[INSERT THE EXISTING \(\kappa\) PARAMETERIZATION AND CLOSED-FORM SYSTEM.]**

This scaling preserves the economic meaning of the asymmetry as \(N\) changes.

## 10.3 Large-\(N\) Behavior

The asymptotic result is

\[
N\frac{d\nu_A^E}{d\tau}
\longrightarrow
-\kappa
\frac{\rho_1^*}
{\rho+\alpha_D(\eta-1)}.
\]

To leading order, asymmetry simply scales the symmetric effective appreciation by the relative importance of the tariff target.

This shows that the symmetric result is not economically knife-edge even though its exact finite-\(N\) cancellation is.

## 10.4 When Can the NEER Sign Reverse?

At finite \(N\), reversals are possible when the target is disproportionately small. The intuition follows directly from the aggregation argument. A appreciates against B, but B receives little weight in A's NEER. If A simultaneously depreciates against many bystanders, those movements can dominate the effective rate.

The reversal nevertheless requires \(\rho\) of order \(N\). Thus the same dilution that makes individual bilateral reversals harder as \(N\) grows also makes aggregate reversal under asymmetry difficult.

The symmetry result should therefore be interpreted as exact under symmetry and approximately robust more broadly, rather than as a knife-edge curiosity.

---

# 11. Why the Canonical PTA Model Is Sharper

The multilateral model predicts that an untreated exporter benefits from a discriminatory tariff only when cross-origin substitution is sufficiently strong. This may initially appear to conflict with the canonical theory of preferential trade agreements, in which discrimination against one exporter unambiguously improves the terms of trade of its competitor.

The difference is not a competing mechanism. It is a difference in the set of margins permitted by the two environments.

## 11.1 Competing Exporters

**[INSERT THE EXISTING CANONICAL PTA SETUP, MARKET CLEARING, AND COMPARATIVE STATICS.]**

A discriminatory tariff on B lowers B's exporter price and raises C's exporter price. The Viner-Mundell sign is therefore unconditional in this environment.

## 11.2 Which Margins Are Missing?

The canonical environment isolates foreign-supplier reallocation. The richer model embeds the same mechanism but allows several forces to oppose it.

Use the existing threshold decomposition prominently:

\[
\rho_3^*
=
\underbrace{3}_{\text{B-C linkage}}
+
\underbrace{3\alpha_D(\eta-1)}_{\text{home switching}}
-
\underbrace{3\alpha_T(1-\alpha_D)}_{\text{openness credit}}.
\]

First, B and C are full trading partners in the richer model. When A tariffs B, the reduction in B's income lowers B's demand for C, while relative-price adjustment can induce C to substitute toward B's cheaper goods. This B-C linkage works against the simple diversion effect.

Second, consumers in A can switch toward A's domestic tradable rather than toward C. This home-switching channel strengthens with \(\eta\) and with the domestic tradable share.

Third, greater openness works in the opposite direction. A larger import share gives the tariff more foreign expenditure to reallocate, lowering the substitution strength needed for C to benefit.

**[INSERT THE EXISTING RESTRICTION TABLE AND NUMERICAL DECOMPOSITION.]**

The canonical model obtains an unconditional sign because it removes the margins that generate the threshold. B and C are competing exporters rather than full trading partners, eliminating the B-C demand linkage. A does not produce the imported good, eliminating substitution toward a domestic variety. Quasilinearity suppresses the relevant income effects. What remains is precisely the diversion of expenditure between foreign suppliers.

The richer model therefore does not overturn Viner-Mundell. It identifies the condition under which the Viner-Mundell mechanism dominates once the opposing margins are restored.

## 11.3 Relation to Analytical and Quantitative Trade Models

Retain the existing literature mapping, but organize it around which margins each model keeps or removes.

The analytical PTA literature often obtains sharp sign results by restricting the environment enough to isolate the reallocation channel. Quantitative trade models retain the full trade matrix, home-versus-import substitution, nontradables, and income effects, and therefore generate both signs numerically.

The contribution of the present framework is to make the condition separating those outcomes explicit.

---

# 12. Conclusion: Bilateral Reallocation Versus Aggregate Adjustment

The familiar statement that an import tariff appreciates the tariffing country's currency is exact in a two-country world because there is only one foreign currency against which appreciation can occur. Once trade is multilateral, that statement combines two distinct economic adjustments.

The first is aggregate substitution between home and foreign goods. The second is reallocation across foreign suppliers. A discriminatory tariff activates both. The aggregate margin pushes toward appreciation of the tariffing country, while the foreign-supplier margin redistributes that adjustment across trading partners and can cause individual bilateral exchange rates to move in the opposite direction.

The three-country model makes this distinction visible. A always appreciates against the tariff target, but can depreciate against an untreated country when cross-origin substitution is sufficiently strong. Generalizing to \(N\) countries strengthens the bilateral threshold because trade diversion is diluted across additional bystanders.

Aggregation produces a different result. Under symmetry, foreign-supplier reallocation cancels from the numerator of the nominal effective exchange-rate response. A unilateral tariff therefore appreciates the tariffing country's NEER for every \(N\) and every cross-origin elasticity consistent with the multilateral Marshall-Lerner condition. The conventional two-country result thus survives multilateralization, but as an effective rather than universally bilateral statement.

The distinction also organizes the extensions. Broad protection treats foreign suppliers symmetrically and shuts down the reallocation margin. Reciprocal retaliation cancels the direct bilateral adjustment between the belligerents and can instead make foreign reallocation decisive for their effective exchange rates. Asymmetry breaks the exact aggregation result but largely preserves its economics, while the canonical Viner-Mundell model emerges as an environment in which the forces opposing foreign-supplier diversion have been removed.

The common principle is therefore simple:

\[
\boxed{
\text{tariffs change both how much a country buys from abroad and from whom it buys it.}
}
\]

The first margin governs the aggregate value of the currency. The second governs the distribution of that adjustment across bilateral exchange rates. Distinguishing the two clarifies both what survives from the two-country model and what genuinely changes in a multilateral world.

---

# Suggested Final Section Structure

1. Introduction: What Survives from the Two-Country Model?
2. Economic Environment: Two Margins of Substitution
   - 2.1 Production and Prices
   - 2.2 Preferences: Home Versus Foreign and Foreign Versus Foreign
   - 2.3 Tariffs, Income, Trade Flows, and Closure
   - 2.4 Exchange-Rate Concepts and Sign Convention
3. Two Countries: The Conventional Appreciation Result
   - 3.1 Why a Tariff Appreciates the Currency
   - 3.2 Connection to the Textbook Marshall-Lerner Condition
   - 3.3 Optional Exact Cobb-Douglas Benchmark
4. Three Countries: Where Multilateralism First Matters
   - 4.1 What Changes When We Add an Untreated Country?
   - 4.2 Impact Effects Before Exchange Rates Move
   - 4.3 Bilateral Equilibrium Responses
   - 4.4 The Meaning of the Bilateral Threshold
5. Disturbance and Adjustment: The General Multilateral Framework
   - 5.1 General Linearization
   - 5.2 The Multilateral Marshall-Lerner Condition
   - 5.3 Technical Matrix Properties
6. Aggregation: Why the Conventional Result Survives in the NEER
7. General N: Dilution and Aggregation
   - 7.1 Reduced N-Country System
   - 7.2 The Bilateral Threshold as Dilution
   - 7.3 Effective Exchange-Rate Aggregation
   - 7.4 Single-Elasticity Restriction and Impossibility Result
   - 7.5 Correspondence Across N
8. What Depends on the Tariff Configuration?
   - 8.1 Broad Unilateral Protection
   - 8.2 Reciprocal Trade War
9. Real Exchange Rates
   - 9.1 Bilateral Real Rates
   - 9.2 Effective Real Rates
10. Asymmetry: How Much of the Aggregation Result Survives?
   - 10.1 General Asymmetric Baseline
   - 10.2 Scaling Exposure with Kappa
   - 10.3 Large-N Behavior
   - 10.4 When Can the NEER Sign Reverse?
11. Why the Canonical PTA Model Is Sharper
   - 11.1 Competing Exporters
   - 11.2 Which Margins Are Missing?
   - 11.3 Relation to Analytical and Quantitative Trade Models
12. Conclusion: Bilateral Reallocation Versus Aggregate Adjustment
