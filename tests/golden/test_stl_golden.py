from __future__ import annotations

import struct
from pathlib import Path

from gh_skyline.stl.writer import HEADER_TEXT


def test_stl_fixture_has_valid_header_and_count() -> None:
    data = Path("testdata/parity/stl/mona-2024.stl").read_bytes()

    assert len(data) >= 84
    header = data[:80]
    triangle_count = struct.unpack("<I", data[80:84])[0]

    assert header.startswith(HEADER_TEXT.encode("utf-8"))
    assert triangle_count == 0
