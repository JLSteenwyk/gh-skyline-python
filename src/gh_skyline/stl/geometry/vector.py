"""Vector operations used for triangle normal generation."""

from __future__ import annotations

import math

from gh_skyline.stl.writer import Point3D


EPSILON = 1e-10


def vector_subtract(a: Point3D, b: Point3D) -> Point3D:
    return Point3D(a.x - b.x, a.y - b.y, a.z - b.z)


def vector_cross(u: Point3D, v: Point3D) -> Point3D:
    return Point3D(
        u.y * v.z - u.z * v.y,
        u.z * v.x - u.x * v.z,
        u.x * v.y - u.y * v.x,
    )


def is_zero_vector(v: Point3D) -> bool:
    return abs(v.x) < EPSILON and abs(v.y) < EPSILON and abs(v.z) < EPSILON


def normalize_vector(v: Point3D) -> Point3D:
    length = math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
    if length > 0:
        return Point3D(v.x / length, v.y / length, v.z / length)
    return v


def calculate_normal(p1: Point3D, p2: Point3D, p3: Point3D) -> Point3D:
    u = vector_subtract(p2, p1)
    v = vector_subtract(p3, p1)
    normal = vector_cross(u, v)
    if is_zero_vector(normal):
        raise ValueError("degenerate triangle")
    return normalize_vector(normal)
