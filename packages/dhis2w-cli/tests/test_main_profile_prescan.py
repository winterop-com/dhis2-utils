"""Regression tests for the argv pre-scan that applies --profile before plugin discovery."""

from __future__ import annotations

from dhis2w_cli.main import _extract_profile_from_argv


def test_returns_none_for_empty_argv() -> None:
    """Returns none for empty argv."""
    assert _extract_profile_from_argv([]) is None


def test_returns_none_when_no_profile_flag() -> None:
    """Returns none when no profile flag."""
    assert _extract_profile_from_argv(["system", "info"]) is None


def test_long_form_space_separated() -> None:
    """Long form space separated."""
    assert _extract_profile_from_argv(["--profile", "v43p", "system", "info"]) == "v43p"


def test_long_form_equals_separated() -> None:
    """Long form equals separated."""
    assert _extract_profile_from_argv(["--profile=v43p", "system", "info"]) == "v43p"


def test_short_form() -> None:
    """Short form."""
    assert _extract_profile_from_argv(["-p", "v43p", "system", "info"]) == "v43p"


def test_flag_after_subcommand() -> None:
    """Flag after subcommand."""
    assert _extract_profile_from_argv(["system", "info", "--profile", "v43p"]) == "v43p"


def test_double_dash_stops_scanning() -> None:
    """Double dash stops scanning."""
    assert _extract_profile_from_argv(["--", "--profile", "v43p"]) is None


def test_long_form_without_value_returns_none() -> None:
    """Long form without value returns none."""
    assert _extract_profile_from_argv(["--profile"]) is None


def test_short_form_without_value_returns_none() -> None:
    """Short form without value returns none."""
    assert _extract_profile_from_argv(["-p"]) is None
