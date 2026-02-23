from __future__ import annotations

from datetime import datetime, timezone

import pytest

from gh_skyline.core.utils import YearRangeError, format_year_range, generate_output_filename, parse_year_range


def test_parse_single_year() -> None:
    start, end = parse_year_range("2024", now=datetime(2026, 1, 1, tzinfo=timezone.utc))
    assert (start, end) == (2024, 2024)


def test_parse_year_range() -> None:
    start, end = parse_year_range("2014-2024", now=datetime(2026, 1, 1, tzinfo=timezone.utc))
    assert (start, end) == (2014, 2024)


def test_parse_invalid_range_format() -> None:
    with pytest.raises(YearRangeError):
        parse_year_range("2014-2024-2025", now=datetime(2026, 1, 1, tzinfo=timezone.utc))


def test_parse_range_bounds() -> None:
    with pytest.raises(YearRangeError, match="years must be between"):
        parse_year_range("2007", now=datetime(2026, 1, 1, tzinfo=timezone.utc))


def test_format_year_range() -> None:
    assert format_year_range(2020, 2024) == "2020-24"


def test_generate_output_filename_default() -> None:
    assert generate_output_filename("mona", 2020, 2024, "") == "mona-2020-24-github-skyline.stl"


def test_generate_output_filename_suffix() -> None:
    assert generate_output_filename("mona", 2020, 2024, "my-skyline") == "my-skyline.stl"
    assert generate_output_filename("mona", 2020, 2024, "my-skyline.STL") == "my-skyline.STL"
