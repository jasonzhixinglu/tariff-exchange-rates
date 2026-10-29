# Understanding Multilateral Tariffs and Exchange Rates

Replication code for *Understanding Multilateral Tariffs and Exchange Rates* (Jason Lu and Dimitre Milkov, IMF Research Department, 2026). The paper is in [`paper/main.pdf`](paper/main.pdf), with LaTeX sources in `paper/`. Everything in it is rebuilt by `python code/run_all.py`, which runs the tests, numerical checks, tables, figures and LaTeX build.

**Live dashboard:** https://jasonzhixinglu.github.io/tariff-exchange-rates/ (built from the earlier three-country draft; see below).

## Results

The paper studies the long-run exchange-rate response to arbitrary tariff vectors in an N-country trade model.

1. **Disturbance–adjustment representation.** To first order, dν = (−J)⁻¹F: the tariff's trade-balance disturbance at unchanged exchange rates, F, times the inverse of the exchange-rate adjustment matrix. A *multilateral Marshall–Lerner* (MML) condition (−J a nonsingular M-matrix) makes adjustment well behaved but does not fix the sign of any bilateral response.
2. **Average protection and relative treatment.** Under partner symmetry, any tariff vector splits into average protection, which alone moves the trade-weighted NEER, and relative treatment, which alone moves bilateral rates around it.
3. **Thresholds (nested CES).** With a home–import elasticity η, a cross-origin elasticity ρ and the domestic diversion margin ρ_D = α_D η + (1−α_D)(1−α_T):
   - a unilateral tariff always appreciates the tariffing country's NEER and its currency against the target, and depreciates it against every untariffed bystander iff **ρ > Nρ_D** (3ρ_D = 3.96 at US-like parameters with N = 3);
   - under bilateral retaliation the belligerents' bilateral rate is unchanged and the bystander threshold falls to **ρ > ρ_D**, so both belligerents depreciate against bystanders and in effective terms;
   - with realistic home bias the reversal requires ρ > η, so it cannot arise when a single elasticity governs both margins.
4. **Composite bystander.** The symmetric N-country economy reduces exactly to a three-country economy with a composite bystander.
5. **Asymmetry and welfare.** A uniform tariff appreciates the currency against every partner and raises welfare at any balanced baseline under MML. A tariff on a single small, low-weight partner can instead worsen the aggregate terms of trade, and hence welfare, when ρ is high.
6. **2025.** A stylized reading of the 2025 episode (no calibration): the retaliation phase is consistent with the trade channel; the dollar's effective weakness under unilateral and near-uniform tariffs is not explained by it.

## Code for the paper

```
code/model/      nested_ces (exact N-country model), linear (Appendix A),
                 closed_forms (symmetric benchmark), asymmetry, extensions
                 (Ricardo–Viner tradables, transfer-financed imbalances)
code/tests/      pytest suite (linearization vs finite differences, closed forms,
                 composite bystander, welfare lemma, uniform tariffs, extensions)
code/checks/     scripts that recompute every number in the paper (code/results/*.json)
code/figures/    one script per figure;  code/tables/  generated table rows
code/data/       fetch_fx_2025.py (FRED, BIS, Fed H.10 weights; cached in data/raw/)
paper/           main.tex, sections/, refs.bib, figures/, tables/, main.pdf
```

## Legacy code (earlier three-country draft)

The package, notebooks, scripts and dashboard below belong to an earlier draft that used a flat single-elasticity CES and calibrated a three-country model to the 2025 episode. They are kept for reference and are not used by the current paper.

### Repository structure

```
src/tariff_exchange_rates/          Core Python package
    economy.py                      Flat-CES allocation and price-index functions
    nested.py                       Nested (eta, rho) model, solver, rho* threshold utilities
    equilibrium.py                  Solvers: solve_2country, solve_3country
    tariffs.py                      Tariff matrix constructors
    parameters.py                   Calibrated configurations (CALIBRATIONS, TARIFF_REGIMES)
    plotting.py                     Figure helpers

tests/                              Regression tests (pytest): model fixes, referee
                                    replication values, analytic threshold checks

notebooks/
    section2_two_country_model.ipynb      Two-country benchmark and robustness
    section3_three_country_model.ipynb    Three-country results and paper figures
    section4_calibration.ipynb            Calibration and model-data comparison

scripts/
    precompute_theory_grid.py       Generate data/theory_grid.json (4^6 × 3 grid)
    precompute_calibration_panel.py Generate data/calibration_panel.json (8 configs)
    fetch_fx_data.py                Fetch observed FX data from Yahoo Finance
    regenerate_calibration_figure.py Regenerate output/calibration_results.pdf
    verify_referee_claims.py        Reproduce every quantitative claim in the Aug 2026
                                    referee report (--symbolic re-derives rho* via sympy)
    derive_general_threshold.py     General-size threshold via share-based linearization

data/
    theory_grid.json                Precomputed equilibria for dashboard theory panel
    calibration_panel.json          Precomputed equilibria for dashboard calibration panel
    fx_data.json                    Observed bilateral FX rates (2024 avg, Mar/Apr 2025)

dashboard/                          Interactive React/Vite dashboard (deployed to GitHub Pages)
    src/components/                 TheoryPanel, CalibrationPanel, LocusChart, CountryCard
    src/lib/                        interpolate.js (7-D multilinear), modelJs.js (JS model port)
    public/data/                    Static copies of data/ for the browser

Exchange_Rate_Tariffs/              LaTeX paper source
    paper_draft.tex                 Current working draft
    paper_draft_original.tex        Pre-revision baseline (original version)
    references.bib                  Bibliography
    calibration_results.pdf         Current calibration figure (labeled bars)
    calibration_results_original.pdf Original calibration figure (unlabeled)
    *.pdf                           Model equilibrium figures referenced in paper
```

