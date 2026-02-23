"""ASCII generation from contribution grids."""

from __future__ import annotations

from datetime import datetime

from gh_skyline.ascii.block import EMPTY_BLOCK, FOUNDATION_LOW, FUTURE_BLOCK, get_block
from gh_skyline.ascii.text import HEADER_TEMPLATE, center_text
from gh_skyline.models.types import ContributionDay


def sort_contribution_days(week: list[ContributionDay], now: datetime) -> tuple[list[ContributionDay], int]:
    """Sort week to match Go order: non-zero, zero, then future days."""
    non_zero: list[ContributionDay] = []
    zero: list[ContributionDay] = []
    future: list[ContributionDay] = []

    for day in week:
        if day.is_after(now):
            future.append(ContributionDay(contribution_count=-1, date=day.date))
        elif day.contribution_count > 0:
            non_zero.append(day)
        else:
            zero.append(day)

    sorted_days = non_zero + zero + future
    while len(sorted_days) < 7:
        sorted_days.append(ContributionDay(contribution_count=0, date=""))

    return sorted_days[:7], len(non_zero)


def generate_ascii(
    contribution_grid: list[list[ContributionDay]],
    username: str,
    year: int,
    *,
    include_header: bool,
    include_user_info: bool,
    now: datetime,
) -> str:
    """Generate ASCII skyline output for a contribution grid."""
    if len(contribution_grid) == 0:
        raise ValueError("invalid contribution grid")

    max_contributions = 0
    for week in contribution_grid:
        for day in week:
            if day.contribution_count > max_contributions:
                max_contributions = day.contribution_count

    cols = len(contribution_grid)
    ascii_grid = [[EMPTY_BLOCK for _ in range(cols)] for _ in range(7)]

    for week_idx, week in enumerate(contribution_grid):
        sorted_days, non_zero_count = sort_contribution_days(week, now)
        for day_idx in range(min(7, len(sorted_days))):
            day = sorted_days[day_idx]
            if day.contribution_count == -1:
                ascii_grid[day_idx][week_idx] = FUTURE_BLOCK
            else:
                normalized = 0.0
                if max_contributions != 0:
                    normalized = float(day.contribution_count) / float(max_contributions)
                ascii_grid[day_idx][week_idx] = get_block(normalized, day_idx, non_zero_count)

    lines: list[str] = []

    if include_header:
        lines.extend(HEADER_TEMPLATE.splitlines())
        lines.append("")

    for row_idx in range(6, -1, -1):
        lines.append("".join(ascii_grid[row_idx]))

    if include_user_info:
        lines.append("")
        lines.append(center_text(username).rstrip("\n"))
        lines.append(center_text(f"{year}").rstrip("\n"))

    return "\n".join(lines) + "\n"


def trim_subsequent_year_ascii(ascii_art: str) -> str:
    """Match Go behavior for multi-year output after first year."""
    lines = ascii_art.splitlines()
    grid_start = 0
    for i, line in enumerate(lines):
        contains_empty_block = EMPTY_BLOCK in line
        contains_foundation_low = FOUNDATION_LOW in line
        is_not_only_empty_blocks = line.strip(EMPTY_BLOCK) != ""
        if (contains_empty_block or contains_foundation_low) and is_not_only_empty_blocks:
            grid_start = i
            break
    return "\n".join(lines[grid_start:]).rstrip("\n")
