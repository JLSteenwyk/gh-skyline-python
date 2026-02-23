# Migration Progress

## Snapshot
- Date: 2026-02-23
- Status: MVP achieved
- Current milestone: M6 started

## Milestone Checklist
- [x] M0 - Parity Harness and Fixture Contract (fixture corpus and fixture-consuming tests)
- [x] M1 - CLI and Auth Foundation (implemented)
- [x] M2 - Core Types/Utilities/Error Contracts (implemented)
- [~] M3 - ASCII Parity (implemented with golden tests; tuning remains)
- [~] M4 - STL Core Parity (implemented with deterministic geometry + raster text/logo; tuning remains)
- [x] M5 - GitHub Data + Full Skyline Flow (implemented)
- [~] M6 - Packaging and Extension Cutover (packaging + smoke checks + CI added; release artifact flow pending)

## MVP Definition
- CLI can fetch contribution history via `gh` adapter or token fallback.
- CLI can generate ASCII output and write a valid STL skyline.
- End-to-end integration test validates a generated non-empty STL file.

## MVP Status
- Achieved in current branch.
- Remaining non-MVP work: parity tuning and release artifact workflow.

## Completed This Update
- Removed Go-dependent parity workflow requirements from docs and process.
- Added generic parity import script: `tools/import_parity_artifacts.py`.
- Removed Go-specific import script.
- Kept fixture generation and validation fully Python-based.

## Verification
- Local package smoke test: `./scripts/package_smoke_test.sh`.
- Local tests: `PYTHONPATH=src ./venv/bin/python -m pytest`.

## Next Tasks
1. Expand parity artifacts with additional real-world scenarios.
2. Add release artifact workflow for distribution.
3. Define and enforce performance budget checks for geometry generation.
4. Tune raster geometry constants against artifact baselines.
