# Migration Progress

## Snapshot
- Date: 2026-02-23
- Status: MVP achieved
- Current milestone: M6 in progress

## Milestone Checklist
- [x] M0 - Parity Harness and Fixture Contract (fixture corpus and fixture-consuming tests)
- [x] M1 - CLI and Auth Foundation (implemented)
- [x] M2 - Core Types/Utilities/Error Contracts (implemented)
- [~] M3 - ASCII Parity (implemented with golden tests; tuning remains)
- [~] M4 - STL Core Parity (implemented with deterministic geometry + raster text/logo; tuning remains)
- [x] M5 - GitHub Data + Full Skyline Flow (implemented)
- [~] M6 - Packaging and Extension Cutover (packaging + smoke checks + CI + release artifact workflow added)

## MVP Definition
- CLI can fetch contribution history via `gh` adapter or token fallback.
- CLI can generate ASCII output and write a valid STL skyline.
- End-to-end integration test validates a generated non-empty STL file.

## MVP Status
- Achieved in current branch.
- Remaining non-MVP work: parity tuning and performance budget enforcement.

## Completed This Update
- Added release artifact workflow: `.github/workflows/release-artifacts.yml`.
- Workflow now builds `sdist` and `wheel`, runs `twine check`, and uploads artifacts.
- Added docs publishing workflow: `.github/workflows/docs-pages.yml` for GitHub Pages deployment.
- Updated release checklist with docs build + publishing steps.

## Verification
- Local package smoke test: `./scripts/package_smoke_test.sh`.
- Local tests: `PYTHONPATH=src ./venv/bin/python -m pytest`.

## Next Tasks
1. Expand parity artifacts with additional real-world scenarios.
2. Define and enforce performance budget checks for geometry generation.
3. Optionally add automated publish flow for tagged releases.
