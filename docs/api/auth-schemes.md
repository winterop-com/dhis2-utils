# Route auth schemes

DHIS2's Route API (`/api/routes`) proxies requests to upstream services. Its own auth is one of five discriminated variants — basic, API token, header, query param, OAuth2 client-credentials. The union is typed end-to-end via the `AuthScheme` `Annotated` union + `AuthSchemeAdapter` (a pydantic `TypeAdapter`) so callers can switch on the variant exhaustively with `match`.

## When to reach for it

- Authoring or editing a `Route` from Python (the route plugin already does this — the types let your own code stay on the same surface).
- Reading a route's auth back from DHIS2 + branching on the variant (e.g. "rotate every Bearer token expiring this week").
- Validating an inbound JSON blob (config file, CI fixture) as a typed `AuthScheme` before saving.

## Worked example — parse + dispatch

```python
from dhis2w_client import (
    AuthScheme,
    AuthSchemeAdapter,
    HttpBasicAuthScheme,
    ApiTokenAuthScheme,
    ApiHeadersAuthScheme,
    ApiQueryParamsAuthScheme,
    OAuth2ClientCredentialsAuthScheme,
)

# DHIS2 returns the auth block as a dict on the Route object. Adapter picks
# the right subclass by the `type` discriminator field.
raw = {"type": "http-basic", "username": "alice", "password": "..."}
scheme: AuthScheme = AuthSchemeAdapter.validate_python(raw)

match scheme:
    case HttpBasicAuthScheme(username=u):
        print(f"basic auth as {u}")
    case ApiTokenAuthScheme(token=t):
        print(f"api token {t[:6]}…")
    case ApiHeadersAuthScheme(headers=hs):
        print(f"headers: {sorted(hs)}")
    case ApiQueryParamsAuthScheme(queryParams=qs):
        print(f"query-params: {sorted(qs)}")
    case OAuth2ClientCredentialsAuthScheme(tokenUri=uri):
        print(f"oauth2 cc against {uri}")
```

## Worked example — round-trip a Route's auth block

```python
from dhis2w_client import AuthSchemeAdapter
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    raw = await client.get_raw("/api/routes/abcdefghij")
    scheme = AuthSchemeAdapter.validate_python(raw["auth"])
    print(f"{raw['name']} -> auth.type={scheme.type}")
```

::: dhis2w_client.v42.auth_schemes
