# Release Checklist

## Package Smoke
1. `source venv/bin/activate`
2. `./scripts/package_smoke_test.sh`

## Core Test Suite
1. `PYTHONPATH=src ./venv/bin/python -m pytest`

## Manual Runtime Check
1. `export GITHUB_TOKEN=...` (or ensure `gh` is installed and authenticated)
2. `PYTHONPATH=src python -m gh_skyline --year 2024 --user <user> --output smoke-skyline`
3. Verify `smoke-skyline.stl` exists and opens in an STL viewer.

## Go Parity Artifact Import (when available)
1. Export Go artifacts into a folder with subdirs: `ascii/`, `stl/`, `graphql/`, `cli/` and optional `cases.yaml`.
2. Import artifacts:
   - `python tools/import_go_parity_artifacts.py /path/to/go_artifacts`
3. Run parity tests:
   - `PYTHONPATH=src ./venv/bin/python -m pytest tests/parity -q`

## Current Gaps Before Cutover
1. Import and validate richer Go-exported artifact corpus across scenarios.
2. Add CI workflow for release artifact validation.
3. Add performance budget checks for geometry generation.
