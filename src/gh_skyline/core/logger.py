"""Minimal logger wrapper for CLI debug toggling."""

from __future__ import annotations

import logging


def get_logger(name: str = "gh_skyline") -> logging.Logger:
    """Get configured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel(logging.INFO)
    return logger
