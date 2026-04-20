"""Service layer for the `browser` plugin — thin wrappers around `dhis2_browser`.

Imports from `dhis2-browser` (the Playwright-carrying workspace member) are
guarded so the plugin stays importable even when the optional `[browser]`
extra isn't installed. The CLI surface substitutes a stub command in that
case; every real call funnels through `require_browser()` here and raises
a clear error if the module is missing.
"""

from __future__ import annotations

from importlib.util import find_spec
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dhis2_browser import PatOptions


class BrowserExtraNotInstalled(RuntimeError):
    """Raised when a `browser` command runs without the `[browser]` extra."""


def require_browser() -> None:
    """Confirm `dhis2_browser` is importable; otherwise raise an install hint."""
    if find_spec("dhis2_browser") is None:
        raise BrowserExtraNotInstalled(
            "The `dhis2 browser` commands need the Playwright extra. "
            'Install with `uv pip install "dhis2-cli[browser]"` '
            "(or `uv pip install dhis2-browser`), then run "
            "`playwright install chromium` once to pull the driver.",
        )


async def create_pat(
    url: str,
    username: str,
    password: str,
    *,
    options: PatOptions | None = None,
    headless: bool | None = None,
) -> str:
    """Mint a DHIS2 Personal Access Token V2 via an authenticated browser session."""
    require_browser()
    from dhis2_browser import create_pat as _create_pat  # noqa: PLC0415 — optional-extra guard

    return await _create_pat(url, username, password, options=options, headless=headless)
