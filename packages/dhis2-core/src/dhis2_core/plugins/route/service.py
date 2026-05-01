"""Service layer for the `route` plugin — DHIS2 /api/routes.

Read paths return the generated v42 `Route` pydantic model.
Write paths (`add`/`update`/`patch`/`delete`) return a typed
`WebMessageResponse` envelope — callers pull the created UID via
`.created_uid` and the error list via `.response` / `.object_report()`.
`run_route` stays `dict[str, Any]` because its shape is whatever the
upstream API returns (opaque proxy — the explicit carveout).
"""

from __future__ import annotations

from typing import Any

from dhis2_client.auth_schemes import AuthScheme
from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.schemas import Route
from dhis2_client.json_patch import JsonPatchOp
from pydantic import BaseModel, ConfigDict

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


class _RoutesEnvelope(BaseModel):
    """Transient model for the `{"pager": ..., "routes": [...]}` envelope from /api/routes."""

    model_config = ConfigDict(extra="allow")

    routes: list[Route] = []


class RoutePayload(BaseModel):
    """Typed body for `POST /api/routes` + `PUT /api/routes/{uid}`.

    DHIS2 accepts (and requires on create) at least `code`, `name`, `url`.
    `extra="allow"` preserves anything else the server cares about that
    isn't explicitly typed here.

    `auth` is the discriminated `AuthScheme` union — one of five typed
    variants keyed on `type`. The codegen `spec_patches` module
    synthesises the Jackson discriminator that upstream DHIS2 omits
    (BUGS.md #14), so this field is fully typed end-to-end. Callers
    either build a concrete variant directly (e.g.
    `HttpBasicAuthScheme(username=..., password=...)`) or pass a raw
    dict with a `type` key and pydantic routes it to the right subclass.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str | None = None
    name: str | None = None
    url: str | None = None
    description: str | None = None
    disabled: bool | None = None
    authorities: list[str] | None = None
    headers: dict[str, str] | None = None
    responseTimeoutSeconds: int | None = None
    auth: AuthScheme | None = None


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


async def add_route(profile: Profile, payload: RoutePayload) -> WebMessageResponse:
    """Create a route via POST /api/routes.

    `payload` must include at least `code`, `name`, `url`. Returns the typed
    WebMessageResponse — use `.created_uid` for the new object's UID.
    """
    async with open_client(profile) as client:
        raw = await client.post_raw("/api/routes", payload.model_dump(exclude_none=True, mode="json"))
    return WebMessageResponse.model_validate(raw)


async def update_route(profile: Profile, uid: str, payload: RoutePayload) -> WebMessageResponse:
    """Replace a route via PUT /api/routes/{uid}.

    For partial updates use `patch_route`. DHIS2 expects the full object on PUT.
    """
    async with open_client(profile) as client:
        raw = await client.put_raw(f"/api/routes/{uid}", payload.model_dump(exclude_none=True, mode="json"))
    return WebMessageResponse.model_validate(raw)


async def patch_route(profile: Profile, uid: str, patch: list[JsonPatchOp]) -> WebMessageResponse:
    """Partial update via PATCH /api/routes/{uid} (JSON Patch, RFC 6902)."""
    body = [op.model_dump(exclude_none=True, by_alias=True, mode="json") for op in patch]
    async with open_client(profile) as client:
        raw = await client.patch_raw(f"/api/routes/{uid}", body)
    return WebMessageResponse.model_validate(raw)


async def delete_route(profile: Profile, uid: str) -> WebMessageResponse:
    """Delete a route via DELETE /api/routes/{uid}."""
    async with open_client(profile) as client:
        raw = await client.delete_raw(f"/api/routes/{uid}")
    return WebMessageResponse.model_validate(raw)


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

    Return type stays `dict[str, Any]` — the payload is whatever the
    upstream (non-DHIS2) service returns, so no stable model fits.
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
