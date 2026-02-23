"""STL model generation orchestration."""

from __future__ import annotations

from gh_skyline.models.types import ContributionDay
from gh_skyline.stl.geometry.geometry import calculate_multi_year_dimensions, create_contribution_geometry
from gh_skyline.stl.geometry.shapes import create_cuboid_base
from gh_skyline.stl.writer import Triangle, write_stl_binary


def _find_max_contributions(contributions: list[list[ContributionDay]]) -> int:
    max_count = 0
    for week in contributions:
        for day in week:
            if day.contribution_count > max_count:
                max_count = day.contribution_count
    return max_count


def _find_max_contributions_across_years(contributions_per_year: list[list[list[ContributionDay]]]) -> int:
    max_count = 0
    for year in contributions_per_year:
        year_max = _find_max_contributions(year)
        if year_max > max_count:
            max_count = year_max
    return max_count


def _generate_model_geometry(
    contributions_per_year: list[list[list[ContributionDay]]],
) -> list[Triangle]:
    if not contributions_per_year:
        raise ValueError("contributions data cannot be empty")

    width, depth = calculate_multi_year_dimensions(len(contributions_per_year))
    max_contrib = _find_max_contributions_across_years(contributions_per_year)

    triangles: list[Triangle] = []

    # Deterministic component ordering: base then columns.
    triangles.extend(create_cuboid_base(width, depth))

    for i in range(len(contributions_per_year) - 1, -1, -1):
        year_offset = len(contributions_per_year) - 1 - i
        triangles.extend(create_contribution_geometry(contributions_per_year[i], year_offset, max_contrib))

    return triangles


def generate_stl(
    contributions: list[list[ContributionDay]],
    output_path: str,
    username: str,
    year: int,
) -> None:
    generate_stl_range([contributions], output_path, username, year, year)


def generate_stl_range(
    contributions_per_year: list[list[list[ContributionDay]]],
    output_path: str,
    username: str,
    start_year: int,
    end_year: int,
) -> None:
    if not contributions_per_year:
        raise ValueError("contributions data cannot be empty")
    if not output_path:
        raise ValueError("output path cannot be empty")
    if not username:
        raise ValueError("username cannot be empty")

    triangles = _generate_model_geometry(contributions_per_year)
    write_stl_binary(output_path, triangles)
