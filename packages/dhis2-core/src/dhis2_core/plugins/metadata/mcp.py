"""FastMCP tool registration for the `metadata` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_core.plugins.metadata import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `list_metadata_types`, `list_metadata`, `get_metadata` as MCP tools."""

    @mcp.tool()
    async def list_metadata_types(profile: str | None = None) -> list[str]:
        """List every metadata resource type the connected DHIS2 instance exposes.

        Pass `profile` to target a named profile; omit to use the default.
        """
        return await service.list_resource_types(resolve_profile(profile))

    @mcp.tool()
    async def list_metadata(
        resource: str,
        fields: str = "id,name",
        filter: str | None = None,
        limit: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List instances of a metadata resource (e.g. `dataElements`, `indicators`).

        `fields` follows DHIS2's selector syntax. `filter` is a DHIS2 filter string
        (e.g. `name:like:Malaria`). `limit` is applied client-side; defaults to 50.
        `profile` selects a named profile; omit for the default.
        """
        return await service.list_metadata(
            resolve_profile(profile), resource, fields=fields, filter=filter, limit=limit
        )

    @mcp.tool()
    async def get_metadata(
        resource: str,
        uid: str,
        fields: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one metadata object by UID from the named resource."""
        return await service.get_metadata(resolve_profile(profile), resource, uid, fields=fields)
