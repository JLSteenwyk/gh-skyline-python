from __future__ import annotations

import json
from pathlib import Path

import yaml

from gh_skyline.core.utils import generate_output_filename


def _load_cases() -> list[dict[str, object]]:
    cases_doc = yaml.safe_load(Path("testdata/parity/cases.yaml").read_text(encoding="utf-8"))
    return cases_doc["cases"]


def test_cases_matrix_references_existing_fixtures() -> None:
    cases = _load_cases()

    for case in cases:
        assert Path("testdata/parity/graphql", str(case["graphql_fixture"])).exists()
        assert Path("testdata/parity/ascii", str(case["ascii_fixture"])).exists()
        assert Path("testdata/parity/stl", str(case["stl_fixture"])).exists()
        assert Path("testdata/parity/cli", str(case["cli_fixture"])).exists()


def test_output_filename_parity_from_cases() -> None:
    cases = _load_cases()

    for case in cases:
        actual = generate_output_filename(
            user=str(case["user"]),
            start_year=int(case["start_year"]),
            end_year=int(case["end_year"]),
            output=str(case["output"]),
        )
        assert actual == str(case["expected_output_filename"])


def test_generated_contributions_fixture_matches_go_pattern_shape() -> None:
    # Validate multiple yearly fixtures exist and each has expected week/day shape.
    for year in (2020, 2021, 2022, 2023, 2024):
        payload = json.loads(
            Path(f"testdata/parity/graphql/contributions_mona_{year}.json").read_text(encoding="utf-8")
        )
        calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        weeks = calendar["weeks"]
        assert len(weeks) == 52
        assert all(len(week["contributionDays"]) == 7 for week in weeks)
        assert isinstance(calendar["totalContributions"], int)
        assert calendar["totalContributions"] > 0
