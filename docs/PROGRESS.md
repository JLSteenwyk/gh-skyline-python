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
- [~] M6 - Packaging and Extension Cutover (editable install + smoke checks + CI workflow added; Go artifact import workflow added)

## MVP Definition
- CLI can fetch contribution history via `gh` adapter or token fallback.
- CLI can generate ASCII output and write a valid STL skyline.
- End-to-end integration test validates a generated non-empty STL file.

## MVP Status
- Achieved in current branch.
- Remaining non-MVP work: import richer Go parity outputs and complete release artifact flow.

## Completed This Update
- Expanded generated parity corpus to multiple years (2020-2024) and added multi-year STL fixture.
- Added tool for importing Go-exported parity artifacts: `tools/import_go_parity_artifacts.py`.
- Updated parity tests to validate expanded yearly fixture set.
- Updated release checklist with explicit Go-artifact import step.

## Verification
- Local package smoke test: `./scripts/package_smoke_test.sh`.
- Local tests: `PYTHONPATH=src ./venv/bin/python -m pytest`.

## Next Tasks
1. Import real Go-exported artifacts and tune constants for tighter parity.
2. Add release artifact workflow for extension distribution.
3. Define and enforce performance budget checks for geometry generation.
