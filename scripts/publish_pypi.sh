#!/usr/bin/env bash
set -euo pipefail

# Build and upload package artifacts to PyPI.
# Requires a configured ~/.pypirc (or TWINE_* env vars).

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

PYTHON_BIN="${PYTHON_BIN:-./venv/bin/python}"

"${PYTHON_BIN}" -m pip install --upgrade build twine
rm -rf dist build *.egg-info
"${PYTHON_BIN}" -m build
"${PYTHON_BIN}" -m twine check dist/*
"${PYTHON_BIN}" -m twine upload dist/* -r pypi
SH && chmod +x /Users/jacoblsteenwyk/Desktop/GITHUB/SKYLINE/gh-skyline-python/scripts/publish_pypi.sh
