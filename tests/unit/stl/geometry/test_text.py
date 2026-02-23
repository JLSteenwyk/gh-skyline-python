from __future__ import annotations

from gh_skyline.stl.geometry.text import create_3d_text, generate_logo_geometry, year_label


def test_year_label_single_year() -> None:
    assert year_label(2024, 2024) == "2024"


def test_year_label_range() -> None:
    assert year_label(2020, 2024) == "2020-24"


def test_create_3d_text_non_empty() -> None:
    tris = create_3d_text("mona", "2024", 140.0, 10.0)
    assert len(tris) > 0


def test_generate_logo_geometry_non_empty() -> None:
    tris = generate_logo_geometry(140.0, 10.0)
    assert len(tris) > 0
