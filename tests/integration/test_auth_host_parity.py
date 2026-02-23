from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from gh_skyline.core.errors import SkylineError
from gh_skyline.github.auth import GhAuthAdapter


class _Proc:
    def __init__(self, stdout: str) -> None:
        self.stdout = stdout


def test_default_host_parses_first_host(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {"hosts": {"github.example.com": {}, "github.com": {}}}

    def fake_run(cmd, capture_output, text, check):  # noqa: ANN001
        assert cmd[:3] == ["gh", "auth", "status"]
        return _Proc(stdout=json.dumps(payload))

    monkeypatch.setattr(shutil, "which", lambda _: "/usr/local/bin/gh")
    monkeypatch.setattr(subprocess, "run", fake_run)
    adapter = GhAuthAdapter()

    assert adapter.default_host() == "github.example.com"


def test_graphql_invokes_gh_api_with_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[list[str]] = []

    def fake_run(cmd, capture_output, text, check):  # noqa: ANN001
        seen.append(cmd)
        return _Proc(stdout='{"data":{"viewer":{"login":"mona"}}}')

    monkeypatch.setattr(shutil, "which", lambda _: "/usr/local/bin/gh")
    monkeypatch.setattr(subprocess, "run", fake_run)
    adapter = GhAuthAdapter()

    payload = adapter.graphql("query { viewer { login } }", {"username": "mona"})

    assert payload["data"]["viewer"]["login"] == "mona"
    flat = " ".join(seen[0])
    assert "api graphql" in flat
    assert "query=query { viewer { login } }" in flat
    assert "username=mona" in flat


def test_auth_token_errors_without_gh_or_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(shutil, "which", lambda _: None)
    adapter = GhAuthAdapter()

    with pytest.raises(SkylineError, match="gh CLI not found"):
        adapter.auth_token()
