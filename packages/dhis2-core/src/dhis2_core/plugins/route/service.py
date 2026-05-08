"""Service layer for the `route` plugin — DHIS2 /api/routes.

Read paths return the generated v42 `Route` pydantic model.
Write paths (`add`/`update`/`patch`/`delete`) return a typed
`WebMessageResponse` envelope — callers pull the created UID via
`.created_uid` and the error list via `.response` / `.object_report()`.
`run_route` stays `dict[str, Any]` because its shape is whatever the
upstream API returns (opaque proxy — the explicit carveout).

Every command accepts a "route reference" — either a DHIS2 UID
(`E8OPcc45A22`) or a route code (`chap`). Codes are resolved via
`/api/routes?filter=code:eq:<code>` before the actual operation runs;
UID-shaped refs skip the lookup. `run_route` also pre-fetches the route's
target URL so it can refuse a missing `--path` against a wildcard
(`/**`) URL with an actionable message instead of a bare upstream 404.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from dhis2_client import JsonPatchOp, WebMessageResponse
from dhis2_client.auth_schemes import AuthScheme
from dhis2_client.generated.v42.schemas import Route
from pydantic import BaseModel, ConfigDict

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile

if TYPE_CHECKING:
    from dhis2_client import Dhis2Client


_UID_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9]{10}$")


def _looks_like_uid(value: str) -> bool:
    """Return True when `value` matches DHIS2's 11-char UID shape."""
    return bool(_UID_RE.match(value))


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


async def _fetch_route(client: Dhis2Client, route_ref: str, *, fields: str | None = None) -> Route:
    """Fetch a route by UID or code; codes resolve via `/api/routes?filter=code:eq:`.

    On the code branch, DHIS2's `/api/routes` defaults to a stripped projection
    (id-only), so when the caller didn't specify fields we ask for `*` to match
    what `/api/routes/{uid}` returns by default on the UID branch.
    """
    if _looks_like_uid(route_ref):
        params = {"fields": fields} if fields else None
        return await client.get(f"/api/routes/{route_ref}", model=Route, params=params)
    list_params: dict[str, str] = {
        "filter": f"code:eq:{route_ref}",
        "fields": fields or "*",
    }
    envelope = await client.get("/api/routes", model=_RoutesEnvelope, params=list_params)
    if not envelope.routes:
        raise LookupError(f"no route found with code or UID {route_ref!r}")
    if len(envelope.routes) > 1:
        raise LookupError(f"multiple routes match code {route_ref!r} ({len(envelope.routes)} hits)")
    return envelope.routes[0]


async def _resolve_route_uid(client: Dhis2Client, route_ref: str) -> str:
    """Resolve a UID-or-code to a UID; UID-shaped refs skip the round trip."""
    if _looks_like_uid(route_ref):
        return route_ref
    route = await _fetch_route(client, route_ref, fields="id")
    if not route.id:
        raise LookupError(f"route lookup for {route_ref!r} returned no id")
    return route.id


async def get_route(profile: Profile, route_ref: str, *, fields: str | None = None) -> Route:
    """Fetch one route by UID or code from GET /api/routes/{uid}."""
    async with open_client(profile) as client:
        return await _fetch_route(client, route_ref, fields=fields)


async def add_route(profile: Profile, payload: RoutePayload) -> WebMessageResponse:
    """Create a route via POST /api/routes.

    `payload` must include at least `code`, `name`, `url`. Returns the typed
    WebMessageResponse — use `.created_uid` for the new object's UID.
    """
    async with open_client(profile) as client:
        return await client.post(
            "/api/routes",
            payload.model_dump(exclude_none=True, mode="json"),
            model=WebMessageResponse,
        )


async def update_route(profile: Profile, route_ref: str, payload: RoutePayload) -> WebMessageResponse:
    """Replace a route via PUT /api/routes/{uid}.

    For partial updates use `patch_route`. DHIS2 expects the full object on PUT.
    """
    async with open_client(profile) as client:
        uid = await _resolve_route_uid(client, route_ref)
        return await client.put(
            f"/api/routes/{uid}",
            payload.model_dump(exclude_none=True, mode="json"),
            model=WebMessageResponse,
        )


async def patch_route(profile: Profile, route_ref: str, patch: list[JsonPatchOp]) -> WebMessageResponse:
    """Partial update via PATCH /api/routes/{uid} (JSON Patch, RFC 6902)."""
    body = [op.model_dump(exclude_none=True, by_alias=True, mode="json") for op in patch]
    async with open_client(profile) as client:
        uid = await _resolve_route_uid(client, route_ref)
        return await client.patch(f"/api/routes/{uid}", body, model=WebMessageResponse)


async def delete_route(profile: Profile, route_ref: str) -> WebMessageResponse:
    """Delete a route via DELETE /api/routes/{uid}."""
    async with open_client(profile) as client:
        uid = await _resolve_route_uid(client, route_ref)
        return await client.delete(f"/api/routes/{uid}", model=WebMessageResponse)


async def run_route(
    profile: Profile,
    route_ref: str,
    *,
    method: str = "GET",
    body: Any = None,
    sub_path: str | None = None,
) -> dict[str, Any]:
    """Execute a route via `{method} /api/routes/{uid}/run[/{sub_path}]`.

    `route_ref` accepts either the route's DHIS2 UID or its `code`. Codes
    resolve via the `/api/routes?filter=code:eq:` index before the run.

    Pre-fetches the route's `url` to fail fast when a wildcard (`/**`) URL
    is invoked without `sub_path` — DHIS2 would otherwise pass the bare
    base URL to the upstream and surface whatever the upstream root says
    (often a bare 404). Callers see an actionable error pointing at
    `--path` instead.

    Return type stays `dict[str, Any]` — the payload is whatever the
    upstream (non-DHIS2) service returns, so no stable model fits.
    """
    async with open_client(profile) as client:
        route = await _fetch_route(client, route_ref, fields="id,url")
        if not route.id:
            raise LookupError(f"route lookup for {route_ref!r} returned no id")
        target_url = route.url or ""
        if sub_path is None and "**" in target_url:
            raise LookupError(
                f"route {route_ref!r} has a wildcard URL ({target_url!r}); "
                "pass --path SEGMENT to fill the wildcard suffix"
            )
        path = f"/api/routes/{route.id}/run"
        if sub_path:
            path = f"{path}/{sub_path.lstrip('/')}"
        if method.upper() == "GET":
            return await client.get_raw(path)
        if method.upper() == "POST":
            return await client.post_raw(path, body)
        if method.upper() == "PUT":
            return await client.put_raw(path, body)
        if method.upper() == "DELETE":
            return await client.delete_raw(path)
        raise ValueError(f"unsupported method {method!r}; use GET/POST/PUT/DELETE")
