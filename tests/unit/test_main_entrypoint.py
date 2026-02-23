from __future__ import annotations

from gh_skyline import __main__


def test_main_returns_cli_code(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setattr(__main__, "cli_main", lambda: 0)
    assert __main__.main() == 0


def test_main_handles_exception(monkeypatch, capsys) -> None:  # noqa: ANN001
    def boom() -> int:
        raise RuntimeError("bad")

    monkeypatch.setattr(__main__, "cli_main", boom)
    assert __main__.main() == 1
    err = capsys.readouterr().err
    assert "Error: bad" in err
