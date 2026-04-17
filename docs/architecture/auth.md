# Pluggable auth

`dhis2-client` has no hardcoded auth. It takes an `AuthProvider` Protocol at construction time and asks it for request headers.

## The Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class AuthProvider(Protocol):
    """Injects authentication headers into outgoing DHIS2 requests."""

    async def headers(self) -> dict[str, str]:
        """Return headers to apply to the next request."""
        ...

    async def refresh_if_needed(self) -> None:
        """Refresh credentials when close to expiry; no-op for static auth."""
        ...
```

That's it. Any class with these two async methods works.

## Shipped providers

### BasicAuth

HTTP Basic: `Authorization: Basic <base64(user:pass)>`. `refresh_if_needed` is a no-op. Good for dev and legacy integrations; **not recommended** for anything else.

```python
from dhis2_client import BasicAuth
auth = BasicAuth(username="admin", password="district")
```

### PatAuth

DHIS2 Personal Access Token: `Authorization: ApiToken <pat>`. Long-lived and revocable. **Best for automation and CI** — no interactive flow, no token expiry to manage, no client secrets. Tokens are issued by each DHIS2 user on their profile page.

```python
from dhis2_client import PatAuth
auth = PatAuth(token="d2pat_...")
```

### OAuth2Auth

OAuth 2.1 authorization-code flow with PKCE against DHIS2's `/oauth2/authorize` and `/oauth2/token` endpoints. Matches DHIS2 core's `AuthorizationServerConfig.java`. **Preferred for interactive use.**

The flow:

1. The provider generates a PKCE `code_verifier` / `code_challenge` pair and a `state` nonce.
2. It starts an asyncio loopback server on `redirect_uri`'s host:port.
3. It opens the browser at `/oauth2/authorize?...`.
4. The user authenticates in DHIS2 and gets redirected back.
5. The loopback server captures `code` + `state`, validates state (CSRF).
6. The provider exchanges `code` for access + refresh tokens via POST `/oauth2/token`.
7. Tokens are persisted via an injected `TokenStore`.

On subsequent calls:

- If the access token is valid, just use it.
- If it's within 60s of expiry, refresh via `refresh_token` grant.
- If no refresh token exists or refresh fails, re-run the authorization flow.

```python
from dhis2_client import OAuth2Auth
auth = OAuth2Auth(
    base_url="https://dhis2.example.org",
    client_id="dhis2-utils",
    client_secret="...",
    scope="openid email ALL",
    redirect_uri="http://localhost:8765",
    token_store=my_token_store,
    store_key="profile:prod",  # distinguishes tokens across profiles
)
```

### TokenStore

`OAuth2Auth` never touches the filesystem or keyring directly. Instead, it takes a `TokenStore` Protocol:

```python
class TokenStore(Protocol):
    async def get(self, key: str) -> OAuth2Token | None: ...
    async def set(self, key: str, token: OAuth2Token) -> None: ...
```

`dhis2-core` provides a SQLAlchemy+SQLite implementation backed by `.dhis2/tokens.sqlite`. A future keyring-backed implementation can be swapped in without touching `OAuth2Auth`.

## Design choices

- **No sync mirror.** Every provider is async-only. Callers running in notebooks can do `asyncio.run(auth.headers())` if needed; matching our async-first client.
- **TokenStore is injected, not discovered.** Keeps `dhis2-client` free of filesystem/OS concerns. All "where do tokens live" decisions live in `dhis2-core`.
- **OAuth2 loopback server is `asyncio.start_server`, not `http.server` on a thread.** Native async, no thread pool, cleaner teardown, no concurrent-request surprise. One HTTP request, server closes.
- **PKCE is mandatory.** Even with a confidential client. OAuth 2.1 recommends it, DHIS2 accepts it, and we have no reason to support the pre-PKCE flow.
- **`store_key` defaults to `f"{base_url}:{client_id}"`** but can be overridden. Profiles override it to `f"profile:{name}"` so tokens don't collide across instances.

## Future providers

All future providers land in `dhis2-client/auth/`. No changes to `client.py` needed.

- `ServiceAccountJwtAuth` — signed-JWT client-credentials grant, for unattended backends.
- `StaticBearerAuth` — pre-minted access token, dev/testing.
- `HeaderInjectorAuth` — sitting behind an auth proxy that already sets `Authorization`.
- `KeyringOAuth2Auth` — swap the `TokenStore` for an OS keyring-backed one.

The PyPI-track for `dhis2-client` means downstream users can also ship their own `AuthProvider` without forking us.
