from __future__ import annotations

from pathlib import Path

from gh_skyline.models.types import ContributionDay
from gh_skyline.stl.generator import generate_stl_range


def _small_grid() -> list[list[ContributionDay]]:
    week = [
        ContributionDay(0, "2024-01-01"),
        ContributionDay(1, "2024-01-02"),
        ContributionDay(0, "2024-01-03"),
        ContributionDay(2, "2024-01-04"),
        ContributionDay(0, "2024-01-05"),
        ContributionDay(0, "2024-01-06"),
        ContributionDay(1, "2024-01-07"),
    ]
    return [week]


def test_generate_stl_range_writes_file(tmp_path: Path) -> None:
    out = tmp_path / "model.stl"
    generate_stl_range([_small_grid()], str(out), "mona", 2024, 2024)
    assert out.exists()
    assert out.stat().st_size > 84


def test_generate_stl_range_text_logo_increase_size(tmp_path: Path) -> None:
    out = tmp_path / "model.stl"
    generate_stl_range([_small_grid()], str(out), "mona", 2024, 2024)
    # Ensure file size reflects more than tiny minimal geometry.
    assert out.stat().st_size > 5000
