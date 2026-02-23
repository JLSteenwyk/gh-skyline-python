# Release Checklist

## Package Smoke
1. `source venv/bin/activate`
2. `./scripts/package_smoke_test.sh`

## Core Test Suite
1. `PYTHONPATH=src ./venv/bin/python -m pytest`

## Build Artifacts Locally
1. `./venv/bin/pip install build twine`
2. `./venv/bin/python -m build`
3. `./venv/bin/python -m twine check dist/*`

## Docs Build Locally
1. `./venv/bin/pip install -r docs/requirements.txt`
2. `./venv/bin/sphinx-build -W -b html docs docs/_build/html`

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

## CI/Release Automation
1. `Python CI` workflow runs package smoke + tests on push/PR.
2. `Release Artifacts` workflow builds and uploads `sdist` + `wheel` on tag push (`v*`) or manual dispatch.
3. `Docs Pages` workflow builds and deploys docs to GitHub Pages.

## Current Gaps Before Final Cutover
1. Expand and tune artifact corpus across multiple real-world scenarios.
2. Add performance budget checks for geometry generation.
3. Optionally add automated PyPI publish job gated on release tags.
