# Understanding Multilateral Tariffs and Exchange Rates

Code, data and LaTeX sources for *Understanding Multilateral Tariffs and Exchange Rates* by Jason Lu and Dimitre Milkov (IMF Research Department, 2026). The paper characterizes the long-run exchange-rate response to arbitrary tariff vectors in an N-country trade model and reads the 2025 tariff episode through it. The compiled paper is [`paper/main.pdf`](paper/main.pdf). Every number, table and figure in it is rebuilt by `python code/run_all.py`.

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
6. **2025.** A stylized reading of the 2025 episode (no calibration): the retaliation phase is consistent with the trade channel, and the near-uniform phase shows none of the predicted effective appreciation. No phase was a clean single configuration (Phase 1 mixed the China tariffs with North American tariffs and Canadian retaliation), so the reading classifies phases only as far as they approximate one.

## Layout

```
code/
  run_all.py     rebuilds everything below, in order
  model/         nested_ces (exact N-country model), linear (Appendix A),
                 closed_forms (symmetric benchmark), asymmetry, extensions
                 (Ricardo-Viner tradables, transfer-financed imbalances)
  tests/         pytest suite
  checks/        recompute every number in the paper -> code/results/*.json
  tables/        make_tables.py -> paper/tables/
  figures/       one script per figure -> paper/figures/
  data/          fetch_fx_2025.py (FRED, BIS, Fed H.10 weights)
data/
  raw/fx2025/        cached exchange-rate downloads and H.10 weights
  raw/tariffs2025/   2025 tariff timeline with official sources
  raw/trade2024/     2024 trade and GDP data (US-China-ROW footnote)
  processed/         monthly and daily FX series built from raw/fx2025
paper/
  main.tex, sections/, refs.bib, figures/, tables/, main.pdf
archive/         earlier drafts, legacy code, dashboard and reports (not used)
```

Each `data/raw/*` folder has a README with its sources and retrieval dates.

## Rebuilding

Requires Python 3.9+ with numpy, scipy, pandas and matplotlib (`pip install -e ".[test]"` installs these and pytest), plus a LaTeX distribution with `latexmk`.

```bash
python code/run_all.py
```

This runs the tests, the numerical checks, the FX data step, the tables, the figures and `latexmk` on `paper/main.tex`. The FX step (`code/data/fetch_fx_2025.py`) downloads only the raw files missing from `data/raw/fx2025/` and rebuilds `data/processed/` from the cache. The run is therefore offline once the cache exists. To refresh a series, delete its cached file and rerun.

## Tests

```bash
python -m pytest -q code/tests
```

The suite checks the linearization against finite differences and complex-step derivatives of the exact model, the closed forms, the composite-bystander reduction, the welfare lemma, the uniform-tariff proposition, the Appendix D extensions and the 2025 data inputs.

## Archive

[`archive/`](archive/README.md) holds everything that does not produce the current paper: the August single-elasticity draft and derivation notes, the old three-country package with its scripts, notebooks and robustness runs, the retired dashboard, old calibration data, and past build and revision reports. The tag `pre-reorg-2026-10-29` marks the last state before the move.
