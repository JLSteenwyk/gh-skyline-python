"""Structured error helpers for gh_skyline."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ErrorType(StrEnum):
    """Categories of errors for consistent reporting."""

    VALIDATION = "VALIDATION"
    IO = "IO"
    NETWORK = "NETWORK"
    GRAPHQL = "GRAPHQL"
    STL = "STL"


@dataclass
class SkylineError(Exception):
    """Structured application error."""

    error_type: ErrorType
    message: str
    original_error: Exception | None = None

    def __str__(self) -> str:
        if self.original_error is not None:
            return f"[{self.error_type}] {self.message}: {self.original_error}"
        return f"[{self.error_type}] {self.message}"


def new_error(error_type: ErrorType, message: str, err: Exception | None = None) -> SkylineError:
    """Construct a SkylineError."""
    return SkylineError(error_type=error_type, message=message, original_error=err)


def wrap_error(err: Exception | None, message: str) -> Exception | None:
    """Wrap an existing error with additional context."""
    if err is None:
        return None

    if isinstance(err, SkylineError):
        return SkylineError(
            error_type=err.error_type,
            message=f"{message}: {err.message}",
            original_error=err.original_error,
        )

    return SkylineError(error_type=ErrorType.STL, message=message, original_error=err)
