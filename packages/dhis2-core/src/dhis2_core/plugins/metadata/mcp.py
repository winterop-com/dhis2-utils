"""FastMCP tool registration for the `metadata` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_core.plugins.metadata import service
from dhis2_core.profile import profile_from_env


def register(mcp: Any) -> None:
    """Register `list_metadata_types`, `list_metadata`, `get_metadata` as MCP tools."""

    @mcp.tool()
    async def list_metadata_types() -> list[str]:
        """List every metadata resource type the connected DHIS2 instance exposes."""
        return await service.list_resource_types(profile_from_env())

    @mcp.tool()
    async def list_metadata(
        resource: str,
        fields: str = "id,name",
        filter: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List instances of a metadata resource (e.g. `dataElements`, `indicators`).

        `fields` follows DHIS2's selector syntax. `filter` is a DHIS2 filter string
        (e.g. `name:like:Malaria`). `limit` is applied client-side; defaults to 50.
        """
        return await service.list_metadata(profile_from_env(), resource, fields=fields, filter=filter, limit=limit)

    @mcp.tool()
    async def get_metadata(
        resource: str,
        uid: str,
        fields: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one metadata object by UID from the named resource."""
        return await service.get_metadata(profile_from_env(), resource, uid, fields=fields)
