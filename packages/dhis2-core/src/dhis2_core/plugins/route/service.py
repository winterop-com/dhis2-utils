"""Service layer for the `route` plugin — DHIS2 /api/routes.

Read paths (`list_routes`, `get_route`) return the generated v42 `Route`
pydantic model. Write paths and `run_route` return raw `dict[str, Any]`:
`add`/`update`/`patch`/`delete` because DHIS2 wraps them in a
WebMessageResponse envelope that's not modelled yet, and `run` because the
response shape is whatever the upstream API returns (opaque proxy).
"""

from __future__ import annotations

from typing import Any

from dhis2_client.generated.v42.schemas import Route
from pydantic import BaseModel, ConfigDict

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


class _RoutesEnvelope(BaseModel):
    """Transient model for the `{"pager": ..., "routes": [...]}` envelope from /api/routes."""

    model_config = ConfigDict(extra="allow")

    routes: list[Route] = []


async def list_routes(profile: Profile, *, fields: str = "id,code,name,url,disabled") -> list[Route]:
    """List registered routes from GET /api/routes."""
    async with open_client(profile) as client:
        envelope = await client.get("/api/routes", model=_RoutesEnvelope, params={"fields": fields})
    return envelope.routes


async def get_route(profile: Profile, uid: str, *, fields: str | None = None) -> Route:
    """Fetch one route by UID from GET /api/routes/{uid}."""
    params = {"fields": fields} if fields else None
    async with open_client(profile) as client:
        return await client.get(f"/api/routes/{uid}", model=Route, params=params)


async def add_route(profile: Profile, payload: dict[str, Any]) -> dict[str, Any]:
    """Create a route via POST /api/routes.

    `payload` must include at least `code`, `name`, `url`. Additional fields:
    `auth` (headers/basic/OIDC), `headers`, `authorities`, `disabled`. Returns
    DHIS2's raw WebMessageResponse envelope `{httpStatus, status, response: {uid, ...}}`.
    """
    async with open_client(profile) as client:
        return await client.post_raw("/api/routes", payload)


async def update_route(profile: Profile, uid: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Replace a route via PUT /api/routes/{uid}.

    For partial updates use `patch_route`. DHIS2 expects the full object on PUT.
    """
    async with open_client(profile) as client:
        return await client.put_raw(f"/api/routes/{uid}", payload)


async def patch_route(profile: Profile, uid: str, patch: list[dict[str, Any]]) -> dict[str, Any]:
    """Partial update via PATCH /api/routes/{uid} (JSON Patch, RFC 6902)."""
    async with open_client(profile) as client:
        return await client.patch_raw(f"/api/routes/{uid}", patch)


async def delete_route(profile: Profile, uid: str) -> dict[str, Any]:
    """Delete a route via DELETE /api/routes/{uid}."""
    async with open_client(profile) as client:
        return await client.delete_raw(f"/api/routes/{uid}")


async def run_route(
    profile: Profile,
    uid: str,
    *,
    method: str = "GET",
    body: Any = None,
    sub_path: str | None = None,
) -> dict[str, Any]:
    """Execute a route via `{method} /api/routes/{uid}/run[/{sub_path}]`.

    DHIS2 proxies the call to the route's configured target URL, injecting
    whatever auth is configured on the route. `sub_path` is appended to the
    target URL when the route was registered with a wildcard suffix.
    """
    path = f"/api/routes/{uid}/run"
    if sub_path:
        path = f"{path}/{sub_path.lstrip('/')}"
    async with open_client(profile) as client:
        if method.upper() == "GET":
            return await client.get_raw(path)
        if method.upper() == "POST":
            return await client.post_raw(path, body)
        if method.upper() == "PUT":
            return await client.put_raw(path, body)
        if method.upper() == "DELETE":
            return await client.delete_raw(path)
        raise ValueError(f"unsupported method {method!r}; use GET/POST/PUT/DELETE")
