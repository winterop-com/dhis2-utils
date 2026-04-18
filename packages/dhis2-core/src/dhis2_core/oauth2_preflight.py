"""Preflight probe that detects whether DHIS2's Spring Authorization Server is enabled."""

from __future__ import annotations

import httpx

DISCOVERY_PATH = "/.well-known/openid-configuration"


async def check_oauth2_server(base_url: str, *, timeout: float = 5.0) -> str | None:
    """Probe `base_url` for an OIDC discovery doc.

    Returns None when DHIS2 looks like a functional OAuth2 Authorization Server.
    Otherwise returns a user-facing error string that explains what's missing
    and how to fix it (typically: enable `oauth2.server.enabled=on` in dhis.conf).
    """
    url = base_url.rstrip("/") + DISCOVERY_PATH
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            response = await client.get(url)
    except httpx.ConnectError as exc:
        return f"cannot reach {base_url} — is the DHIS2 instance running? ({exc})"
    except httpx.TimeoutException:
        return f"timed out probing {url} — DHIS2 may be slow or unreachable"
    except httpx.HTTPError as exc:
        return f"error probing {url}: {type(exc).__name__}: {exc}"
    if response.status_code == 404:
        return (
            f"DHIS2 at {base_url} does not expose OAuth2/OIDC endpoints "
            f"(GET {DISCOVERY_PATH} returned 404). "
            "Enable the built-in Authorization Server by adding "
            "`oauth2.server.enabled = on` to dhis.conf, then restart DHIS2."
        )
    if response.status_code >= 400:
        return (
            f"DHIS2 at {base_url} returned HTTP {response.status_code} on {DISCOVERY_PATH}; "
            "the OAuth2 Authorization Server may be misconfigured."
        )
    content_type = response.headers.get("content-type", "")
    if "json" not in content_type.lower():
        return (
            f"unexpected response from {url} (content-type={content_type!r}); "
            "OAuth2 Authorization Server may not be fully configured."
        )
    return None
