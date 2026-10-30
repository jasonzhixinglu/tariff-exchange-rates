# Repository reorganization report (2026-10-29)

Branch `repo-reorg`, created from `main` after `main` was fast-forwarded to `paper-draft-v3`. It is not merged and not pushed. The branches `paper-draft-v1`, `-v2` and `-v3` are left in place.

## Step 0: merge, tag, branch
- **Working tree before starting:** clean for tracked files. The only untracked file was `notes/local_elasticity_representation.md`, which was left alone and not committed.
- **Merge:** `main` (8f420b6) was an ancestor of `paper-draft-v3`, so the merge was a fast-forward to 9e982d4 (`git merge --ff-only`). There were no conflicts.
- **Tag:** lightweight tag `pre-reorg-2026-10-29` on 9e982d4, local only.
- **Commits on `repo-reorg`:**
  1. `44b7fde` Move legacy code, write-ups, dashboard, old data and reports to archive/. Pure renames, all 132 at 100% similarity.
  2. `8e00007` Fix configuration after the move: .gitignore, pyproject, stale path.
  3. Rewrite README for the production repo; add archive index.
  4. This report.

## Top-level layout

Before (tracked):
```
.github/  .gitignore  BUILD_REPORT.md  Exchange_Rate_Tariffs/  README.md
REVISION_CHANGES.md  REVISION_PLAN.md  REVISION_REPORT_v2.md  REVISION_REPORT_v3.md
code/  dashboard/  data/  notebooks/  notes/  output/  paper/  pyproject.toml
revision_framing_memo.md  robustness/  scripts/  src/  tests/
```
After (tracked):
```
.gitignore  README.md  archive/  code/  data/  paper/  pyproject.toml
```

The working directory also keeps three untracked items:
- `notes/`, which now holds only the authors' `local_elasticity_representation.md`;
- `gdrive_files/` (gitignored);
- local tool folders `.claude/` and `.pytest_cache/` (gitignored).

## Confirming the production list

I traced what production reads in three places: `code/run_all.py` and every script it calls, the tests, and the LaTeX build (`\input`, `\includegraphics` with `graphicspath{figures/}`, and `\bibliography{refs}`). Production reads only:
- `data/raw/fx2025/`
- `data/raw/tariffs2025/`
- `data/raw/trade2024/trade_2024.json`
- `data/processed/`
- `code/`
- `paper/`

No production file imports `tariff_exchange_rates`, and none reads `data/*.json`, `output/`, `notes/` or `Exchange_Rate_Tariffs/`. Nothing outside the keep list was needed.

The other files in `data/raw/trade2024/` (Census, GACC, IMF and WTO source downloads) are not read by code. They are the documented sources of `trade_2024.json` and stay with it as the task listed.

## Classification of files not on either list
- **`dashboard/.gitignore`** (tracked) moved with the dashboard, to `archive/dashboard/dashboard/.gitignore`.
- **`notes/archive/README.md`** and the rest of `notes/` moved as a group to `archive/writeups/notes/`. The one exception is the untracked author file named above.
- **Ignored local files inside the moved folders** were moved with plain `mv` so that their source folders could disappear:
  - LaTeX aux and log files and `literature_review/` in `Exchange_Rate_Tariffs/`;
  - `node_modules/` and `dist/` in `dashboard/`;
  - untracked figures, CSVs and text in `output/`;
  - run logs in `robustness/results/`;
  - `src/tariff_exchange_rates.egg-info/`;
  - aux and log files in `notes/`.

  These moves did not touch git.
- **Deleted untracked root junk:** `multilateral_tariff_exchange_rate_results.aux`, `multilateral_tariff_exchange_rate_results.log`, `texput.log`. A `tariff_exchange_rates.egg-info/` created by my own `pip install --dry-run` check was also removed.
- **`data/raw/trade2024/bea_NipaDataA.txt`** (ignored, kept locally) stays in production data, as before.

