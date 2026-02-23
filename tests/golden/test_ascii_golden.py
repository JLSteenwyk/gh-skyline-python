from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from gh_skyline.ascii.generator import generate_ascii
from gh_skyline.models.types import ContributionDay


def _load_grid() -> list[list[ContributionDay]]:
    payload = json.loads(Path("testdata/parity/graphql/contributions_mona_2024.json").read_text(encoding="utf-8"))
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    grid: list[list[ContributionDay]] = []
    for week in weeks:
        days = [ContributionDay(d["contributionCount"], d["date"]) for d in week["contributionDays"]]
        grid.append(days)
    return grid


def test_ascii_matches_golden_fixture() -> None:
    art = generate_ascii(
        _load_grid(),
        username="mona",
        year=2024,
        include_header=False,
        include_user_info=True,
        now=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )

    golden = Path("testdata/parity/ascii/mona-2024.txt").read_text(encoding="utf-8")
    assert art == golden
