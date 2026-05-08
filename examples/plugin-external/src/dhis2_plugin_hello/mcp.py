"""FastMCP tool registration — `hello_say`."""

from __future__ import annotations

from typing import Any

from dhis2w_core.profile import resolve_profile

from dhis2_plugin_hello import service


def register(mcp: Any) -> None:
    """Register `hello_say` — called by dhis2-core's plugin loader."""

    @mcp.tool()
    async def hello_say(greeting: str = "Hello", profile: str | None = None) -> str:
        """Greet the authenticated user by their displayName.

        Calls `/api/me` and returns `"{greeting}, {name}!"`.
        """
        return await service.greet(resolve_profile(profile), greeting=greeting)
