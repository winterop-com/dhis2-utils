"""Shared pytest fixtures for dhis2-client tests, including live DHIS2 access."""

from __future__ import annotations

import asyncio
import os
from collections.abc import Iterator

import httpx
import pytest

# ---------------------------------------------------------------------------
# Play (public, remote)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def play_url() -> str:
    """Base URL of the DHIS2 play instance used by integration tests."""
    return os.environ.get("DHIS2_PLAY_URL", "https://play.im.dhis2.org/dev").rstrip("/")


@pytest.fixture(scope="session")
def play_username() -> str:
    """Username for the DHIS2 play instance."""
    return os.environ.get("DHIS2_PLAY_USER", "system")


@pytest.fixture(scope="session")
def play_password() -> str:
    """Password for the DHIS2 play instance."""
    return os.environ.get("DHIS2_PLAY_PASS", "System123")


# ---------------------------------------------------------------------------
# Local (docker / dev)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def local_url() -> str:
    """Base URL of the local DHIS2 instance used by destructive integration tests."""
    return os.environ.get("DHIS2_LOCAL_URL", "http://localhost:8080").rstrip("/")


@pytest.fixture(scope="session")
def local_username() -> str:
    """Username for the local DHIS2 instance (Basic auth fallback)."""
    return os.environ.get("DHIS2_LOCAL_USER", "admin")


@pytest.fixture(scope="session")
def local_password() -> str:
    """Password for the local DHIS2 instance (Basic auth fallback)."""
    return os.environ.get("DHIS2_LOCAL_PASS", "district")


def _is_local_reachable(url: str) -> bool:
    try:
        with httpx.Client(timeout=2.0) as client:
            client.get(f"{url}/dhis-web-login/")
        return True
    except (httpx.RequestError, httpx.HTTPError):
        return False


@pytest.fixture(scope="session")
def local_available(local_url: str) -> bool:
    """Whether the local DHIS2 instance is reachable; skip destructive tests otherwise."""
    return _is_local_reachable(local_url)


@pytest.fixture(scope="session")
def local_pat(
    local_url: str,
    local_username: str,
    local_password: str,
    local_available: bool,
) -> Iterator[str]:
    """Return a valid PAT for the local DHIS2 instance.

    Prefers the `DHIS2_LOCAL_PAT` env var (fast reuse). Otherwise mints a fresh
    PAT via Playwright. Skips the requesting test if neither is available.
    """
    env_token = os.environ.get("DHIS2_LOCAL_PAT")
    if env_token:
        yield env_token
        return
    if not local_available:
        pytest.skip(f"local DHIS2 not reachable at {local_url}")
    try:
        from dhis2_browser.pat import create_pat
    except ImportError:
        pytest.skip("dhis2-browser not installed — cannot mint PAT via Playwright")
    try:
        token = asyncio.run(create_pat(local_url, local_username, local_password))
    except Exception as exc:  # noqa: BLE001 — surface as skip so we don't wedge CI
        pytest.skip(f"PAT creation failed: {exc}")
    yield token
