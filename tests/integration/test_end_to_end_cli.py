from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from gh_skyline.cli import root


class E2EClient:
    class _Auth:
        @staticmethod
        def default_host() -> str:
            return "github.com"

    auth = _Auth()

    @staticmethod
    def get_authenticated_user() -> str:
        return "mona"

    @staticmethod
    def get_user_join_year(username: str) -> int:
        assert username == "mona"
        return 2024

    @staticmethod
    def fetch_contributions(username: str, year: int) -> dict[str, object]:
        payload = json.loads(Path("testdata/parity/graphql/contributions_mona_2024.json").read_text(encoding="utf-8"))
        payload["data"]["user"]["login"] = username
        return payload


def test_root_run_generates_stl_file(tmp_path: Path, monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr(root, "GitHubClient", E2EClient)

    out = tmp_path / "mvp-output"
    rc = root.run(
        ["--year", "2024", "--user", "mona", "--output", str(out)],
        now=datetime(2026, 2, 23, tzinfo=timezone.utc),
    )

    assert rc == 0
    stl_path = tmp_path / "mvp-output.stl"
    assert stl_path.exists()
    # Non-empty model: should include at least base geometry.
    assert stl_path.stat().st_size > 84


def test_root_run_art_only_no_stl(tmp_path: Path, monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr(root, "GitHubClient", E2EClient)

    out = tmp_path / "art-only-output"
    rc = root.run(
        ["--year", "2024", "--user", "mona", "--art-only", "--output", str(out)],
        now=datetime(2026, 2, 23, tzinfo=timezone.utc),
    )

    assert rc == 0
    assert not (tmp_path / "art-only-output.stl").exists()
