"""FastMCP tool registration for the `route` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client import WebMessageResponse
from dhis2_client.generated.v42.schemas import Route

from dhis2_core.plugins.route import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `route_*` tools on the MCP server."""

    @mcp.tool()
    async def route_list(
        fields: str = "id,code,name,url,disabled",
        profile: str | None = None,
    ) -> list[Route]:
        """List DHIS2 integration routes (GET /api/routes)."""
        return await service.list_routes(resolve_profile(profile), fields=fields)

    @mcp.tool()
    async def route_get(uid: str, fields: str | None = None, profile: str | None = None) -> Route:
        """Fetch one route by UID."""
        return await service.get_route(resolve_profile(profile), uid, fields=fields)

    @mcp.tool()
    async def route_add(payload: dict[str, Any], profile: str | None = None) -> WebMessageResponse:
        """Create a route via POST /api/routes.

        `payload` must include at minimum `code`, `name`, `url`. Optional fields:
        `auth` (headers/basic/OIDC), `headers`, `authorities`, `disabled`.
        """
        return await service.add_route(resolve_profile(profile), payload)

    @mcp.tool()
    async def route_update(uid: str, payload: dict[str, Any], profile: str | None = None) -> WebMessageResponse:
        """Replace a route via PUT /api/routes/{uid} (full-object semantics)."""
        return await service.update_route(resolve_profile(profile), uid, payload)

    @mcp.tool()
    async def route_patch(uid: str, patch: list[dict[str, Any]], profile: str | None = None) -> WebMessageResponse:
        """Apply a JSON Patch (RFC 6902) to a route."""
        return await service.patch_route(resolve_profile(profile), uid, patch)

    @mcp.tool()
    async def route_delete(uid: str, profile: str | None = None) -> WebMessageResponse:
        """Delete a route."""
        return await service.delete_route(resolve_profile(profile), uid)

    @mcp.tool()
    async def route_run(
        uid: str,
        method: str = "GET",
        body: Any = None,
        sub_path: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Execute a route — DHIS2 proxies the request to the configured target URL.

        `method` is GET (default), POST, PUT, or DELETE. `sub_path` is appended
        to the route's target URL, useful when the route was registered with a
        wildcard suffix. `body` is the JSON payload for POST/PUT.
        """
        return await service.run_route(
            resolve_profile(profile),
            uid,
            method=method,
            body=body,
            sub_path=sub_path,
        )
