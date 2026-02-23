from __future__ import annotations

from gh_skyline.core.errors import ErrorType, SkylineError, new_error, wrap_error


def test_skyline_error_formatting() -> None:
    err = SkylineError(error_type=ErrorType.VALIDATION, message="bad input")
    assert str(err) == "[VALIDATION] bad input"


def test_wrap_skyline_error_keeps_type() -> None:
    source = new_error(ErrorType.NETWORK, "upstream failed")
    wrapped = wrap_error(source, "while fetching")
    assert isinstance(wrapped, SkylineError)
    assert wrapped.error_type == ErrorType.NETWORK
    assert wrapped.message == "while fetching: upstream failed"


def test_wrap_non_skyline_defaults_to_stl() -> None:
    wrapped = wrap_error(ValueError("boom"), "failed")
    assert isinstance(wrapped, SkylineError)
    assert wrapped.error_type == ErrorType.STL
