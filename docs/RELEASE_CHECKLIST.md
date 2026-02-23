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

## Current Gaps Before Cutover
1. Replace placeholder deterministic text/logo geometry with raster parity implementation.
2. Import Go-exported fixture corpus for stronger differential parity checks.
3. Add CI workflow for package smoke test and release artifact validation.