## Moves (132, all `git mv`)
- `BUILD_REPORT.md` → `archive/build-reports/BUILD_REPORT.md`
- `REVISION_CHANGES.md` → `archive/build-reports/REVISION_CHANGES.md`
- `REVISION_PLAN.md` → `archive/build-reports/REVISION_PLAN.md`
- `REVISION_REPORT_v2.md` → `archive/build-reports/REVISION_REPORT_v2.md`
- `REVISION_REPORT_v3.md` → `archive/build-reports/REVISION_REPORT_v3.md`
- `revision_framing_memo.md` → `archive/build-reports/revision_framing_memo.md`
- `notebooks/section2_two_country_model.ipynb` → `archive/code/notebooks/section2_two_country_model.ipynb`
- `notebooks/section3_three_country_model.ipynb` → `archive/code/notebooks/section3_three_country_model.ipynb`
- `notebooks/section4_calibration.ipynb` → `archive/code/notebooks/section4_calibration.ipynb`
- `robustness/check_neer_calibration.py` → `archive/code/robustness/check_neer_calibration.py`
- `robustness/figures/task_a_threshold.png` → `archive/code/robustness/figures/task_a_threshold.png`
- `robustness/figures/task_b_threshold.png` → `archive/code/robustness/figures/task_b_threshold.png`
- `robustness/figures/task_c_sensitivities.png` → `archive/code/robustness/figures/task_c_sensitivities.png`
- `robustness/figures/task_d_search.png` → `archive/code/robustness/figures/task_d_search.png`
- `robustness/make_figures.py` → `archive/code/robustness/make_figures.py`
- `robustness/model.py` → `archive/code/robustness/model.py`
- `robustness/results/check_neer_calibration.json` → `archive/code/robustness/results/check_neer_calibration.json`
- `robustness/results/task_a.json` → `archive/code/robustness/results/task_a.json`
- `robustness/results/task_b.json` → `archive/code/robustness/results/task_b.json`
- `robustness/results/task_c.json` → `archive/code/robustness/results/task_c.json`
- `robustness/results/task_c_decomp.json` → `archive/code/robustness/results/task_c_decomp.json`
- `robustness/results/task_d_common.npz` → `archive/code/robustness/results/task_d_common.npz`
- `robustness/results/task_d_draws.json` → `archive/code/robustness/results/task_d_draws.json`
- `robustness/results/task_d_order_cases.json` → `archive/code/robustness/results/task_d_order_cases.json`
- `robustness/results/task_d_rho_scan.json` → `archive/code/robustness/results/task_d_rho_scan.json`
- `robustness/results/task_d_targeted_common.json` → `archive/code/robustness/results/task_d_targeted_common.json`
- `robustness/results/verify.json` → `archive/code/robustness/results/verify.json`
- `robustness/robustness_results.md` → `archive/code/robustness/robustness_results.md`
- `robustness/style.py` → `archive/code/robustness/style.py`
- `robustness/task_a.py` → `archive/code/robustness/task_a.py`
- `robustness/task_b.py` → `archive/code/robustness/task_b.py`
- `robustness/task_c.py` → `archive/code/robustness/task_c.py`
- `robustness/task_c_decomp.py` → `archive/code/robustness/task_c_decomp.py`
- `robustness/task_d.py` → `archive/code/robustness/task_d.py`
- `robustness/task_d_rho_scan.py` → `archive/code/robustness/task_d_rho_scan.py`
- `robustness/verify.py` → `archive/code/robustness/verify.py`
- `scripts/calibrate_nested.py` → `archive/code/scripts/calibrate_nested.py`
- `scripts/derive_N_country.py` → `archive/code/scripts/derive_N_country.py`
- `scripts/derive_general_threshold.py` → `archive/code/scripts/derive_general_threshold.py`
- `scripts/derive_kappa_asymmetric.py` → `archive/code/scripts/derive_kappa_asymmetric.py`
- `scripts/derive_symmetric_N_system.py` → `archive/code/scripts/derive_symmetric_N_system.py`
- `scripts/fetch_fx_data.py` → `archive/code/scripts/fetch_fx_data.py`
- `scripts/liberation_day_cross_section.py` → `archive/code/scripts/liberation_day_cross_section.py`
- `scripts/liberation_day_scatter.py` → `archive/code/scripts/liberation_day_scatter.py`
- `scripts/make_calibration_figure_nested.py` → `archive/code/scripts/make_calibration_figure_nested.py`
- `scripts/make_loci_multipanel.py` → `archive/code/scripts/make_loci_multipanel.py`
- `scripts/make_theory_figures.py` → `archive/code/scripts/make_theory_figures.py`
- `scripts/make_threshold_figure.py` → `archive/code/scripts/make_threshold_figure.py`
- `scripts/precompute_calibration_panel.py` → `archive/code/scripts/precompute_calibration_panel.py`
- `scripts/precompute_theory_grid.py` → `archive/code/scripts/precompute_theory_grid.py`
- `scripts/regenerate_calibration_figure.py` → `archive/code/scripts/regenerate_calibration_figure.py`
- `scripts/rv_prototype.py` → `archive/code/scripts/rv_prototype.py`
- `scripts/settled_schedule_cross_section.py` → `archive/code/scripts/settled_schedule_cross_section.py`
- `scripts/verify_derivation_notes.py` → `archive/code/scripts/verify_derivation_notes.py`
- `scripts/verify_framing_memo_checks.py` → `archive/code/scripts/verify_framing_memo_checks.py`
- `scripts/verify_referee_claims.py` → `archive/code/scripts/verify_referee_claims.py`
- `scripts/verify_restructured_results.py` → `archive/code/scripts/verify_restructured_results.py`
- `src/tariff_exchange_rates/__init__.py` → `archive/code/src/tariff_exchange_rates/__init__.py`
- `src/tariff_exchange_rates/economy.py` → `archive/code/src/tariff_exchange_rates/economy.py`
- `src/tariff_exchange_rates/equilibrium.py` → `archive/code/src/tariff_exchange_rates/equilibrium.py`
- `src/tariff_exchange_rates/nested.py` → `archive/code/src/tariff_exchange_rates/nested.py`
- `src/tariff_exchange_rates/parameters.py` → `archive/code/src/tariff_exchange_rates/parameters.py`
- `src/tariff_exchange_rates/plotting.py` → `archive/code/src/tariff_exchange_rates/plotting.py`
- `src/tariff_exchange_rates/tariffs.py` → `archive/code/src/tariff_exchange_rates/tariffs.py`
- `tests/test_economy.py` → `archive/code/tests/test_economy.py`
- `tests/test_nested.py` → `archive/code/tests/test_nested.py`
- `.github/workflows/deploy.yml` → `archive/dashboard/.github/workflows/deploy.yml`
- `dashboard/.gitignore` → `archive/dashboard/dashboard/.gitignore`
- `dashboard/index.html` → `archive/dashboard/dashboard/index.html`
- `dashboard/package-lock.json` → `archive/dashboard/dashboard/package-lock.json`
- `dashboard/package.json` → `archive/dashboard/dashboard/package.json`
- `dashboard/postcss.config.js` → `archive/dashboard/dashboard/postcss.config.js`
- `dashboard/public/data/calibration_panel.json` → `archive/dashboard/dashboard/public/data/calibration_panel.json`
- `dashboard/public/data/fx_data.json` → `archive/dashboard/dashboard/public/data/fx_data.json`
- `dashboard/public/data/theory_grid.json` → `archive/dashboard/dashboard/public/data/theory_grid.json`
- `dashboard/src/App.jsx` → `archive/dashboard/dashboard/src/App.jsx`
- `dashboard/src/components/AboutPanel.jsx` → `archive/dashboard/dashboard/src/components/AboutPanel.jsx`
- `dashboard/src/components/CalibrationPanel.jsx` → `archive/dashboard/dashboard/src/components/CalibrationPanel.jsx`
- `dashboard/src/components/CountryCard.jsx` → `archive/dashboard/dashboard/src/components/CountryCard.jsx`
- `dashboard/src/components/LocusChart.jsx` → `archive/dashboard/dashboard/src/components/LocusChart.jsx`
- `dashboard/src/components/TheoryPanel.jsx` → `archive/dashboard/dashboard/src/components/TheoryPanel.jsx`
- `dashboard/src/index.css` → `archive/dashboard/dashboard/src/index.css`
- `dashboard/src/lib/interpolate.js` → `archive/dashboard/dashboard/src/lib/interpolate.js`
- `dashboard/src/lib/modelJs.js` → `archive/dashboard/dashboard/src/lib/modelJs.js`
- `dashboard/src/main.jsx` → `archive/dashboard/dashboard/src/main.jsx`
- `dashboard/tailwind.config.js` → `archive/dashboard/dashboard/tailwind.config.js`
- `dashboard/vite.config.js` → `archive/dashboard/dashboard/vite.config.js`
- `data/calibration_inputs.json` → `archive/data/calibration_inputs.json`
- `data/calibration_nested.json` → `archive/data/calibration_nested.json`
- `data/calibration_panel.json` → `archive/data/calibration_panel.json`
- `data/fx_data.json` → `archive/data/fx_data.json`
- `output/liberation_day_cross_section.pdf` → `archive/data/output/liberation_day_cross_section.pdf`
- `output/liberation_day_cross_section.png` → `archive/data/output/liberation_day_cross_section.png`
- `output/liberation_day_scatter.pdf` → `archive/data/output/liberation_day_scatter.pdf`
- `output/liberation_day_scatter.png` → `archive/data/output/liberation_day_scatter.png`
- `output/settled_schedule_cross_section.pdf` → `archive/data/output/settled_schedule_cross_section.pdf`
- `output/settled_schedule_cross_section.png` → `archive/data/output/settled_schedule_cross_section.png`
- `data/theory_grid.json` → `archive/data/theory_grid.json`
- `Exchange_Rate_Tariffs/2c2s1f_eq.pdf` → `archive/writeups/Exchange_Rate_Tariffs/2c2s1f_eq.pdf`
- `Exchange_Rate_Tariffs/2c2s1f_with_tariffs_eq.pdf` → `archive/writeups/Exchange_Rate_Tariffs/2c2s1f_with_tariffs_eq.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CD_free_trade.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CD_free_trade.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CD_isolated_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CD_isolated_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CD_trade_war.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CD_trade_war.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CD_uniform_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CD_uniform_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CES05_isolated_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CES05_isolated_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CES2_isolated_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CES2_isolated_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CES2_uniform_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CES2_uniform_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CESp5_isolated_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CESp5_isolated_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_CESp5_uniform_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_CESp5_uniform_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_eq.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_eq.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_eq_single_tariff.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_eq_single_tariff.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_eq_trade_war.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_eq_trade_war.pdf`
- `Exchange_Rate_Tariffs/3c2s1f_eq_uniform_tariffs.pdf` → `archive/writeups/Exchange_Rate_Tariffs/3c2s1f_eq_uniform_tariffs.pdf`
- `Exchange_Rate_Tariffs/calibration_nested_results.pdf` → `archive/writeups/Exchange_Rate_Tariffs/calibration_nested_results.pdf`
- `Exchange_Rate_Tariffs/calibration_results.pdf` → `archive/writeups/Exchange_Rate_Tariffs/calibration_results.pdf`
- `Exchange_Rate_Tariffs/calibration_results_original.pdf` → `archive/writeups/Exchange_Rate_Tariffs/calibration_results_original.pdf`
- `Exchange_Rate_Tariffs/loci_multipanel.pdf` → `archive/writeups/Exchange_Rate_Tariffs/loci_multipanel.pdf`
- `Exchange_Rate_Tariffs/main.tex` → `archive/writeups/Exchange_Rate_Tariffs/main.tex`
- `Exchange_Rate_Tariffs/paper_draft.pdf` → `archive/writeups/Exchange_Rate_Tariffs/paper_draft.pdf`
- `Exchange_Rate_Tariffs/paper_draft.tex` → `archive/writeups/Exchange_Rate_Tariffs/paper_draft.tex`
- `Exchange_Rate_Tariffs/references.bib` → `archive/writeups/Exchange_Rate_Tariffs/references.bib`
- `Exchange_Rate_Tariffs/three_country_two_sector_one_factor_model.tex` → `archive/writeups/Exchange_Rate_Tariffs/three_country_two_sector_one_factor_model.tex`
- `Exchange_Rate_Tariffs/threshold_figure.pdf` → `archive/writeups/Exchange_Rate_Tariffs/threshold_figure.pdf`
- `Exchange_Rate_Tariffs/two_country_price_index.tex` → `archive/writeups/Exchange_Rate_Tariffs/two_country_price_index.tex`
- `Exchange_Rate_Tariffs/two_country_two_sector_one_factor_model.tex` → `archive/writeups/Exchange_Rate_Tariffs/two_country_two_sector_one_factor_model.tex`
- `notes/archive/2026-08-27_multilateral_results_outline.pdf` → `archive/writeups/notes/archive/2026-08-27_multilateral_results_outline.pdf`
- `notes/archive/2026-08-27_multilateral_results_outline.tex` → `archive/writeups/notes/archive/2026-08-27_multilateral_results_outline.tex`
- `notes/archive/README.md` → `archive/writeups/notes/archive/README.md`
- `notes/figures/fig1_two_country.pdf` → `archive/writeups/notes/figures/fig1_two_country.pdf`
- `notes/figures/fig3_decomposition.pdf` → `archive/writeups/notes/figures/fig3_decomposition.pdf`
- `notes/model_derivations.pdf` → `archive/writeups/notes/model_derivations.pdf`
- `notes/model_derivations.tex` → `archive/writeups/notes/model_derivations.tex`

