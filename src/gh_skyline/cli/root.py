"""Root CLI command and flag parity with Go cmd/root.go."""

from __future__ import annotations

import argparse
import webbrowser
from collections.abc import Callable
from datetime import datetime, timezone

from gh_skyline.cli.skyline import generate_skyline
from gh_skyline.core.logger import get_logger
from gh_skyline.core.utils import YearRangeError, parse_year_range
from gh_skyline.github.client import GitHubClient


def _build_parser(now_year: int) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skyline",
        description="Generate a 3D model of a user's GitHub contribution history",
    )
    parser.add_argument(
        "-y",
        "--year",
        default=str(now_year),
        help="Year or year range (e.g., 2024 or 2014-2024)",
    )
    parser.add_argument(
        "-u",
        "--user",
        default="",
        help="GitHub username (optional, defaults to authenticated user)",
    )
    parser.add_argument(
        "-f",
        "--full",
        action="store_true",
        help="Generate contribution graph from join year to current year",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "-w",
        "--web",
        action="store_true",
        help="Open GitHub profile (authenticated or specified user).",
    )
    parser.add_argument(
        "-a",
        "--art-only",
        action="store_true",
        help="Generate only ASCII preview",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="",
        help="Output file path (optional)",
    )
    return parser


def open_github_profile(
    target_user: str,
    client: GitHubClient,
    browser_open: Callable[[str], bool] | None = None,
) -> int:
    """Open GitHub profile for explicit or authenticated user."""
    resolved_user = target_user or client.get_authenticated_user()
    host = client.auth.default_host()
    url = f"https://{host}/{resolved_user}"
    opener = browser_open or webbrowser.open
    opener(url)
    return 0


def run(argv: list[str] | None = None, *, now: datetime | None = None) -> int:
    """Execute root CLI flow."""
    effective_now = now or datetime.now(timezone.utc)
    parser = _build_parser(effective_now.year)
    args = parser.parse_args(argv)

    logger = get_logger()
    if args.debug:
        logger.setLevel("DEBUG")
        logger.debug("Debug logging enabled")

    client = GitHubClient()

    if args.web:
        return open_github_profile(args.user, client)

    try:
        start_year, end_year = parse_year_range(args.year, now=effective_now)
    except YearRangeError as exc:
        raise ValueError(f"invalid year range: {exc}") from exc

    return generate_skyline(
        start_year=start_year,
        end_year=end_year,
        target_user=args.user,
        full=args.full,
        output=args.output,
        art_only=args.art_only,
        now=effective_now,
        client=client,
    )


def main(argv: list[str] | None = None) -> int:
    return run(argv)
