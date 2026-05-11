"""Sanity check: every workspace member is importable."""

import dhis2w_browser
import dhis2w_cli
import dhis2w_client
import dhis2w_core
import dhis2w_mcp


def test_members_importable() -> None:
    """Members importable."""
    for module in (dhis2w_client, dhis2w_core, dhis2w_cli, dhis2w_mcp, dhis2w_browser):
        assert module.__doc__
