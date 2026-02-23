"""Raster-based text and logo geometry for front-face embossing."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from gh_skyline.stl.geometry.shapes import create_cube
from gh_skyline.stl.writer import Triangle

BASE_WIDTH_VOXEL_RESOLUTION = 2000
VOXEL_DEPTH = 1.0

LOGO_SCALE = 0.4
LOGO_TOP_OFFSET = 0.15
LOGO_LEFT_OFFSET = 0.03

USERNAME_FONT_SIZE = 120.0
USERNAME_JUSTIFICATION = "left"
USERNAME_LEFT_OFFSET = 0.1

YEAR_FONT_SIZE = 100.0
YEAR_JUSTIFICATION = "right"
YEAR_LEFT_OFFSET = 0.97

PRIMARY_FONT = "monasans-medium.ttf"
FALLBACK_FONT = "monasans-regular.ttf"


def _assets_dir() -> Path:
    return Path(__file__).resolve().parent / "assets"


def _font_path(font_name: str) -> Path:
    path = _assets_dir() / font_name
    if not path.exists():
        raise FileNotFoundError(f"font asset not found: {font_name}")
    return path


def _load_font(size: float) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(_font_path(PRIMARY_FONT)), int(size))
    except OSError:
        return ImageFont.truetype(str(_font_path(FALLBACK_FONT)), int(size))


def create_voxel_on_face(x: float, y: float, height: float, base_width: float, base_height: float) -> list[Triangle]:
    """Map 2D face pixel coordinate to a cube extruded from the front face."""
    x_resolution = float(BASE_WIDTH_VOXEL_RESOLUTION)
    y_resolution = x_resolution * base_height / base_width

    voxel_size = 1.0

    x_model = (x / x_resolution) * base_width
    y_model = (y / y_resolution) * base_height
    voxel_size_x = (voxel_size / x_resolution) * base_width
    voxel_size_y = (voxel_size / y_resolution) * base_height

    return create_cube(
        x_model,
        -height,
        -voxel_size_y - y_model,
        voxel_size_x,
        height,
        voxel_size_y,
    )


def _render_text(
    text: str,
    justification: str,
    left_offset_percent: float,
    font_size: float,
    base_width: float,
    base_height: float,
) -> list[Triangle]:
    face_width_res = BASE_WIDTH_VOXEL_RESOLUTION
    face_height_res = int(float(face_width_res) * base_height / base_width)

    image = Image.new("L", (face_width_res, face_height_res), 0)
    draw = ImageDraw.Draw(image)

    font = _load_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = max(1, bbox[2] - bbox[0])
    text_height = max(1, bbox[3] - bbox[1])

    x_anchor = float(face_width_res) * left_offset_percent
    if justification == "center":
        x = x_anchor - (text_width / 2.0)
    elif justification == "right":
        x = x_anchor - text_width
    else:
        x = x_anchor

    y = (float(face_height_res) * 0.5) - (text_height / 2.0)

    draw.text((x, y), text, fill=255, font=font)

    triangles: list[Triangle] = []
    px = image.load()
    for xx in range(face_width_res):
        for yy in range(face_height_res):
            if px[xx, yy] > 127:
                triangles.extend(create_voxel_on_face(float(xx), float(yy), VOXEL_DEPTH, base_width, base_height))

    return triangles


def create_3d_text(username: str, year_text: str, base_width: float, base_height: float) -> list[Triangle]:
    """Create embossed text geometry for username and year."""
    if username == "":
        username = "anonymous"

    username_triangles = _render_text(
        username,
        USERNAME_JUSTIFICATION,
        USERNAME_LEFT_OFFSET,
        USERNAME_FONT_SIZE,
        base_width,
        base_height,
    )

    year_triangles = _render_text(
        year_text,
        YEAR_JUSTIFICATION,
        YEAR_LEFT_OFFSET,
        YEAR_FONT_SIZE,
        base_width,
        base_height,
    )

    return username_triangles + year_triangles


def generate_logo_geometry(base_width: float, base_height: float) -> list[Triangle]:
    """Create front-face embossed logo geometry from embedded PNG."""
    logo_path = _assets_dir() / "invertocat.png"
    img = Image.open(logo_path).convert("RGBA")
    logo_width, logo_height = img.size
    px = img.load()

    face_width_res = BASE_WIDTH_VOXEL_RESOLUTION
    face_height_res = int(float(face_width_res) * base_height / base_width)

    triangles: list[Triangle] = []
    for x in range(logo_width):
        for y in range(logo_height - 1, -1, -1):
            r, _, _, a = px[x, y]
            if a > 128 and r > 128:
                face_x = (LOGO_LEFT_OFFSET * float(face_width_res)) + float(x) * LOGO_SCALE
                face_y = (LOGO_TOP_OFFSET * float(face_height_res)) + float(y) * LOGO_SCALE
                triangles.extend(create_voxel_on_face(face_x, face_y, VOXEL_DEPTH, base_width, base_height))

    return triangles


def year_label(start_year: int, end_year: int) -> str:
    """Match Go year formatting convention used for front-face label."""
    if start_year == end_year:
        return f"{end_year}"
    return f"{start_year:04d}-{end_year % 100:02d}"
