from __future__ import annotations

import json
from pathlib import Path

import yaml

from gh_skyline.core.utils import generate_output_filename


def test_cases_matrix_references_existing_fixtures() -> None:
    cases_doc = yaml.safe_load(Path("testdata/parity/cases.yaml").read_text(encoding="utf-8"))
    cases = cases_doc["cases"]

    for case in cases:
        assert Path("testdata/parity/graphql", case["graphql_fixture"]).exists()
        assert Path("testdata/parity/ascii", case["ascii_fixture"]).exists()
        assert Path("testdata/parity/stl", case["stl_fixture"]).exists()
        assert Path("testdata/parity/cli", case["cli_fixture"]).exists()


def test_output_filename_parity_from_cases() -> None:
    cases_doc = yaml.safe_load(Path("testdata/parity/cases.yaml").read_text(encoding="utf-8"))
    cases = cases_doc["cases"]

    for case in cases:
        actual = generate_output_filename(
            user=case["user"],
            start_year=case["start_year"],
            end_year=case["end_year"],
            output=case["output"],
        )
        assert actual == case["expected_output_filename"]


def test_generated_contributions_fixture_matches_go_pattern_shape() -> None:
    payload = json.loads(Path("testdata/parity/graphql/contributions_mona_2024.json").read_text(encoding="utf-8"))

    calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = calendar["weeks"]
    assert len(weeks) == 52
    assert all(len(week["contributionDays"]) == 7 for week in weeks)
    assert isinstance(calendar["totalContributions"], int)
    assert calendar["totalContributions"] > 0
