<p align="center">
  <a href="https://github.com/JLSteenwyk/gh-skyline-python">
    <img src="docs/assets/logo.png" alt="gh-skyline-python logo" width="180">
  </a>
  <p align="center">
    <a href="docs/MIGRATION_PLAN.md">Plan</a>
    ·
    <a href="https://github.com/JLSteenwyk/gh-skyline-python/issues">Report Bug</a>
    ·
    <a href="https://github.com/JLSteenwyk/gh-skyline-python/issues">Request Feature</a>
  </p>
  <p align="center">
    <a href="https://github.com/JLSteenwyk/gh-skyline-python/actions/workflows/python-ci.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/JLSteenwyk/gh-skyline-python/python-ci.yml?label=tests" alt="Tests">
    </a>
    <a href="https://github.com/JLSteenwyk/gh-skyline-python/actions/workflows/release-artifacts.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/JLSteenwyk/gh-skyline-python/release-artifacts.yml?label=release%20artifacts" alt="Release Artifacts">
    </a>
    <a href="https://github.com/JLSteenwyk/gh-skyline-python">
      <img src="https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue" alt="Python Versions">
    </a>
    <a href="https://github.com/JLSteenwyk/gh-skyline-python/graphs/contributors">
      <img src="https://img.shields.io/github/contributors/JLSteenwyk/gh-skyline-python" alt="Contributors">
    </a>
  </p>
</p>

# gh-skyline-python

Python-only MVP of GitHub Skyline generation.

This project can fetch GitHub contribution history, render ASCII output, and generate an STL skyline.

## Current Status

## Python-Only Workflow

This project does not require Go for development, testing, or fixture generation.
All parity artifacts and tests are generated/validated using Python tooling in this repo.

- MVP: ready for local skyline generation
- Test status: `52 passed`
- Not complete yet: final parity tuning and release cutover polish

See migration tracking in:

- `docs/MIGRATION_PLAN.md`
- `docs/PROGRESS.md`

## Requirements

- Python 3.11+
- Network access to GitHub GraphQL API
- Auth via one of:
1. `gh` CLI auth session (`gh auth login`)
2. `GITHUB_TOKEN` or `GH_TOKEN`

## Setup

```bash
cd gh-skyline-python
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -e .[dev]
```

## Usage

Run as module:

```bash
PYTHONPATH=src python -m gh_skyline --year 2024 --user JLSteenwyk --output my-skyline
```

Or after editable install:

```bash
gh-skyline --year 2024 --user JLSteenwyk --output my-skyline
```

### Multiple years

```bash
PYTHONPATH=src python -m gh_skyline --user JLSteenwyk --year 2019-2024 --output my-skyline
```

### Full history (join year to now)

```bash
PYTHONPATH=src python -m gh_skyline --user JLSteenwyk --full --output my-skyline
```

### ASCII preview only

```bash
PYTHONPATH=src python -m gh_skyline --year 2024 --user JLSteenwyk --art-only
```

## Auth Notes

If `gh` is installed and on `PATH`, the tool uses it first.

If `gh` is not installed, set a token:

```bash
export GITHUB_TOKEN=YOUR_TOKEN
```

Optional GHES host override:

```bash
export GH_HOST=github.example.com
```

## Testing

```bash
source venv/bin/activate
PYTHONPATH=src python -m pytest
```

## Output

- Default output filename pattern: `{username}-{year|year-range}-github-skyline.stl`
- If `--output` omits `.stl`, the extension is added automatically.
