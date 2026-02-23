"""ASCII block character mapping and thresholds."""

from __future__ import annotations

EMPTY_BLOCK = " "
FUTURE_BLOCK = "."

FOUNDATION_LOW = "░"
FOUNDATION_MED = "▒"
FOUNDATION_HIGH = "▓"

MIDDLE_LOW = "░"
MIDDLE_MED = "▒"
MIDDLE_HIGH = "▓"

TOP_LOW = "╻"
TOP_MED = "┃"
TOP_HIGH = "╽"

LOW_THRESHOLD = 0.33
MEDIUM_THRESHOLD = 0.66


_BLOCK_SETS = {
    "foundation": (FOUNDATION_LOW, FOUNDATION_MED, FOUNDATION_HIGH),
    "middle": (MIDDLE_LOW, MIDDLE_MED, MIDDLE_HIGH),
    "top": (TOP_LOW, TOP_MED, TOP_HIGH),
}


def _block_type(normalized: float) -> int:
    if normalized < LOW_THRESHOLD:
        return 0
    if normalized < MEDIUM_THRESHOLD:
        return 1
    return 2


def get_block(normalized: float, day_idx: int, non_zero_count: int) -> str:
    """Determine display block for normalized contribution at column position."""
    if normalized == 0:
        return EMPTY_BLOCK

    block_type = _block_type(normalized)

    if non_zero_count == 1:
        return _BLOCK_SETS["foundation"][block_type]

    if day_idx == non_zero_count - 1:
        return _BLOCK_SETS["top"][block_type]
    if day_idx == 0:
        return _BLOCK_SETS["foundation"][block_type]
    return _BLOCK_SETS["middle"][block_type]
