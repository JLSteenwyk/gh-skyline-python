from __future__ import annotations

from gh_skyline.cli.root import _build_parser


def test_cli_help_contains_required_contract_lines() -> None:
    """Argparse formatting varies by Python version; assert contract, not spacing."""
    help_text = _build_parser(2026).format_help()
    normalized_help = " ".join(help_text.split())

    required_flag_snippets = [
        "usage: skyline",
        "-y",
        "--year",
        "-u",
        "--user",
        "-f",
        "--full",
        "-d",
        "--debug",
        "-w",
        "--web",
        "-a",
        "--art-only",
        "-o",
        "--output",
    ]
    required_description_snippets = [
        "Generate a 3D model of a user's GitHub contribution history",
        "Year or year range (e.g., 2024 or 2014-2024)",
        "GitHub username (optional, defaults to authenticated user)",
        "Generate contribution graph from join year to current year",
        "Enable debug logging",
        "Open GitHub profile (authenticated or specified user).",
        "Generate only ASCII preview",
        "Output file path (optional)",
    ]

    for snippet in required_flag_snippets:
        assert snippet in help_text
    for snippet in required_description_snippets:
        assert snippet in normalized_help
