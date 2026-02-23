"""Utility helpers that mirror Go year/output filename behavior."""

from __future__ import annotations

from datetime import datetime, timezone

GITHUB_LAUNCH_YEAR = 2008


class YearRangeError(ValueError):
    """Raised when year range input is invalid."""


def parse_year_range(year_range: str, *, now: datetime | None = None) -> tuple[int, int]:
    """Parse either a single year or range 'YYYY-YYYY'."""
    current_year = (now or datetime.now(timezone.utc)).year

    if "-" in year_range:
        parts = year_range.split("-")
        if len(parts) != 2:
            raise YearRangeError("invalid year range format")
        try:
            start_year = int(parts[0])
            end_year = int(parts[1])
        except ValueError as exc:
            raise YearRangeError(str(exc)) from exc
    else:
        try:
            year = int(year_range)
        except ValueError as exc:
            raise YearRangeError(str(exc)) from exc
        start_year, end_year = year, year

    _validate_year_range(start_year, end_year, current_year=current_year)
    return start_year, end_year


def _validate_year_range(start_year: int, end_year: int, *, current_year: int) -> None:
    if start_year < GITHUB_LAUNCH_YEAR or end_year > current_year:
        raise YearRangeError(f"years must be between {GITHUB_LAUNCH_YEAR} and {current_year}")
    if start_year > end_year:
        raise YearRangeError("start year cannot be after end year")


def format_year_range(start_year: int, end_year: int) -> str:
    """Format year range like Go: single year or YYYY-YY."""
    if start_year == end_year:
        return f"{start_year}"
    return f"{start_year:04d}-{end_year % 100:02d}"


def generate_output_filename(user: str, start_year: int, end_year: int, output: str) -> str:
    """Generate output filename like Go behavior."""
    if output:
        return output if output.lower().endswith(".stl") else f"{output}.stl"

    year_str = format_year_range(start_year, end_year)
    return f"{user}-{year_str}-github-skyline.stl"
