# gh-skyline Python Migration Plan

## Goal
Ship a fully Python-based GitHub Skyline tool with stable behavior, deterministic outputs, and reproducible packaging.

## Principles
- Python-only execution and validation workflow.
- Contract-first development with fixture-backed parity checks.
- Deterministic outputs for repeatable testing.
- Preserve CLI UX and documented flags.

## Milestones
1. M0 - Parity Harness and Fixture Contract
- Maintain fixture corpus for CLI, ASCII, GraphQL, STL.
- Baseline snapshots are generated from the Python implementation.
- Enforce deterministic STL policy and schema checks.

2. M1 - CLI and Auth Foundation
- Implement CLI flags and flow parity with documented behavior.
- Implement auth adapter (`gh` when present, token HTTPS fallback).
- Add integration tests for CLI year parsing and web-profile behavior.

3. M2 - Core Types/Utilities/Error Contracts
- Implement utility and error contracts.
- Add unit tests for year ranges, filename behavior, and error formatting.

4. M3 - ASCII Parity
- Implement ASCII generator and text/block behavior.
- Add frozen-time golden tests for ASCII output.

5. M4 - STL Core Parity
- Implement STL writer and geometry primitives.
- Enforce deterministic ordering and structural validation.
- Implement raster-based text/logo embossing.

6. M5 - GitHub Data + Full Skyline Flow
- Implement contribution fetching and year-range orchestration.
- Add integration tests for `--full`, `--art-only`, and range behavior.

7. M6 - Packaging and Extension Cutover
- Harden packaging and entrypoint behavior.
- Add CI for package smoke + test suite.
- Add release artifact workflow.

## Deliverables by Area
- CLI: flag matrix parity, help text equivalence, error prefix parity.
- Auth/API: host/token/GraphQL behavior parity.
- ASCII: output snapshots for fixed fixtures.
- STL: header/triangle count validity + deterministic policy gates.
- Packaging: install and run paths for fresh environment.

## Risks and Controls
- Auth/host drift: keep both `gh` and token fallback covered by tests.
- STL nondeterminism: lock ordering + structural assertions.
- Performance regressions: benchmark geometry and text raster stages.
- Hidden behavior drift: enforce fixture-based parity checks in CI.
