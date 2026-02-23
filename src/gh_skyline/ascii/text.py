"""ASCII text formatting helpers."""

from __future__ import annotations

GRID_WIDTH = 53

HEADER_TEMPLATE = r"""
           ____ _ _   _   _       _     
          / ___(_) |_| | | |_   _| |__  
         | |  _| | __| |_| | | | | '_ \ 
         | |_| | | |_|  _  | |_| | |_) |
          \____|_|\__|_| |_|\__,_|_.__/ 

          ____  _          _ _            
         / ___|| | ___   _| (_)_ __   ___ 
         \___ \| |/ / | | | | | '_ \ / _ \
          ___) |   <| |_| | | | | | | __/
         |____/|_|\_\\__, |_|_|_| |_|\___|
                    |___/
"""


def center_text(text: str) -> str:
    """Center text using Go-style width handling."""
    visual_width = len(text)

    if visual_width >= GRID_WIDTH:
        return text[:GRID_WIDTH] + "\n"

    total_padding = GRID_WIDTH - visual_width
    if total_padding <= 1:
        return text + "\n"

    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    return (" " * left_padding) + text + (" " * right_padding) + "\n"
