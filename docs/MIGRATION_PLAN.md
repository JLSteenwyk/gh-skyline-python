# gh-skyline Python Migration Plan

## Goal
Convert `gh-skyline` from Go to Python while preserving user-visible behavior (`gh skyline` UX, auth, CLI flags, ASCII output, STL output semantics).

## Principles
- Parity before feature work.
- Phased migration with measurable gates.
- Keep extension UX stable.
- Explicitly document intentional behavior differences.

## Milestones
1. M0 - Parity Harness and Fixture Contract
- Create fixture corpus for CLI, ASCII, GraphQL, STL.
- Freeze baseline outputs from Go implementation.
- Define STL comparison policy (byte-identical or canonical semantic parity).

2. M1 - CLI and Auth Foundation
- Implement Python CLI flags and flow parity for `cmd/root.go`.
- Implement `gh`-backed auth adapter and basic GitHub client calls.
- Add integration tests for CLI year parsing and web-profile behavior.

3. M2 - Core Types/Utilities/Error Contracts
- Port `utils`, `errors`, and types semantics.
- Add unit tests for year ranges, filename behavior, and error formatting.

4. M3 - ASCII Parity
- Port ASCII generator and text/block behavior.
- Add frozen-time golden tests for ASCII output.

5. M4 - STL Core Parity
- Port STL binary writer and geometry primitives.
- Add deterministic ordering policy and golden/semantic STL tests.

6. M5 - GitHub Data + Full Skyline Flow
- Port contribution fetching and year-range orchestration.
- Add integration tests for `--full`, `--art-only`, and range behavior.

7. M6 - Packaging and Extension Cutover
- Package Python implementation for `gh extension` compatibility.
- Run Go/Python dual implementation in CI until parity gates pass.

## Deliverables by Area
- CLI: flag matrix parity, help text equivalence, error prefix parity.
- Auth/API: `gh` host/token/GraphQL behavior parity.
- ASCII: output snapshots for fixed fixtures.
- STL: header/triangle count validity + deterministic policy gates.
- Packaging: install and run paths for fresh environment.

## Risks and Controls
- Auth/host drift: use `gh` subprocess adapter first.
- STL nondeterminism: define ordering policy and test for it.
- Performance regressions: benchmark geometry and text raster stages.
- Hidden behavior drift: enforce fixture-based parity checks in CI.
