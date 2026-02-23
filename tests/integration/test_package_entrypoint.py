from __future__ import annotations

import subprocess


def test_console_script_help_works() -> None:
    proc = subprocess.run(
        ["./venv/bin/gh-skyline", "--help"],
        cwd=".",
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "Generate a 3D model" in proc.stdout


def test_module_entrypoint_help_works() -> None:
    proc = subprocess.run(
        ["./venv/bin/python", "-m", "gh_skyline", "--help"],
        cwd=".",
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "--year" in proc.stdout
    assert "--full" in proc.stdout
