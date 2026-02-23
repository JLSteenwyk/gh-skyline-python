from __future__ import annotations

import json
from pathlib import Path

import pytest

from gh_skyline.core.errors import SkylineError
from gh_skyline.github.client import GitHubClient


class FixtureAuthAdapter:
    def __init__(self, fixtures_dir: Path) -> None:
        self.fixtures_dir = fixtures_dir
        self.calls: list[tuple[str, dict[str, object] | None]] = []

    def graphql(self, query: str, variables: dict[str, object] | None = None) -> dict[str, object]:
        self.calls.append((query, variables))

        if "viewer" in query:
            name = "viewer_mona.json"
        elif "UserJoinDate" in query:
            name = "user_join_year_mona.json"
        elif "ContributionGraph" in query:
            name = "contributions_mona_2024.json"
        else:
            raise AssertionError("Unknown query")

        return json.loads((self.fixtures_dir / name).read_text(encoding="utf-8"))


def _fixtures_dir() -> Path:
    return Path("testdata/parity/graphql")


def test_get_authenticated_user_from_fixture() -> None:
    auth = FixtureAuthAdapter(_fixtures_dir())
    client = GitHubClient(auth)

    assert client.get_authenticated_user() == "mona"
    assert "viewer" in auth.calls[0][0]


def test_get_user_join_year_from_fixture() -> None:
    auth = FixtureAuthAdapter(_fixtures_dir())
    client = GitHubClient(auth)

    assert client.get_user_join_year("mona") == 2011
    assert auth.calls[0][1] == {"username": "mona"}


def test_fetch_contributions_contract_from_fixture() -> None:
    auth = FixtureAuthAdapter(_fixtures_dir())
    client = GitHubClient(auth)

    payload = client.fetch_contributions("mona", 2024)

    user = payload["data"]["user"]
    assert user["login"] == "mona"
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    assert len(weeks) == 52
    assert len(weeks[0]["contributionDays"]) == 7

    _, vars_used = auth.calls[0]
    assert vars_used == {
        "username": "mona",
        "from": "2024-01-01T00:00:00Z",
        "to": "2024-12-31T23:59:59Z",
    }


def test_fetch_contributions_validation_errors() -> None:
    auth = FixtureAuthAdapter(_fixtures_dir())
    client = GitHubClient(auth)

    with pytest.raises(SkylineError, match="username cannot be empty"):
        client.fetch_contributions("", 2024)

    with pytest.raises(SkylineError, match="year cannot be before GitHub's launch"):
        client.fetch_contributions("mona", 2007)
