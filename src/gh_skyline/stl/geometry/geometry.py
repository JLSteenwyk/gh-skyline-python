"""Core geometry constants and contribution normalization."""

from __future__ import annotations

import math

from gh_skyline.models.types import ContributionDay
from gh_skyline.stl.geometry.shapes import create_column
from gh_skyline.stl.writer import Triangle

BASE_HEIGHT = 10.0
MAX_HEIGHT = 25.0
CELL_SIZE = 2.5
GRID_SIZE = 53
MIN_HEIGHT = CELL_SIZE
YEAR_SPACING = 0.0
YEAR_OFFSET = 7.0 * CELL_SIZE


def normalize_contribution(count: int, max_count: int) -> float:
    """Normalize contribution count to column height."""
    if count == 0:
        return 0.0
    if max_count <= 0:
        return MIN_HEIGHT

    height_range = MAX_HEIGHT - MIN_HEIGHT
    normalized = math.sqrt(float(count)) / math.sqrt(float(max_count))
    return MIN_HEIGHT + (normalized * height_range)


def calculate_multi_year_dimensions(year_count: int) -> tuple[float, float]:
    width = float(GRID_SIZE) * CELL_SIZE + 4 * CELL_SIZE
    depth = float(7 * year_count) * CELL_SIZE + 4 * CELL_SIZE
    return width, depth


def create_contribution_geometry(
    contributions: list[list[ContributionDay]],
    year_index: int,
    max_contrib: int,
) -> list[Triangle]:
    """Generate cuboid columns for contribution grid."""
    triangles: list[Triangle] = []
    base_y_offset = 2 * CELL_SIZE + float(year_index) * 7 * CELL_SIZE

    for week_idx, week in enumerate(contributions):
        for day_idx, day in enumerate(week):
            if day.contribution_count > 0:
                height = normalize_contribution(day.contribution_count, max_contrib)
                x = 2 * CELL_SIZE + float(week_idx) * CELL_SIZE
                y = base_y_offset + float(day_idx) * CELL_SIZE
                triangles.extend(create_column(x, y, height, CELL_SIZE))

    return triangles
