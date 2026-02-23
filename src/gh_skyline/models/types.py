"""Shared dataclasses for GitHub Skyline domain objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ContributionDay:
    """Single day contribution metadata."""

    contribution_count: int
    date: str

    def is_after(self, dt: datetime) -> bool:
        """Match Go's date parsing behavior for future-day detection."""
        try:
            value = datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            return False
        return value.date() > dt.date()
