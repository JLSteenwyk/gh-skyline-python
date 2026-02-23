"""Shape primitives that generate triangle meshes."""

from __future__ import annotations

from gh_skyline.stl.geometry.vector import calculate_normal
from gh_skyline.stl.writer import Point3D, Triangle


def create_quad(v1: Point3D, v2: Point3D, v3: Point3D, v4: Point3D) -> list[Triangle]:
    normal = calculate_normal(v1, v2, v3)
    return [
        Triangle(normal=normal, v1=v1, v2=v2, v3=v3),
        Triangle(normal=normal, v1=v1, v2=v3, v3=v4),
    ]


def _create_box(x: float, y: float, z: float, width: float, height: float, depth: float) -> list[Triangle]:
    if width < 0 or height < 0 or depth < 0:
        raise ValueError("negative dimensions not allowed")

    vertices = [
        Point3D(x, y, z),
        Point3D(x + width, y, z),
        Point3D(x + width, y + height, z),
        Point3D(x, y + height, z),
        Point3D(x, y, z + depth),
        Point3D(x + width, y, z + depth),
        Point3D(x + width, y + height, z + depth),
        Point3D(x, y + height, z + depth),
    ]

    quads = [
        (0, 3, 2, 1),
        (5, 6, 7, 4),
        (4, 7, 3, 0),
        (1, 2, 6, 5),
        (3, 7, 6, 2),
        (4, 0, 1, 5),
    ]

    triangles: list[Triangle] = []
    for a, b, c, d in quads:
        triangles.extend(create_quad(vertices[a], vertices[b], vertices[c], vertices[d]))
    return triangles


def create_cube(x: float, y: float, z: float, width: float, height: float, depth: float) -> list[Triangle]:
    return _create_box(x, y, z, width, height, depth)


def create_cuboid_base(width: float, depth: float, base_height: float = 10.0) -> list[Triangle]:
    return _create_box(0.0, 0.0, -base_height, width, depth, base_height)


def create_column(x: float, y: float, height: float, size: float) -> list[Triangle]:
    return _create_box(x, y, 0.0, size, size, height)
