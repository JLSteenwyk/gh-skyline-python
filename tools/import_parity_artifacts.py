"""Import externally generated parity artifacts into testdata/parity.

Expected source layout:
  <src>/ascii/*.txt
  <src>/stl/*.stl
  <src>/graphql/*.json
  <src>/cli/*.txt
  <src>/cases.yaml   (optional)

This workflow is toolchain-agnostic and does not require Go.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "testdata" / "parity"


def _copy_tree_if_exists(src_dir: Path, dst_dir: Path, pattern: str) -> int:
    if not src_dir.exists():
        return 0
    dst_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in src_dir.glob(pattern):
        if p.is_file():
            shutil.copy2(p, dst_dir / p.name)
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Import parity artifacts")
    parser.add_argument("src", help="Path to artifact directory")
    args = parser.parse_args()

    src_root = Path(args.src).resolve()
    if not src_root.exists():
        raise SystemExit(f"error: source path does not exist: {src_root}")

    copied = 0
    copied += _copy_tree_if_exists(src_root / "ascii", DEST / "ascii", "*.txt")
    copied += _copy_tree_if_exists(src_root / "stl", DEST / "stl", "*.stl")
    copied += _copy_tree_if_exists(src_root / "graphql", DEST / "graphql", "*.json")
    copied += _copy_tree_if_exists(src_root / "cli", DEST / "cli", "*.txt")

    cases_src = src_root / "cases.yaml"
    if cases_src.exists():
        shutil.copy2(cases_src, DEST / "cases.yaml")
        copied += 1

    print(f"import complete: copied {copied} files into {DEST}")


if __name__ == "__main__":
    main()
