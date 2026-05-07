"""FastMCP tool registration for the `route` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client import JsonPatchOp, WebMessageResponse
from dhis2_client.generated.v42.schemas import Route

from dhis2_core.plugins.route import service
from dhis2_core.plugins.route.service import RoutePayload
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
    async def route_get(route: str, fields: str | None = None, profile: str | None = None) -> Route:
        """Fetch one route by UID or code."""
        return await service.get_route(resolve_profile(profile), route, fields=fields)

    @mcp.tool()
    async def route_create(payload: RoutePayload, profile: str | None = None) -> WebMessageResponse:
        """Create a route via POST /api/routes.

        `payload` must include at minimum `code`, `name`, `url`. Optional fields:
        `auth` (headers/basic/OIDC), `headers`, `authorities`, `disabled`.
        """
        return await service.add_route(resolve_profile(profile), payload)

    @mcp.tool()
    async def route_update(route: str, payload: RoutePayload, profile: str | None = None) -> WebMessageResponse:
        """Replace a route via PUT /api/routes/{uid} (full-object semantics).

        `route` accepts the route's UID or its `code`.
        """
        return await service.update_route(resolve_profile(profile), route, payload)

    @mcp.tool()
    async def route_patch(
        route: str,
        patch: list[JsonPatchOp],
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Apply a JSON Patch (RFC 6902) to a route.

        `route` accepts the route's UID or its `code`. Each patch element is one
        `{op, path, value?, from?}` operation; the `from` JSON key maps to the
        typed `from_` alias.
        """
        return await service.patch_route(resolve_profile(profile), route, patch)

    @mcp.tool()
    async def route_delete(route: str, profile: str | None = None) -> WebMessageResponse:
        """Delete a route. `route` accepts the route's UID or its `code`."""
        return await service.delete_route(resolve_profile(profile), route)

    @mcp.tool()
    async def route_run(
        route: str,
        method: str = "GET",
        body: Any = None,
        sub_path: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Execute a route — DHIS2 proxies the request to the configured target URL.

        `route` accepts the route's UID or its `code`. `method` is GET (default),
        POST, PUT, or DELETE. `sub_path` is appended to the route's target URL —
        required when the route URL ends in a wildcard (`/**`). `body` is the
        JSON payload for POST/PUT.
        """
        return await service.run_route(
            resolve_profile(profile),
            route,
            method=method,
            body=body,
            sub_path=sub_path,
        )