## Fixes
- **`pyproject.toml`**
  - It no longer packages anything: `[tool.setuptools.packages.find] where = ["src"]` is replaced by `[tool.setuptools] packages = []`. The production code is run as scripts and is not a package.
  - Dependencies are now numpy, scipy, pandas and matplotlib, with pytest under the `test` extra.
  - Dropped statsmodels, seaborn and tqdm, which no tracked code imports.
  - Version 0.1.0 → 0.2.0, and the description now names the paper.
  - `pip install --dry-run -e ".[test]"` resolves.
- **`.gitignore`**
  - The `Exchange_Rate_Tariffs/...` rules now point to `archive/writeups/Exchange_Rate_Tariffs/...`.
  - `output/` is now `archive/data/output/`. The six Liberation Day figures stay tracked.
  - The `.bbl`, `.blg` and `.toc` rules were `paper/`-only and now apply everywhere. `texput.log` is ignored.
- **Paths:**
  - The only reference from production into a moved file was the docstring of `code/checks/us_china_row.py`. It said "For BUILD_REPORT only" and now names `archive/build-reports/BUILD_REPORT.md`.
  - The paper sources had no such references.
  - Nothing inside `archive/` was edited. New files there: `archive/README.md` and this report.
- **`README.md`:** rewritten with the paper paragraph, the results (kept), the layout tree, rebuild and test instructions, and a pointer to `archive/`. The "Legacy" and dashboard sections are removed.

