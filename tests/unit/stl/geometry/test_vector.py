from __future__ import annotations

import math

import pytest

from gh_skyline.stl.geometry.vector import calculate_normal, normalize_vector, vector_cross, vector_subtract
from gh_skyline.stl.writer import Point3D


def test_vector_subtract() -> None:
    got = vector_subtract(Point3D(3, 2, 1), Point3D(1, 1, 1))
    assert got == Point3D(2, 1, 0)


def test_vector_cross() -> None:
    got = vector_cross(Point3D(1, 0, 0), Point3D(0, 1, 0))
    assert got == Point3D(0, 0, 1)


def test_normalize_vector() -> None:
    got = normalize_vector(Point3D(0, 3, 4))
    assert math.isclose(got.y, 0.6)
    assert math.isclose(got.z, 0.8)


def test_calculate_normal_degenerate_triangle() -> None:
    with pytest.raises(ValueError, match="degenerate triangle"):
        calculate_normal(Point3D(0, 0, 0), Point3D(1, 1, 1), Point3D(2, 2, 2))
