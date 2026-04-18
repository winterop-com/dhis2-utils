"""FastMCP tool registration for the `metadata` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_core.plugins.metadata import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `metadata_type_list`, `metadata_list`, `metadata_get` as MCP tools."""

    @mcp.tool()
    async def metadata_type_list(profile: str | None = None) -> list[str]:
        """List every metadata resource type the connected DHIS2 instance exposes.

        Pass `profile` to target a named profile; omit to use the default.
        """
        return await service.list_resource_types(resolve_profile(profile))

    @mcp.tool()
    async def metadata_list(
        resource: str,
        fields: str = "id,name",
        filters: list[str] | None = None,
        root_junction: str | None = None,
        order: list[str] | None = None,
        page: int | None = None,
        page_size: int | None = None,
        paging: bool | None = None,
        translate: bool | None = None,
        locale: str | None = None,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List instances of a metadata resource (e.g. `dataElements`, `indicators`).

        Every DHIS2 `/api/<resource>` query parameter is exposed:

        - `fields`: DHIS2 selector. Supports plain lists (`id,name`), presets
          (`:identifiable`, `:nameable`, `:owner`, `:all`), exclusions
          (`:all,!lastUpdated`), and nested selectors (`children[id,name]`).
        - `filters`: list of `property:operator:value` strings. Multiple filters
          default to AND; pass `root_junction="OR"` to OR them.
        - `order`: list of `property:asc|desc` clauses (later ones tie-break).
        - `page` + `page_size`: server-side pagination.
        - `paging=False`: return every row in one response.
        - `translate` + `locale`: return localised fields.

        `profile` selects a named profile; omit for the default.
        """
        return await service.list_metadata(
            resolve_profile(profile),
            resource,
            fields=fields,
            filters=filters,
            root_junction=root_junction,
            order=order,
            page=page,
            page_size=page_size,
            paging=paging,
            translate=translate,
            locale=locale,
        )

    @mcp.tool()
    async def metadata_get(
        resource: str,
        uid: str,
        fields: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one metadata object by UID from the named resource."""
        return await service.get_metadata(resolve_profile(profile), resource, uid, fields=fields)
