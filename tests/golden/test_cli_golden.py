from __future__ import annotations

from gh_skyline.cli.root import _build_parser


def test_cli_help_matches_golden_snapshot() -> None:
    current_help = _build_parser(2026).format_help()

    with open("testdata/parity/cli/skyline-help-2026.txt", "r", encoding="utf-8") as f:
        golden = f.read()

    assert current_help == golden
