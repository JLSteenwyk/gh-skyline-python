#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -x "./venv/bin/python" ]]; then
  echo "error: expected ./venv. Create it first: python3 -m venv venv" >&2
  exit 1
fi

echo "[1/3] Installing editable package..."
./venv/bin/pip install -e . >/dev/null

echo "[2/3] Checking console script..."
./venv/bin/gh-skyline --help >/dev/null

echo "[3/3] Checking module entrypoint..."
PYTHONPATH=src ./venv/bin/python -m gh_skyline --help >/dev/null

echo "package smoke test passed"
