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
- [~] M4 - STL Core Parity (writer + deterministic geometry foundation implemented; text/logo geometry pending)
- [x] M5 - GitHub Data + Full Skyline Flow (year/user/full orchestration + STL generator wiring implemented)
- [ ] M6 - Packaging and Extension Cutover

## MVP Definition
- CLI can fetch contribution history via `gh` adapter.
- CLI can generate ASCII output and write a valid STL skyline (base + columns).
- End-to-end integration test validates a generated non-empty STL file.

## MVP Status
- Achieved in current branch.
- Remaining non-MVP work: full text/logo geometry parity, deeper Go-output parity fixtures, release packaging/cutover.

## Completed This Update
- Added robust entrypoint error handling in `src/gh_skyline/__main__.py`.
- Added end-to-end CLI generation tests in `tests/integration/test_end_to_end_cli.py`.
- Added entrypoint tests in `tests/unit/test_main_entrypoint.py`.

## Verification
- Test command: `PYTHONPATH=src ./venv/bin/python -m pytest`
- Result: expected green (run after this update)

## Next Tasks
1. Implement `stl/geometry/text.py` parity for embossed text/logo geometry.
2. Expand parity corpus with Go-exported real command outputs for multiple scenarios.
3. Add packaging/entrypoint behavior checks for extension cutover.
4. Define and enforce performance budget checks for geometry generation.
