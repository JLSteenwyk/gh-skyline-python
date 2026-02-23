"""Test config for src-layout imports and fixture bootstrap."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def pytest_sessionstart(session) -> None:  # noqa: ANN001
    """Ensure parity fixtures exist for CI/test environments."""
    required = [
        ROOT / "testdata/parity/cases.yaml",
        ROOT / "testdata/parity/stl/mona-2024.stl",
        ROOT / "testdata/parity/stl/mona-2020-24.stl",
    ]
    if all(path.exists() for path in required):
        return

    subprocess.run(
        [sys.executable, str(ROOT / "tools/generate_parity_fixtures.py")],
        cwd=str(ROOT),
        check=True,
    )
