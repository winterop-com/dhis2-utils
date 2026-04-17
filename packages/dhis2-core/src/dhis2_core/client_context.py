"""Helpers for opening a connected Dhis2Client from a resolved Profile."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dhis2_client import AuthProvider, BasicAuth, Dhis2Client, PatAuth

from dhis2_core.profile import Profile


def build_auth(profile: Profile) -> AuthProvider:
    """Construct an `AuthProvider` matching the profile's auth kind."""
    if profile.auth == "pat":
        if not profile.token:
            raise ValueError("profile.auth == 'pat' but no token is set")
        return PatAuth(token=profile.token)
    if profile.auth == "basic":
        if not (profile.username and profile.password):
            raise ValueError("profile.auth == 'basic' but username/password are missing")
        return BasicAuth(username=profile.username, password=profile.password)
    raise ValueError(f"unknown profile.auth value: {profile.auth!r}")


@asynccontextmanager
async def open_client(profile: Profile, *, allow_version_fallback: bool = True) -> AsyncIterator[Dhis2Client]:
    """Open a connected Dhis2Client for `profile` — yields inside `async with`."""
    auth = build_auth(profile)
    async with Dhis2Client(profile.base_url, auth=auth, allow_version_fallback=allow_version_fallback) as client:
        yield client
