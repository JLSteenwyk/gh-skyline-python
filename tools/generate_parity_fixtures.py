"""Generate deterministic parity fixtures for gh-skyline-python."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARITY = ROOT / "testdata" / "parity"


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def generate_viewer_fixture() -> None:
    payload = {"data": {"viewer": {"login": "mona"}}}
    _write_json(PARITY / "graphql" / "viewer_mona.json", payload)


def generate_join_year_fixture() -> None:
    payload = {"data": {"user": {"createdAt": "2011-10-04T00:00:00Z"}}}
    _write_json(PARITY / "graphql" / "user_join_year_mona.json", payload)


def generate_contributions_fixture(username: str = "mona", year: int = 2024) -> None:
    # Mirrors gh-skyline/internal/testutil/fixtures/github.go generation pattern.
    start = datetime(year, 1, 1, tzinfo=UTC)
    weeks: list[dict[str, object]] = []
    total = 0

    for week_idx in range(52):
        days: list[dict[str, object]] = []
        for day_idx in range(7):
            count = (week_idx + day_idx) % 10
            total += count
            dt = start + timedelta(days=week_idx * 7 + day_idx)
            days.append(
                {
                    "contributionCount": count,
                    "date": dt.strftime("%Y-%m-%d"),
                }
            )
        weeks.append({"contributionDays": days})

    payload = {
        "data": {
            "user": {
                "login": username,
                "contributionsCollection": {
                    "contributionCalendar": {
                        "totalContributions": total,
                        "weeks": weeks,
                    }
                },
            }
        }
    }
    _write_json(PARITY / "graphql" / "contributions_mona_2024.json", payload)


def main() -> None:
    (PARITY / "graphql").mkdir(parents=True, exist_ok=True)
    generate_viewer_fixture()
    generate_join_year_fixture()
    generate_contributions_fixture()


if __name__ == "__main__":
    main()
