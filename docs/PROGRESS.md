# Migration Progress

## Snapshot
- Date: 2026-02-23
- Status: MVP achieved
- Current milestone: M5 complete enough for MVP

## Milestone Checklist
- [x] M0 - Parity Harness and Fixture Contract (initial fixture corpus and fixture-consuming tests)
- [x] M1 - CLI and Auth Foundation (initial implementation)
- [x] M2 - Core Types/Utilities/Error Contracts (initial implementation)
- [~] M3 - ASCII Parity (core generator + header template support + fixture-driven golden tests; fine-grained rendering parity still pending)
- [~] M4 - STL Core Parity (writer + deterministic geometry foundation + deterministic text/logo placeholder implemented; pixel-level parity pending)
- [x] M5 - GitHub Data + Full Skyline Flow (year/user/full orchestration + STL generator wiring implemented)
- [ ] M6 - Packaging and Extension Cutover

## MVP Definition
- CLI can fetch contribution history via `gh` adapter or token fallback.
- CLI can generate ASCII output and write a valid STL skyline.
- End-to-end integration test validates a generated non-empty STL file.

## MVP Status
- Achieved in current branch.
- Remaining non-MVP work: true text/logo raster parity vs Go, deeper Go-output parity fixtures, release packaging/cutover.

## Completed This Update
- Implemented deterministic text/logo geometry module: `src/gh_skyline/stl/geometry/text.py`.
- Integrated text/logo geometry into STL generation pipeline in deterministic order.
- Added unit tests for text/logo geometry and year label logic.

## Verification
- Test command: `PYTHONPATH=src ./venv/bin/python -m pytest`
- Result: expected green (run after this update)

## Next Tasks
1. Replace deterministic text/logo placeholder with raster-based parity implementation using embedded assets.
2. Expand parity corpus with Go-exported real command outputs for multiple scenarios.
3. Add packaging/entrypoint behavior checks for extension cutover.
4. Define and enforce performance budget checks for geometry generation.
