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

## Parity Artifact Import (Optional)
1. Prepare artifact folder with subdirs: `ascii/`, `stl/`, `graphql/`, `cli/` and optional `cases.yaml`.
2. Import artifacts:
   - `python tools/import_parity_artifacts.py /path/to/artifacts`
3. Run parity tests:
   - `PYTHONPATH=src ./venv/bin/python -m pytest tests/parity -q`

## Current Gaps Before Cutover
1. Expand and tune artifact corpus across multiple real-world scenarios.
2. Add release artifact validation workflow.
3. Add performance budget checks for geometry generation.
