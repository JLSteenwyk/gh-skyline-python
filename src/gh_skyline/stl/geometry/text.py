"""Text and logo geometry approximations for front-face embossing.

This module provides a deterministic, dependency-light placeholder for text/logo embossing
until full raster parity is implemented.
"""

from __future__ import annotations

from gh_skyline.stl.geometry.geometry import BASE_HEIGHT, CELL_SIZE
from gh_skyline.stl.geometry.shapes import create_cube
from gh_skyline.stl.writer import Triangle

VOXEL_DEPTH = 1.0


def _char_bitmap(ch: str) -> list[int]:
    """Generate a simple 5x7 deterministic bitmap from character code."""
    code = ord(ch)
    rows: list[int] = []
    for r in range(7):
        # 5-bit row pattern; deterministic and stable.
        pattern = ((code * (r + 3)) ^ (code >> (r % 3))) & 0b11111
        # Ensure at least one active bit in each row to avoid fully empty chars.
        if pattern == 0:
            pattern = 0b00100
        rows.append(pattern)
    return rows


def _string_to_voxels(text: str) -> list[tuple[int, int]]:
    """Convert string to sparse voxel points in a 2D bitmap plane."""
    voxels: list[tuple[int, int]] = []
    x_offset = 0
    for ch in text:
        if ch == " ":
            x_offset += 3
            continue
        bitmap = _char_bitmap(ch)
        for y, row in enumerate(bitmap):
            for bit in range(5):
                if row & (1 << (4 - bit)):
                    voxels.append((x_offset + bit, y))
        x_offset += 6
    return voxels


def _voxel_to_face_cube(
    x_px: int,
    y_px: int,
    face_width: float,
    face_height: float,
    x_scale: float,
    y_scale: float,
    x_offset: float,
    y_offset: float,
) -> list[Triangle]:
    """Map voxel coordinate to front-face cube in model coordinates."""
    x = x_offset + (x_px * x_scale)
    # Draw on front face; negative y extrudes outward like Go path.
    y = -VOXEL_DEPTH
    # Map y pixel from top-down into z coordinates on front face.
    z = -(y_offset + (y_px * y_scale))

    return create_cube(x, y, z, x_scale, VOXEL_DEPTH, y_scale)


def create_3d_text(username: str, year_text: str, base_width: float, base_height: float) -> list[Triangle]:
    """Create embossed text geometry for username and year on front face."""
    if not username:
        username = "anonymous"

    triangles: list[Triangle] = []

    # Username on left.
    uname_vox = _string_to_voxels(username)
    # Year on right.
    year_vox = _string_to_voxels(year_text)

    # Scale bitmap to roughly fit the front face.
    x_scale = max(CELL_SIZE * 0.18, base_width / 400.0)
    y_scale = max(CELL_SIZE * 0.22, base_height / 80.0)

    for x_px, y_px in uname_vox:
        triangles.extend(
            _voxel_to_face_cube(
                x_px=x_px,
                y_px=y_px,
                face_width=base_width,
                face_height=base_height,
                x_scale=x_scale,
                y_scale=y_scale,
                x_offset=base_width * 0.08,
                y_offset=base_height * 0.25,
            )
        )

    # Right align year approx by offsetting based on glyph width.
    year_width_px = max([x for x, _ in year_vox], default=0) + 1
    year_start = max(base_width * 0.62, base_width - (year_width_px * x_scale) - base_width * 0.06)
    for x_px, y_px in year_vox:
        triangles.extend(
            _voxel_to_face_cube(
                x_px=x_px,
                y_px=y_px,
                face_width=base_width,
                face_height=base_height,
                x_scale=x_scale,
                y_scale=y_scale,
                x_offset=year_start,
                y_offset=base_height * 0.25,
            )
        )

    return triangles


def generate_logo_geometry(base_width: float, base_height: float) -> list[Triangle]:
    """Create a small deterministic logo-like mark on the front face."""
    triangles: list[Triangle] = []

    # A small 10x10 pattern approximating a logo block.
    pattern = [
        "0011111100",
        "0110000110",
        "1101111011",
        "1011111101",
        "1010010101",
        "1011111101",
        "1101111011",
        "0110000110",
        "0011111100",
        "0001111000",
    ]

    x_scale = max(CELL_SIZE * 0.20, base_width / 450.0)
    y_scale = max(CELL_SIZE * 0.20, base_height / 90.0)
    x_offset = base_width * 0.03
    y_offset = base_height * 0.15

    for y, row in enumerate(pattern):
        for x, bit in enumerate(row):
            if bit == "1":
                triangles.extend(
                    _voxel_to_face_cube(
                        x_px=x,
                        y_px=y,
                        face_width=base_width,
                        face_height=base_height,
                        x_scale=x_scale,
                        y_scale=y_scale,
                        x_offset=x_offset,
                        y_offset=y_offset,
                    )
                )

    return triangles


def year_label(start_year: int, end_year: int) -> str:
    """Match Go year formatting convention used for front-face label."""
    if start_year == end_year:
        return f"{end_year}"
    return f"{start_year:04d}-{end_year % 100:02d}"
