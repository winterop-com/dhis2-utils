"""Helpers for opening a connected Dhis2Client from a resolved Profile."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from dhis2_core.profile import Profile, ResolvedProfile, resolve

if TYPE_CHECKING:
    import httpx
    from dhis2_client import AuthProvider, Dhis2Client, RetryPolicy
    from dhis2_client.auth.oauth2 import OAuth2Auth


def build_auth(
    profile: Profile,
    *,
    profile_name: str | None = None,
    scope: str = "global",
    open_browser: bool = True,
) -> AuthProvider:
    """Construct an `AuthProvider` matching the profile's auth kind.

    `profile_name` and `scope` only matter for `auth="oauth2"` — they pick the
    token-store key and the DB file location. When omitted for oauth2, fall
    back to `DHIS2_PROFILE` env var or a synthetic store key.

    `open_browser` only matters for `auth="oauth2"`. When False, the CLI prints
    the authorization URL to stderr instead of launching the system browser —
    useful when running over SSH, in a different browser, or under Playwright.
    """
    from dhis2_client import BasicAuth, PatAuth  # noqa: PLC0415 — defer to keep `--help` fast

    if profile.auth == "pat":
        if not profile.token:
            raise ValueError("profile.auth == 'pat' but no token is set")
        return PatAuth(token=profile.token)
    if profile.auth == "basic":
        if not (profile.username and profile.password):
            raise ValueError("profile.auth == 'basic' but username/password are missing")
        return BasicAuth(username=profile.username, password=profile.password)
    if profile.auth == "oauth2":
        return _build_oauth2(profile, profile_name=profile_name, scope=scope, open_browser=open_browser)
    raise ValueError(f"unknown profile.auth value: {profile.auth!r}")


def _build_oauth2(
    profile: Profile,
    *,
    profile_name: str | None,
    scope: str,
    open_browser: bool,
) -> OAuth2Auth:
    from dhis2_client.auth.oauth2 import OAuth2Auth  # noqa: PLC0415 — defer fastapi/sqlalchemy

    from dhis2_core.oauth2_redirect import capture_code  # noqa: PLC0415
    from dhis2_core.token_store import token_store_for_scope  # noqa: PLC0415

    if not profile.client_id:
        raise ValueError("profile.auth == 'oauth2' requires client_id")
    if not profile.client_secret:
        raise ValueError("profile.auth == 'oauth2' requires client_secret")
    if not profile.scope:
        raise ValueError("profile.auth == 'oauth2' requires a scope (DHIS2 only recognises 'ALL')")
    if not profile.redirect_uri:
        raise ValueError("profile.auth == 'oauth2' requires redirect_uri")
    name = profile_name or os.environ.get("DHIS2_PROFILE") or "default"
    store = token_store_for_scope(scope)
    redirect_uri = profile.redirect_uri

    async def capturer(auth_url: str, expected_state: str) -> str:
        return await capture_code(
            redirect_uri,
            expected_state,
            auth_url=auth_url,
            open_browser=open_browser,
        )

    return OAuth2Auth(
        base_url=profile.base_url,
        client_id=profile.client_id,
        client_secret=profile.client_secret,
        scope=profile.scope,
        redirect_uri=profile.redirect_uri,
        token_store=store,
        store_key=f"profile:{name}",
        redirect_capturer=capturer,
    )


def scope_from_resolved(resolved: ResolvedProfile) -> str:
    """Translate a `ResolvedProfile.source` into a 'project' / 'global' scope."""
    if resolved.source == "project-toml":
        return "project"
    return "global"


def build_auth_for_name(
    name: str | None = None,
    *,
    open_browser: bool = True,
) -> tuple[Profile, AuthProvider]:
    """Resolve a profile by name and return (profile, auth). Convenience for the CLI.

    `open_browser=False` is plumbed through to OAuth2 auth so `dhis2 profile
    login --no-browser` and its kin skip the `webbrowser.open()` call.
    """
    resolved = resolve(name)
    auth = build_auth(
        resolved.profile,
        profile_name=resolved.name,
        scope=scope_from_resolved(resolved),
        open_browser=open_browser,
    )
    return resolved.profile, auth


@asynccontextmanager
async def open_client(
    profile: Profile,
    *,
    profile_name: str | None = None,
    scope: str = "global",
    allow_version_fallback: bool = True,
    retry_policy: RetryPolicy | None = None,
    http_limits: httpx.Limits | None = None,
    system_cache_ttl: float | None = 300.0,
) -> AsyncGenerator[Dhis2Client]:
    """Open a connected Dhis2Client for `profile` — yields inside `async with`.

    Pass `retry_policy=RetryPolicy(...)` to enable exponential-backoff retries
    on transient HTTP failures (connection errors, 429/502/503/504). See
    `dhis2_client.RetryPolicy` for the tuning knobs.

    Pass `http_limits=httpx.Limits(max_connections=..., max_keepalive_connections=...)`
    to tune the connection pool for high-concurrency workloads (or to clamp
    it down against a small DHIS2 instance). See
    `docs/architecture/client.md` for sizing guidance.

    `system_cache_ttl` (default 300 s) caps how long cached system-level
    reads (`client.system.info()`, default categoryCombo UID, per-key
    system settings) stay fresh before the next call refetches. Pass
    `None` to disable the cache entirely.
    """
    from dhis2_client import Dhis2Client  # noqa: PLC0415 — defer client+OAS until actually opening

    auth = build_auth(profile, profile_name=profile_name, scope=scope)
    async with Dhis2Client(
        profile.base_url,
        auth=auth,
        allow_version_fallback=allow_version_fallback,
        retry_policy=retry_policy,
        http_limits=http_limits,
        system_cache_ttl=system_cache_ttl,
    ) as client:
        yield client