## Notes for the authors
- **`--fetch`:** the task mentions `python code/run_all.py --fetch`, but `run_all.py` has no such flag. Its FX step always runs and is cache-aware: it downloads only missing raw files and is offline once the cache exists. The README documents that behaviour (refresh by deleting the cached file) rather than an option that doesn't exist.
- **Dashboard:** moving `deploy.yml` stops future deploys. The site already published on GitHub Pages stays up until Pages is disabled in the repository settings.
- **Legacy package:** `tariff-exchange-rates` 0.1.0 is still installed in the local Python environment from the old `src/` layout. Run `pip uninstall tariff-exchange-rates`, or reinstall with `pip install -e .`.
- **`us_china_row.py` docstring:** it says its output is "not a claim in the paper", but since v2 the US–China–ROW footnote in §4.5 uses these numbers. This was not changed here.

## Verification (on `repo-reorg`)
- **Tests:** `python -m pytest -q code/tests` gives 345 passed. The same result holds inside `run_all.py`.
- **Build:** `python code/run_all.py` exits 0.
  - No undefined references or citations.
  - Two overfull boxes (2.8pt and 1.5pt), unchanged from before.
- **PDF content:** the rebuilt `paper/main.pdf` matches the PDF at `pre-reorg-2026-10-29`. Text extracted page by page with PyMuPDF is identical on all 55 pages.
  - Rebuilt figures and the PDF differed from the committed ones only in `/CreationDate`, checked byte for byte after removing it.
  - The committed versions were therefore restored and not recommitted.
- **`git log --follow`:** checked on a sample of moved files.

  | File | Commits | Oldest |
  |---|---|---|
  | `archive/code/src/tariff_exchange_rates/nested.py` | 2 | 2026-08-22 |
  | `archive/writeups/Exchange_Rate_Tariffs/paper_draft.tex` | 10 | 2026-04-20 |
  | `archive/dashboard/dashboard/src/App.jsx` | 4 | 2026-04-20 |
  | `archive/data/theory_grid.json` | 4 | 2026-04-20 |
  | `archive/build-reports/REVISION_CHANGES.md` | 59 | 2026-08-23 |
  | `archive/writeups/notes/model_derivations.tex` | 77 | 2026-08-23 |
  | `archive/dashboard/.github/workflows/deploy.yml` | 3 | 2026-04-20 |

## git status (before committing this report)
```
On branch repo-reorg
Untracked files:
	notes/
nothing added to commit but untracked files present
```
