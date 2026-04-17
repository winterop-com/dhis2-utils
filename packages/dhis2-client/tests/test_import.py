"""Sanity check: every workspace member is importable."""

import dhis2_browser
import dhis2_cli
import dhis2_client
import dhis2_core
import dhis2_mcp


def test_members_importable() -> None:
    for module in (dhis2_client, dhis2_core, dhis2_cli, dhis2_mcp, dhis2_browser):
        assert module.__doc__
