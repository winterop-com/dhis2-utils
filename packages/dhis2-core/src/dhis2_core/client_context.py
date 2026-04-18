"""Helpers for opening a connected Dhis2Client from a resolved Profile."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dhis2_client import AuthProvider, BasicAuth, Dhis2Client, PatAuth
from dhis2_client.auth.oauth2 import OAuth2Auth

from dhis2_core.oauth2_redirect import capture_code
from dhis2_core.profile import Profile, ResolvedProfile, resolve
from dhis2_core.token_store import token_store_for_scope


def build_auth(
    profile: Profile,
    *,
    profile_name: str | None = None,
    scope: str = "global",
) -> AuthProvider:
    """Construct an `AuthProvider` matching the profile's auth kind.

    `profile_name` and `scope` only matter for `auth="oauth2"` — they pick the
    token-store key and the DB file location. When omitted for oauth2, fall
    back to `DHIS2_PROFILE` env var or a synthetic store key.
    """
    if profile.auth == "pat":
        if not profile.token:
            raise ValueError("profile.auth == 'pat' but no token is set")
        return PatAuth(token=profile.token)
    if profile.auth == "basic":
        if not (profile.username and profile.password):
            raise ValueError("profile.auth == 'basic' but username/password are missing")
        return BasicAuth(username=profile.username, password=profile.password)
    if profile.auth == "oauth2":
        return _build_oauth2(profile, profile_name=profile_name, scope=scope)
    raise ValueError(f"unknown profile.auth value: {profile.auth!r}")


def _build_oauth2(
    profile: Profile,
    *,
    profile_name: str | None,
    scope: str,
) -> OAuth2Auth:
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
        return await capture_code(redirect_uri, expected_state, open_url=auth_url)

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


def build_auth_for_name(name: str | None = None) -> tuple[Profile, AuthProvider]:
    """Resolve a profile by name and return (profile, auth). Convenience for the CLI."""
    resolved = resolve(name)
    auth = build_auth(resolved.profile, profile_name=resolved.name, scope=scope_from_resolved(resolved))
    return resolved.profile, auth


@asynccontextmanager
async def open_client(
    profile: Profile,
    *,
    profile_name: str | None = None,
    scope: str = "global",
    allow_version_fallback: bool = True,
) -> AsyncIterator[Dhis2Client]:
    """Open a connected Dhis2Client for `profile` — yields inside `async with`."""
    auth = build_auth(profile, profile_name=profile_name, scope=scope)
    async with Dhis2Client(profile.base_url, auth=auth, allow_version_fallback=allow_version_fallback) as client:
        yield client
