from __future__ import annotations

import struct
from pathlib import Path

from gh_skyline.stl.writer import HEADER_TEXT, Point3D, Triangle, write_stl_binary


def test_write_stl_zero_triangles(tmp_path: Path) -> None:
    out = tmp_path / "zero.stl"
    write_stl_binary(out, [])

    data = out.read_bytes()
    assert len(data) == 84
    assert data[:80].startswith(HEADER_TEXT.encode("utf-8"))
    assert struct.unpack("<I", data[80:84])[0] == 0


def test_write_stl_one_triangle_size(tmp_path: Path) -> None:
    out = tmp_path / "one.stl"
    tri = Triangle(
        normal=Point3D(0.0, 0.0, 1.0),
        v1=Point3D(0.0, 0.0, 0.0),
        v2=Point3D(1.0, 0.0, 0.0),
        v3=Point3D(0.0, 1.0, 0.0),
    )

    write_stl_binary(out, [tri])

    data = out.read_bytes()
    assert len(data) == 84 + 50
    assert struct.unpack("<I", data[80:84])[0] == 1
