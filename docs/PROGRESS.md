# Migration Progress

## Snapshot
- Date: 2026-02-23
- Status: MVP achieved
- Current milestone: M6 started

## Milestone Checklist
- [x] M0 - Parity Harness and Fixture Contract (initial fixture corpus and fixture-consuming tests)
- [x] M1 - CLI and Auth Foundation (initial implementation)
- [x] M2 - Core Types/Utilities/Error Contracts (initial implementation)
- [~] M3 - ASCII Parity (core generator + header template support + fixture-driven golden tests; fine-grained rendering parity still pending)
- [~] M4 - STL Core Parity (writer + deterministic geometry foundation + raster-based text/logo embossing implemented; numeric parity tuning pending)
- [x] M5 - GitHub Data + Full Skyline Flow (year/user/full orchestration + STL generator wiring implemented)
- [~] M6 - Packaging and Extension Cutover (editable install + smoke checks + CI workflow added; release artifact flow pending)

## MVP Definition
- CLI can fetch contribution history via `gh` adapter or token fallback.
- CLI can generate ASCII output and write a valid STL skyline.
- End-to-end integration test validates a generated non-empty STL file.

## MVP Status
- Achieved in current branch.
- Remaining non-MVP work: deeper Go-output parity fixtures, release packaging/cutover.

## Completed This Update
- Replaced deterministic placeholder text/logo geometry with raster-based implementation using embedded assets.
- Added Pillow runtime dependency in `pyproject.toml`.
- Updated text/logo geometry tests for the raster path.

## Verification
- Local package smoke test: `./scripts/package_smoke_test.sh`.
- Local tests: `PYTHONPATH=src ./venv/bin/python -m pytest`.

## Next Tasks
1. Expand parity corpus with Go-exported real command outputs for multiple scenarios.
2. Add release artifact workflow for extension distribution.
3. Define and enforce performance budget checks for geometry generation.
4. Tune raster geometry constants against Go parity baselines.
