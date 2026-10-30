# Archive

These files do not produce the current paper. They were moved here on 2026-10-29 with `git mv`, so `git log --follow <path>` shows their full history. The tag **`pre-reorg-2026-10-29`** marks the last state before the move. Check it out to see or run anything here in its original location.

Nothing here is maintained. The archived code **does not run from its new location without path changes**: scripts, notebooks and tests refer to `src/`, `data/*.json`, `output/` and `Exchange_Rate_Tariffs/` at the repo root. Date ranges are the first and last commits that touched each path before the move.

## writeups/
- **`Exchange_Rate_Tariffs/`** (2026-04-20 to 2026-08-23): the August draft, with LaTeX sources, bibliography and figures.
  - It uses a single elasticity σ in a three-country model calibrated to the 2025 episode.
  - Superseded by `paper/` (nested CES, N countries).
- **`notes/`** (2026-08-23 to 2026-09-22): derivation notes (`model_derivations.tex`), notes figures, and the earlier `notes/archive/` (results outline of 2026-08-27).
  - Superseded by the paper's sections and appendices.
  - The authors' untracked `notes/local_elasticity_representation.md` was not moved and is still at the repo root.

## code/
- **`src/tariff_exchange_rates/`** (2026-04-20 to 2026-08-23): the old three-country package (flat CES, then the first nested model). Superseded by `code/model/`.
- **`tests/`** (2026-08-22 to 2026-08-23): that package's regression tests. Superseded by `code/tests/`.
- **`scripts/`** (2026-04-20 to 2026-09-22): grid and calibration precomputation, the FX fetch from Yahoo Finance, and referee-claim and threshold derivations. Superseded by `code/checks/`, `code/figures/` and `code/data/`.
- **`robustness/`** (2026-09-22): standalone robustness computations of 22 September 2026, which never went into the paper. Superseded by `code/checks/` (Appendices C and D).
- **`notebooks/`** (2026-04-20 to 2026-08-22): the section 2–4 notebooks of the August draft. Superseded by `code/figures/` and `code/checks/`.

## dashboard/
- **`dashboard/`** (2026-04-20 to 2026-08-23): the React/Vite dashboard, which runs the old single-σ model.
- **`.github/workflows/deploy.yml`** (2026-04-20 to 2026-04-22): its GitHub Pages deploy.

The dashboard is retired and has no successor. Moving the workflow stops future deploys. The site already published stays up until Pages is disabled in the repository settings.

## data/
- **`calibration_inputs.json`, `calibration_nested.json`, `calibration_panel.json`, `fx_data.json`, `theory_grid.json`** (2026-04-20 to 2026-08-23): calibration inputs and precomputed grids for the August draft and the dashboard. Superseded by `data/raw/` and `data/processed/`.
- **`output/`** (2026-09-17): the Liberation Day cross-section and scatter figures. Superseded by Figure 7 of the paper.

## build-reports/
- **`REVISION_PLAN.md`, `REVISION_CHANGES.md`, `revision_framing_memo.md`** (2026-08-22 to 2026-08-29): planning and change logs for the August draft.
- **`BUILD_REPORT.md`, `REVISION_REPORT_v2.md`, `REVISION_REPORT_v3.md`** (2026-10-29): reports on building the LaTeX paper and its v2 and v3 revisions.
- **`REORG_REPORT.md`**: this reorganization.
