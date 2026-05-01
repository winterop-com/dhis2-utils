# Route plugin

`dhis2 route` covers DHIS2's `/api/routes` integration-route surface — a
generic reverse-proxy that lets DHIS2 forward an authenticated CLI / app
request to an external service, injecting upstream auth on the way out.
Routes turn DHIS2 into a credential broker for downstream APIs.

```
dhis2 route {list,get,create,update,patch,delete,run}
```

MCP mirrors every command as `route_list`, `route_get`, `route_create`,
`route_update`, `route_patch`, `route_delete`, `route_run`.

## What a route is

A route is a stored configuration: a target URL, an `AuthScheme`, optional
custom headers, and authority gates. Once registered, callers hit
`/api/routes/<uid>/run[/<sub_path>]` and DHIS2 proxies the call to the
target with the configured auth applied. Useful when:

- A frontend app shouldn't see upstream credentials directly.
- A workflow needs to fan out to a third-party API while staying inside
  DHIS2's auth + audit boundary.
- Multiple environments (staging / prod) point at different upstream
  hosts, switched by re-registering the route — callers stay constant.

## Auth schemes

The single non-trivial bit of typing in this plugin. `auth` on a route is
a discriminated union of six variants keyed on `type`:

| `type` | Carries | When |
| --- | --- | --- |
| `none` | nothing | Open upstream — DHIS2 forwards as-is. |
| `http-basic` | `username` + `password` | Classic `Authorization: Basic <b64>`. |
| `api-token` | `token` | DHIS2-specific `Authorization: ApiToken <token>` (NOT standard `Bearer` — see BUGS.md #4e). |
| `api-headers` | `headers: dict[str, str]` | Arbitrary custom headers (e.g. `X-Api-Key`). |
| `api-query-params` | `queryParams: dict[str, str]` | Auth via URL query string (older APIs). |
| `oauth2-client-credentials` | `clientId`, `clientSecret`, `tokenUri`, `scopes` | OAuth2 Client Credentials grant; DHIS2 caches the access token between calls. |

The codegen `spec_patches` module synthesises the Jackson discriminator
that upstream DHIS2 omits (BUGS.md #14), so the union is fully typed
end-to-end. Callers either build a concrete variant
(`HttpBasicAuthScheme(username=..., password=...)`) or pass a raw dict
with a `type` key — pydantic routes it to the right subclass.

## Register + run workflow

```bash
# Register a route that proxies to an external API with API-token auth:
dhis2 route create \
  --code analytics-bridge \
  --name "External analytics bridge" \
  --url "https://reports.example.org/api" \
  --auth-type api-token \
  --auth-token "$EXTERNAL_API_TOKEN"

# Run it. DHIS2 issues the upstream call with the stored auth applied:
dhis2 route run <uid> --method GET
dhis2 route run <uid> --method GET --sub-path /reports/2025

# POST a JSON body through:
dhis2 route run <uid> --method POST --body '{"key":"value"}'
```

`run`'s response stays `dict[str, Any]` — the payload is whatever the
upstream service returns, so no stable model fits. This is the explicit
HTTP-boundary carveout for an opaque proxy.

## Library API

```python
from dhis2_client import JsonPatchOp
from dhis2_client.auth_schemes import HttpBasicAuthScheme

from dhis2_core.client_context import open_client
from dhis2_core.plugins.route.service import RoutePayload, add_route, run_route
from dhis2_core.profile import profile_from_env

profile = profile_from_env()

payload = RoutePayload(
    code="weather",
    name="Weather upstream",
    url="https://api.weather.example/forecast",
    auth=HttpBasicAuthScheme(username="dhis2", password="..."),
)
result = await add_route(profile, payload)
uid = result.created_uid

# Patch one field without re-sending the rest:
await patch_route(profile, uid, [JsonPatchOp(op="replace", path="/disabled", value=True)])

# Proxy a call through:
data = await run_route(profile, uid, method="GET", sub_path="forecast")
```

## Not covered here

- **Per-call auth override** — `/api/routes/.../run` always uses the
  stored auth scheme. To swap auth dynamically, register multiple routes
  pointing at the same URL with different schemes.
- **Streaming responses** — the run endpoint buffers the upstream
  response into memory before returning. Large downloads should bypass
  the route surface and hit the upstream directly.
- **Authority gates on `/run`** — DHIS2 supports per-route authorities
  to restrict who can invoke it; configurable via the `authorities`
  field on `RoutePayload` but not surfaced as CLI flags. Use `route
  patch` with a JSON Patch op when needed.
