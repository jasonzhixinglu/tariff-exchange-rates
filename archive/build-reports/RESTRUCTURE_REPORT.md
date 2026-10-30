# Paper restructure report (2026-10-29)

Branch `paper-restructure`, created from `repo-reorg`. The paper now follows the structure of `archive/writeups/notes/model_derivations.tex`:
- everything that holds in the general model comes first, including the symmetric-partner decomposition in terms of the four eigenvalues;
- nested CES comes afterwards, to attach parameters (ρ_D, ρ, M_N) to those eigenvalues.

No result, number, figure content or proof changed.

## Housekeeping
- **Old package uninstalled:** `pip uninstall -y tariff-exchange-rates` removed version 0.1.0 (the archived `src/` package).
- **Current package installed:** `pip install -e ".[test]"` installed 0.2.0 from the current `pyproject.toml`. `import tariff_exchange_rates` now fails (ModuleNotFoundError).
- **No dependency on the old package:** with it gone, the 345 tests and `python code/run_all.py` both pass.
- **Docstring fixed:** `code/checks/us_china_row.py` now says it backs the US–China–ROW footnote in the 2025 section (the Phase 2 bullet "China's size does not"). The "not a claim in the paper" wording is gone.
- **Left alone:** `notes/local_elasticity_representation.md`.

## Section map

| Old (v3) | New |
|---|---|
| 1 Introduction | 1 Introduction (Results paragraphs and roadmap reordered) |
| 2.1–2.3 Framework | 2.1–2.3 unchanged |
| 3 The Symmetric Case | removed as a section; its parts are distributed below |
| 3.1 Average protection and relative treatment | **2.4 Symmetric partners** |
| 3.2 A nested-CES economy (environment) | **3 The Nested-CES Model**, 3.1 Production, preferences and equilibrium |
| 3.2 "The two-country case" paragraph, eq. (3.7) | 3.2 The two-country case (eq. 3.4) |
| 3.3 The main theorem | 3.3 The N-country case |
| 3.4 A unilateral tariff (+ Fig. 2 moved here from 3.1) | 3.4 A unilateral tariff |
| 3.6 The three-country representation | 3.5 The three-country representation |
| 3.7 Real exchange rates | 3.6 Real exchange rates |
| 3.5 Retaliation and trade wars | **4 Trade Wars and Preferential Tariffs**, 4.1 Trade wars |
| 3.8 Relation to the competing-exporter model | 4.2 Preferential tariffs and competing exporters |
| 4 Asymmetry (4.1–4.5) | 5 Asymmetry (5.1–5.5), unchanged |
| 5 Conclusion | 6 Conclusion |
| Appendices A–D | unchanged letters and numbering |

**Section files.**
- `sections/symmetric.tex` is removed.
- New files: `sections/nested_ces.tex` (§3) and `sections/tradewars.tex` (§4).
- `sections/framework.tex` gains §2.4.
- `main.tex` inputs the files in the new order.

## Result, figure and table numbers (from `main.aux`, v3 vs new; ← marks a change)

