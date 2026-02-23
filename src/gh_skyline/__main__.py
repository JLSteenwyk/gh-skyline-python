"""CLI entrypoint for gh-skyline."""

from __future__ import annotations

import sys

from gh_skyline.cli.root import main as cli_main


def main() -> int:
    """Entrypoint exposed by project script."""
    try:
        return cli_main()
    except Exception as exc:  # pragma: no cover - integration behavior
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
