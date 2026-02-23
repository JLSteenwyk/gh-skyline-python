from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from gh_skyline.cli.skyline import generate_skyline


class FixtureClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def get_authenticated_user(self) -> str:
        self.calls.append(("get_authenticated_user", None))
        return "mona"

    def get_user_join_year(self, username: str) -> int:
        self.calls.append(("get_user_join_year", username))
        return 2023

    def fetch_contributions(self, username: str, year: int) -> dict[str, object]:
        self.calls.append(("fetch_contributions", (username, year)))
        payload = json.loads(Path("testdata/parity/graphql/contributions_mona_2024.json").read_text(encoding="utf-8"))
        payload["data"]["user"]["login"] = username
        return payload


def test_generate_skyline_art_only_does_not_write_stl() -> None:
    outputs: list[str] = []
    client = FixtureClient()

    rc = generate_skyline(
        start_year=2024,
        end_year=2024,
        target_user="mona",
        full=False,
        output="",
        art_only=True,
        now=datetime(2025, 1, 1, tzinfo=timezone.utc),
        client=client,
        print_fn=outputs.append,
    )

    assert rc == 0
    assert len(outputs) == 1
    assert "mona" not in outputs[0]  # include_user_info=False for art-only parity
    assert ("fetch_contributions", ("mona", 2024)) in client.calls


def test_generate_skyline_full_uses_join_year_and_writes_output(tmp_path: Path) -> None:
    outputs: list[str] = []
    client = FixtureClient()
    out = tmp_path / "skyline-output"

    rc = generate_skyline(
        start_year=2026,
        end_year=2026,
        target_user="",
        full=True,
        output=str(out),
        art_only=False,
        now=datetime(2026, 2, 23, tzinfo=timezone.utc),
        client=client,
        print_fn=outputs.append,
    )

    assert rc == 0
    assert len(outputs) == 1
    assert ("get_authenticated_user", None) in client.calls
    assert ("get_user_join_year", "mona") in client.calls
    # years 2023..2026 expected
    fetch_years = [args[1][1] for args in client.calls if args[0] == "fetch_contributions"]
    assert fetch_years == [2023, 2024, 2025, 2026]
    assert (tmp_path / "skyline-output.stl").exists()
