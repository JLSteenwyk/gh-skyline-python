from __future__ import annotations

from datetime import datetime, timezone

from gh_skyline.models.types import ContributionDay


def test_contribution_day_is_after() -> None:
    day = ContributionDay(1, "2026-02-24")
    assert day.is_after(datetime(2026, 2, 23, tzinfo=timezone.utc))


def test_contribution_day_invalid_date_returns_false() -> None:
    day = ContributionDay(1, "not-a-date")
    assert not day.is_after(datetime(2026, 2, 23, tzinfo=timezone.utc))
