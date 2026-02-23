"""Skyline command orchestration."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timezone

from gh_skyline.ascii.generator import generate_ascii, trim_subsequent_year_ascii
from gh_skyline.core.utils import generate_output_filename
from gh_skyline.github.client import GitHubClient
from gh_skyline.models.types import ContributionDay
from gh_skyline.stl.generator import generate_stl_range


def _payload_to_grid(payload: dict[str, object]) -> list[list[ContributionDay]]:
    weeks = (
        payload.get("data", {})
        .get("user", {})
        .get("contributionsCollection", {})
        .get("contributionCalendar", {})
        .get("weeks", [])
    )

    grid: list[list[ContributionDay]] = []
    for week in weeks:
        week_days: list[ContributionDay] = []
        for day in week.get("contributionDays", []):
            week_days.append(
                ContributionDay(
                    contribution_count=int(day.get("contributionCount", 0)),
                    date=str(day.get("date", "")),
                )
            )
        grid.append(week_days)
    return grid


def generate_skyline(
    start_year: int,
    end_year: int,
    target_user: str,
    full: bool,
    output: str,
    art_only: bool,
    *,
    now: datetime | None = None,
    client: GitHubClient | None = None,
    print_fn: Callable[[str], None] = print,
) -> int:
    """Generate skyline flow with ASCII output and placeholder STL write path."""
    effective_now = now or datetime.now(timezone.utc)
    gh = client or GitHubClient()

    resolved_user = target_user
    if not resolved_user:
        resolved_user = gh.get_authenticated_user()

    if full:
        start_year = gh.get_user_join_year(resolved_user)
        end_year = effective_now.year

    rendered_chunks: list[str] = []
    all_contributions: list[list[list[ContributionDay]]] = []

    for year in range(start_year, end_year + 1):
        payload = gh.fetch_contributions(resolved_user, year)
        grid = _payload_to_grid(payload)
        all_contributions.append(grid)

        ascii_art = generate_ascii(
            grid,
            username=resolved_user,
            year=year,
            include_header=(year == start_year) and (not art_only),
            include_user_info=not art_only,
            now=effective_now,
        )

        if year == start_year:
            rendered_chunks.append(ascii_art.rstrip("\n"))
        else:
            rendered_chunks.append(trim_subsequent_year_ascii(ascii_art))

    if rendered_chunks:
        print_fn("\n".join(rendered_chunks))

    if not art_only:
        output_path = generate_output_filename(resolved_user, start_year, end_year, output)
        generate_stl_range(all_contributions, output_path, resolved_user, start_year, end_year)

    return 0
