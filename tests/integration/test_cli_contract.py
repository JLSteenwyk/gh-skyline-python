from __future__ import annotations

from datetime import datetime, timezone

import pytest

from gh_skyline.cli import root


class DummyClient:
    class _Auth:
        @staticmethod
        def default_host() -> str:
            return "github.com"

    auth = _Auth()

    @staticmethod
    def get_authenticated_user() -> str:
        return "mona"


def test_cli_default_year_calls_generate(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_generate(**kwargs: object) -> int:
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(root, "GitHubClient", DummyClient)
    monkeypatch.setattr(root, "generate_skyline", fake_generate)

    rc = root.run([], now=datetime(2026, 2, 23, tzinfo=timezone.utc))

    assert rc == 0
    assert captured["start_year"] == 2026
    assert captured["end_year"] == 2026
    assert captured["target_user"] == ""


def test_cli_invalid_year_has_go_style_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(root, "GitHubClient", DummyClient)

    with pytest.raises(ValueError, match="^invalid year range:"):
        root.run(["--year", "2026-2024"], now=datetime(2026, 2, 23, tzinfo=timezone.utc))


def test_cli_web_uses_authenticated_user(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[str] = []

    class BrowserClient(DummyClient):
        pass

    monkeypatch.setattr(root, "GitHubClient", BrowserClient)
    monkeypatch.setattr(root.webbrowser, "open", lambda url: opened.append(url) or True)

    rc = root.run(["--web"], now=datetime(2026, 2, 23, tzinfo=timezone.utc))

    assert rc == 0
    assert opened == ["https://github.com/mona"]
