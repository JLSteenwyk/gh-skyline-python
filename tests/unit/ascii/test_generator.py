from __future__ import annotations

from datetime import datetime, timezone

from gh_skyline.ascii.generator import generate_ascii, sort_contribution_days
from gh_skyline.models.types import ContributionDay


def _sample_week() -> list[ContributionDay]:
    return [
        ContributionDay(0, "2024-01-01"),
        ContributionDay(2, "2024-01-02"),
        ContributionDay(3, "2099-01-03"),
        ContributionDay(1, "2024-01-04"),
        ContributionDay(0, "2024-01-05"),
        ContributionDay(0, "2024-01-06"),
        ContributionDay(0, "2024-01-07"),
    ]


def test_sort_contribution_days_order() -> None:
    sorted_days, non_zero_count = sort_contribution_days(_sample_week(), datetime(2026, 1, 1, tzinfo=timezone.utc))

    assert non_zero_count == 2
    assert [d.contribution_count for d in sorted_days[:3]] == [2, 1, 0]
    assert sorted_days[-1].contribution_count == -1


def test_generate_ascii_basic_shape() -> None:
    grid = [_sample_week(), _sample_week()]
    art = generate_ascii(
        grid,
        username="mona",
        year=2024,
        include_header=False,
        include_user_info=True,
        now=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    lines = art.splitlines()
    assert len(lines) >= 9
    assert "mona" in art


def test_generate_ascii_with_header() -> None:
    grid = [_sample_week()]
    art = generate_ascii(
        grid,
        username="mona",
        year=2024,
        include_header=True,
        include_user_info=False,
        now=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    assert "____ _ _   _   _" in art
    assert "|___/" in art