| Label | Old | New |
|---|---|---|
| `sec:intro` | 1 | 1 |
| `fig:bilateral` | 1 | 1 |
| `tab:composite` | 1 | 1 |
| `sec:literature` | 1.1 | 1.1 |
| `sec:framework` | 2 | 2 |
| `fig:geometry` | 2 | 2 |
| `tab:q2` | 2 | 2 |
| `ass:gs` | 2.1 | 2.1 |
| `rem:robustness` | 2.1 | 2.1 |
| `sec:bilateral` | 2.1 | 2.1 |
| `def:mml` | 2.2 | 2.2 |
| `sec:representation` | 2.2 | 2.2 |
| `sec:mml` | 2.3 | 2.3 |
| `lem:gs` | 2.3 | 2.3 |
| `prop:decomposition` | 3.1 | 2.4 ← |
| `sec:decomposition` | 3.1 | 2.4 ← |
| `fig:geometry-a` | 2a | 2a |
| `fig:geometry-b` | 2b | 2b |
| `fig:unilateral` | 3 | 3 |
| `sec:nestedces` | — | 3 ← |
| `tab:neer` | 3 | 3 |
| `sec:symmetric` | 3 | — ← |
| `sec:model` | 3.2 | 3.1 ← |
| `thm:main` | 3.2 | 3.1 ← |
| `sec:twocountry` | — | 3.2 ← |
| `prop:unilateral` | 3.3 | 3.2 ← |
| `cor:single` | 3.4 | 3.3 ← |
| `sec:theorem` | 3.3 | 3.3 |
| `sec:unilateral` | 3.4 | 3.4 |
| `prop:composite` | 3.6 | 3.4 ← |
| `prop:real` | 3.7 | 3.5 ← |
| `sec:composite` | 3.6 | 3.5 ← |
| `sec:real` | 3.7 | 3.6 ← |
| `sec:tradewars` | — | 4 ← |
| `tab:phases` | 4 | 4 |
| `fig:composite` | 5 | 4 ← |
| `sec:retaliation` | 3.5 | 4.1 ← |
| `prop:retaliation` | 3.5 | 4.1 ← |
| `sec:pta` | 3.8 | 4.2 ← |
| `tab:tau0` | 5 | 5 |
| `sec:asymmetry` | 4 | 5 ← |
| `fig:configurations` | 4 | 5 ← |
| `lem:welfare` | 4.1 | 5.1 ← |
| `sec:welfare` | 4.1 | 5.1 ← |
| `prop:uniform` | 4.2 | 5.2 ← |
| `sec:totcondition` | 4.2 | 5.2 ← |
| `sec:threecountry` | 4.3 | 5.3 ← |
| `def:tot` | 4.3 | 5.3 ← |
| `sec:heterogeneous` | 4.4 | 5.4 ← |
| `prop:threecases` | 4.4 | 5.4 ← |
| `sec:2025` | 4.5 | 5.5 ← |
| `tab:sens` | 6 | 6 |
| `fig:tot` | 6 | 6 |
| `sec:conclusion` | 5 | 6 ← |
| `fig:episode` | 7 | 7 |
| `app:linear` | A | A |
| `lem:jacobian` | A.1 | A.1 |
| `app:proofs` | B | B |
| `app:departures` | C | C |
| `app:asym-tariff` | C.1 | C.1 |
| `app:asym-finite` | C.2 | C.2 |
| `app:asym-primitives` | C.3 | C.3 |
| `app:asym-neer` | C.4 | C.4 |
| `app:online` | D | D |
| `lem:tariffmono` | D.1 | D.1 |
| `app:online-twocountry` | D.1 | D.1 |
| `lem:ermono` | D.2 | D.2 |
| `app:online-rv` | D.2 | D.2 |
| `prop:twosign` | D.3 | D.3 |
| `app:online-imbalance` | D.3 | D.3 |

Equation numbers in §§2–5 change with their sections. The new equation (3.6) lists the eigenvalues. Appendix equations are unchanged, for example (A.4) = `eq:geigen`.

**Figures.** The figure files keep their names, but Figures 4 and 5 swap numbers:
- `fig5*_composite` is now Figure 4 (§3.5);
- `fig4_configurations` is now Figure 5 (§4.1).

**Appendix B.** The proof of the retaliation proposition (now 4.1) moved from after Corollary 3.3 to after Proposition 3.5, so the proofs follow the new numbering. Appendix A has no subsection pointers into the main text. All of its references are `\cref` to labels, which resolve.

## New or changed sentences

**Transitions** (new):
1. §2.4 opening: "The representation (2.3) holds at any balanced baseline. When the tariffing country's partners are symmetric, it can be solved in closed form in terms of four eigenvalues."
2. §2.4 closing: "Section 3 gives these eigenvalues economic content."
3. §3 opening: "We now specify an economy in which these eigenvalues, and hence every response in Section 2.4, can be computed from primitives."
4. §3.3 link: "We now evaluate the eigenvalues of Section 2.4 in this model."
5. §4 opening: "So far only A has changed its tariffs. This section lets partners respond, and then relates the bystander result to the literature on preferential tariffs."

**Theorem 3.1** (opening rewritten as requested): after the definition of M_N it now reads "The eigenvalues of Proposition 2.4 are (Lemma A.1 and Eq. (A.4)) g_S = −mρ_D/(N−1), g_D = −mρ/(N−1), j_S = mM_N/(N−1), j_D = N j_S." This is the new display (3.6). The rest of the statement is unchanged.

**§3.5, forward reference to §4:** "The shocks it covers include the retaliation and trade-war experiments of Section 4." This is appended to "The reduction is first-order …".
- The old §3.6 never used the word retaliation.
- Its shock class ("between A and B", and "by all bystanders on A or B") is where the retaliation experiments sit, so the forward reference goes after the statement that the reduction is first-order.

**Introduction:**
- "We proceed in three steps." → "We proceed in four steps."
- The paragraph "*The symmetric case (Section 3).*" is split into two:
  - "*Symmetric partners (Section 2.4).*", with the first four sentences unchanged;
  - "*The nested-CES model (Section 3).*", which keeps the rest unchanged.