### Installation

```bash
pip install -e .
```

Requires Python 3.9+. Dependencies (numpy, scipy, pandas, matplotlib, seaborn) are declared in `pyproject.toml`.

To run the dashboard locally:

```bash
cd dashboard
npm install
npm run dev
```

### Reproducing results

**Paper figures** (Sections 2–3): run `notebooks/section3_three_country_model.ipynb`. Figures are written to `Exchange_Rate_Tariffs/`.

**Calibration figure** (Section 4): run `scripts/regenerate_calibration_figure.py`. Output goes to `output/calibration_results.pdf` and is copied to `Exchange_Rate_Tariffs/`.

**Dashboard data**: precomputed files in `data/` are committed. To regenerate from scratch:

```bash
python scripts/precompute_theory_grid.py       # ~9 min (4^6 × 3 = 12,288 points)
python scripts/precompute_calibration_panel.py
python scripts/fetch_fx_data.py                # requires internet
```

### Calibration (Section 4)

Three main configurations appear in the paper body; eight appear in the dashboard and Appendix B. Parameters are calibrated as follows:

| Parameter | Source |
|---|---|
| Expenditure shares $\alpha_{T_j}$ | 2024 world goods export shares (WTO); tradable budget fixed at 0.40 |
| Labor endowments $L_i$ | 2024 PPP GDP (IMF WEO Oct 2024), normalised to $L_A = 1$ (US) |
| $\sigma$ | Amiti, Redding & Weinstein (2019) as anchor (≈6); Fajgelbaum et al. (2020, 2024); Feenstra et al. (2018); varies by config (see table below) |

Tariff regimes (incremental above pre-2025 baseline):

| Regime | $\tau_{AB}$ | $\tau_{BA}$ | $\tau_{AC}$ | Data reference |
|---|---|---|---|---|
| 1 — Fentanyl-related tariffs | 20% | 0% | 0% | March 2025 |
| 2 — Peak escalation | 145% | 125% | 10% | April 2025 |

Extended calibration parameters (Appendix B / dashboard):

| Country C | $\sigma$ | $\alpha_{T,C}$ | $L_C/L_A$ | Rationale |
|---|---|---|---|---|
| European Union | 6 | 0.138 | 0.860 | China Shock 2.0; ARW (2019) central estimate |
| Japan | 4 | 0.051 | 0.226 | Advanced manufactures; below ARW, limited Chinese overlap |
| South Korea | 5 | 0.043 | 0.103 | Electronics/semiconductor overlap |
| Mexico | 5 | 0.044 | 0.113 | Nearshoring; autos and electronics overlap |
| Canada | 2 | 0.038 | 0.086 | Commodity-heavy; low substitutability |
| Vietnam | 8 | 0.026 | 0.055 | China re-export hub; close substitutes |
| Taiwan | 3 | 0.035 | 0.058 | Semiconductor-dominant; low aggregate substitutability |
| India | 3 | 0.031 | 0.497 | Growing manufacturing; limited current overlap |

### Usage

```python
from tariff_exchange_rates import CALIBRATIONS, TARIFF_REGIMES, solve_3country, free_trade

params = CALIBRATIONS["US\u2013China\u2013EU"]
eq_ft  = solve_3country(params, free_trade())
eq_r2  = solve_3country(params, TARIFF_REGIMES["Regime 2 (Peak trade war)"])

e_AC_pct = 100 * (eq_r2["e_AC"] / eq_ft["e_AC"] - 1)
print(f"USD/EUR change under peak trade war: {e_AC_pct:+.2f}%")
```
