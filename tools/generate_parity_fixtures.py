"""Generate deterministic parity fixtures for gh-skyline-python."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gh_skyline.ascii.generator import generate_ascii  # noqa: E402
from gh_skyline.models.types import ContributionDay  # noqa: E402
from gh_skyline.stl.generator import generate_stl_range  # noqa: E402

PARITY = ROOT / "testdata" / "parity"


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _load_contrib_fixture(username: str, year: int) -> dict[str, object]:
    path = PARITY / "graphql" / f"contributions_{username}_{year}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _payload_to_grid(payload: dict[str, object]) -> list[list[ContributionDay]]:
    weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    grid: list[list[ContributionDay]] = []
    for week in weeks:
        grid.append([ContributionDay(d["contributionCount"], d["date"]) for d in week["contributionDays"]])
    return grid


def generate_viewer_fixture(username: str = "mona") -> None:
    payload = {"data": {"viewer": {"login": username}}}
    _write_json(PARITY / "graphql" / f"viewer_{username}.json", payload)


def generate_join_year_fixture(username: str = "mona", join_year: int = 2011) -> None:
    payload = {"data": {"user": {"createdAt": f"{join_year}-10-04T00:00:00Z"}}}
    _write_json(PARITY / "graphql" / f"user_join_year_{username}.json", payload)


def generate_contributions_fixture(username: str, year: int) -> None:
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
            days.append({"contributionCount": count, "date": dt.strftime("%Y-%m-%d")})
        weeks.append({"contributionDays": days})

    payload = {
        "data": {
            "user": {
                "login": username,
                "contributionsCollection": {
                    "contributionCalendar": {"totalContributions": total, "weeks": weeks}
                },
            }
        }
    }
    _write_json(PARITY / "graphql" / f"contributions_{username}_{year}.json", payload)


def generate_ascii_fixture(username: str, year: int, now_year: int) -> None:
    payload = _load_contrib_fixture(username, year)
    grid = _payload_to_grid(payload)
    art = generate_ascii(
        grid,
        username=username,
        year=year,
        include_header=False,
        include_user_info=True,
        now=datetime(now_year, 1, 1, tzinfo=UTC),
    )
    (PARITY / "ascii" / f"{username}-{year}.txt").write_text(art, encoding="utf-8")


def generate_stl_fixture_single_year(username: str, year: int) -> None:
    payload = _load_contrib_fixture(username, year)
    grid = _payload_to_grid(payload)
    out = PARITY / "stl" / f"{username}-{year}.stl"
    generate_stl_range([grid], str(out), username, year, year)


def generate_stl_fixture_year_range(username: str, start_year: int, end_year: int) -> None:
    grids: list[list[list[ContributionDay]]] = []
    for year in range(start_year, end_year + 1):
        payload = _load_contrib_fixture(username, year)
        grids.append(_payload_to_grid(payload))

    out = PARITY / "stl" / f"{username}-{start_year}-{end_year % 100:02d}.stl"
    generate_stl_range(grids, str(out), username, start_year, end_year)


def generate_cases_yaml(username: str = "mona") -> None:
    cases = {
        "cases": [
            {
                "id": f"{username}_2024_art_only",
                "user": username,
                "year": "2024",
                "start_year": 2024,
                "end_year": 2024,
                "full": False,
                "art_only": True,
                "output": "",
                "expected_output_filename": f"{username}-2024-github-skyline.stl",
                "graphql_fixture": f"viewer_{username}.json",
                "ascii_fixture": f"{username}-2024.txt",
                "stl_fixture": f"{username}-2024.stl",
                "cli_fixture": "skyline-help-2026.txt",
            },
            {
                "id": f"{username}_2024_single",
                "user": username,
                "year": "2024",
                "start_year": 2024,
                "end_year": 2024,
                "full": False,
                "art_only": False,
                "output": "",
                "expected_output_filename": f"{username}-2024-github-skyline.stl",
                "graphql_fixture": f"contributions_{username}_2024.json",
                "ascii_fixture": f"{username}-2024.txt",
                "stl_fixture": f"{username}-2024.stl",
                "cli_fixture": "skyline-help-2026.txt",
            },
            {
                "id": f"{username}_2020_2024_range",
                "user": username,
                "year": "2020-2024",
                "start_year": 2020,
                "end_year": 2024,
                "full": False,
                "art_only": False,
                "output": "",
                "expected_output_filename": f"{username}-2020-24-github-skyline.stl",
                "graphql_fixture": f"contributions_{username}_2020.json",
                "ascii_fixture": f"{username}-2024.txt",
                "stl_fixture": f"{username}-2020-24.stl",
                "cli_fixture": "skyline-help-2026.txt",
            },
        ]
    }

    import yaml  # local import to keep runtime deps lean

    (PARITY / "cases.yaml").write_text(yaml.safe_dump(cases, sort_keys=False), encoding="utf-8")


def main() -> None:
    (PARITY / "graphql").mkdir(parents=True, exist_ok=True)
    (PARITY / "ascii").mkdir(parents=True, exist_ok=True)
    (PARITY / "stl").mkdir(parents=True, exist_ok=True)

    username = "mona"
    years = [2020, 2021, 2022, 2023, 2024]

    generate_viewer_fixture(username)
    generate_join_year_fixture(username, join_year=2011)

    for year in years:
        generate_contributions_fixture(username, year)

    generate_ascii_fixture(username, 2024, now_year=2025)
    generate_stl_fixture_single_year(username, 2024)
    generate_stl_fixture_year_range(username, 2020, 2024)
    generate_cases_yaml(username)


if __name__ == "__main__":
    main()