- The two retaliation sentences ("Bilateral retaliation lowers … no financial channel.") moved verbatim into a new paragraph, "*Trade wars (Section 4).*", placed after the three-country paragraph.
- "Finally, we show that the symmetric …" → "We then show that the symmetric …".
- Roadmap: "Section 2 develops the general framework and its symmetric-partner decomposition. Section 3 gives the decomposition economic content in a nested-CES model and derives the three-country representation, Section 4 turns to trade wars and preferential tariffs, and Section 5 to asymmetry and the 2025 episode. Section 6 concludes." The appendix sentence is unchanged.

**Conclusion:** the sentence "An exact three-country representation shows …" moved before "Under bilateral retaliation …", following the new order. No words changed.

**Re-targeted pointers.** These are reference changes only; the old `sec:symmetric` label no longer exists.
- Appendix C opening: "The results of Section 3" → "The results of Sections 2.4, 3 and 4".
- §5.1: "the average-protection disturbance of Section 3" → "of Section 3.3" (the theorem, where g_S is evaluated).

**Headings:**
- §2.4, §3, §3.1, §3.2 and §3.3 have new titles.
- §3.2 was previously a run-in paragraph head, "The two-country case.".
- §4 is new, and §4.1 and §4.2 are retitled.

## Forward references

These were checked in source order. Apart from the cases below, every forward reference also existed in v3: pointers to appendices, the introduction's section pointers, and figures and tables cited just before their float.

| From | To | Why |
|---|---|---|
| §2.4 ("… each component is scaled by its own coefficient (Figure 2)") | Figure 2, now in §3.4 | requested: the figure is computed at nested-CES parameters |
| §2.4 closing sentence | Section 3 | requested transition |
| Theorem 3.1 | Lemma A.1, eq. (A.4) | requested; appendix |
| §3.5 | Section 4 | requested forward reference to retaliation |
| Introduction | Sections 2.4, 3, 4 | roadmap and Results paragraphs |

No proposition, theorem, lemma or corollary is cited before its definition except Lemma A.1 (appendix) as above. Each figure file is included exactly once, and no label is defined twice.

## Content check (v3 PDF at `pre-reorg-2026-10-29` vs new PDF)

**Method.**
- Text blocks of both PDFs were extracted with PyMuPDF; page-number blocks were dropped.
- Hyphens and whitespace were removed on both sides.
- Only cross-reference numbers were masked: "Section/Proposition/Figure/Table/… N", "(N.M)" equation tags, and leading heading numbers. Data numbers stay compared.
- Each v3 block must occur in the new text. Blocks not found whole were checked sentence by sentence.
- A sentence counts as found across a break if it occurs in two pieces, because a page break or float now falls inside it.

**Result.**
- **1,164 v3 blocks.** Every sentence of every v3 paragraph appears in the new PDF, verbatim or differing only in reference numbers, except the 12 below.
- **All 12 are intended**, and all are listed above:
  - "We proceed in three steps.";
  - the header "The symmetric case (Section 3).";
  - "Finally, we show that the symmetric …";
  - the three roadmap sentences;
  - six old section headings (3, 3.1, 3.2, 3.3, 3.5, 3.8).
- **Two sentences found only across a page break:**
  - "In this family q0 < 0 throughout and the two-root case never appears." (v3 p. 24);
  - "US tariffs of 25 percent on Canada and Mexico took effect on March 4, …" (v3 p. 27).
- **Reverse direction:** the 26 sentences or fragments that are new in the restructured PDF are exactly the transitions, headings, intro and roadmap sentences, the Theorem 3.1 eigenvalue line and the §3.5 forward reference listed above.

**What the check caught.** The first build failed it. When `symmetric.tex` was split, the competing-exporter paragraph had been cut after its first line, losing its display equation and the rest of the paragraph. The check flagged the missing sentences, and the paragraph was restored from git before anything was committed.

**A procedural error, also fixed before anything was committed.** While building the v3 comparison tree, a `git checkout -- paper` discarded the uncommitted edits to tracked files. All edits were reapplied by an asserted script and committed. Every check above was then rerun, with identical results.

## Build and tests
- `python code/run_all.py` exits 0, with 345 tests passed.
- `paper/main.pdf` has 55 pages, as before, and no undefined references.
- Overfull boxes are the same two as in v3, 2.80pt and 1.47pt.
- The bookmark warning from `$N$` in a heading is fixed with `\texorpdfstring`.
- Figures changed only in `/CreationDate` and were not recommitted.

The README cites no section numbers and needed no change.
