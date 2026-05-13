"""Regression test: _enable_debug_logging() is idempotent across repeated calls.

CliRunner reuses the same Python process across `invoke()` calls, and
`make docs-cli`'s typer-docs sweep imports `main` repeatedly. Adding a
fresh RichHandler each time would accumulate duplicate stderr lines for
every HTTP request. The handler is tagged with a stable name; a second
call to `_enable_debug_logging()` finds it and returns.
"""

from __future__ import annotations

import logging

import pytest
from dhis2w_cli.main import _DEBUG_HANDLER_NAME, _enable_debug_logging


@pytest.fixture(autouse=True)
def _reset_root_handlers() -> object:
    """Strip any debug handlers we added so this test doesn't leak into other tests."""
    yield None
    root = logging.getLogger()
    for handler in list(root.handlers):
        if getattr(handler, "name", None) == _DEBUG_HANDLER_NAME:
            root.removeHandler(handler)


def test_first_call_installs_one_handler() -> None:
    """First call installs one handler."""
    root = logging.getLogger()
    before = sum(1 for h in root.handlers if getattr(h, "name", None) == _DEBUG_HANDLER_NAME)
    _enable_debug_logging()
    after = sum(1 for h in root.handlers if getattr(h, "name", None) == _DEBUG_HANDLER_NAME)
    assert after - before == 1


def test_repeated_calls_do_not_duplicate_handlers() -> None:
    """Repeated calls do not duplicate handlers."""
    root = logging.getLogger()
    _enable_debug_logging()
    _enable_debug_logging()
    _enable_debug_logging()
    matching = [h for h in root.handlers if getattr(h, "name", None) == _DEBUG_HANDLER_NAME]
    assert len(matching) == 1
