# gh-skyline-python

Python MVP of GitHub Skyline generation.

This project can fetch GitHub contribution history, render ASCII output, and generate an STL skyline (base + columns).

## Current Status

- MVP: ready for local skyline generation
- Test status: `44 passed`
- Not complete yet: text/logo STL geometry parity and final extension packaging cutover

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
pip install -e .
pip install pytest pyyaml
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
