"""PAT (Personal Access Token) registration helpers — POST /api/apiToken."""

from __future__ import annotations

import json
from typing import Any

from dhis2w_client import Dhis2Client
from dhis2w_client.v42.auth.base import AuthProvider
from pydantic import BaseModel, ConfigDict


class PatCredentials(BaseModel):
    """PAT value + metadata returned when a PAT is created."""

    model_config = ConfigDict(frozen=True)

    uid: str
    token: str
    description: str | None = None


async def register_pat(
    *,
    base_url: str,
    admin_auth: AuthProvider,
    description: str | None = None,
    expires_in_days: int | None = None,
    allowed_ips: list[str] | None = None,
    allowed_methods: list[str] | None = None,
    allowed_referrers: list[str] | None = None,
) -> PatCredentials:
    """Create a PAT via POST /api/apiToken. Returns the one-time token value + uid.

    `expires_in_days` sets an absolute expiry (DHIS2 converts to epoch millis).
    `allowed_*` lists populate DHIS2's `attributes` array with IP/method/referrer
    restrictions — empty/None means no restriction. The token value is only
    returned once on creation; subsequent GETs never expose it.
    """
    payload: dict[str, Any] = {"type": "PERSONAL_ACCESS_TOKEN_V2"}
    attributes: list[dict[str, Any]] = []
    if allowed_ips:
        attributes.append({"type": "IpAllowedList", "allowedIps": allowed_ips})
    if allowed_methods:
        attributes.append({"type": "MethodAllowedList", "allowedMethods": allowed_methods})
    if allowed_referrers:
        attributes.append({"type": "RefererAllowedList", "allowedReferrers": allowed_referrers})
    payload["attributes"] = attributes
    if description:
        payload["description"] = description
    if expires_in_days is not None:
        # DHIS2 wants expiry as absolute epoch millis — compute from now.
        import time

        payload["expire"] = int((time.time() + expires_in_days * 86400) * 1000)

    async with Dhis2Client(base_url, auth=admin_auth) as client:
        response = await client.post_raw("/api/apiToken", payload)
    response_body = response.get("response") or {}
    key = response_body.get("key")
    uid = response_body.get("uid") or response.get("id") or ""
    if not isinstance(key, str) or not key:
        raise RuntimeError(f"unexpected /api/apiToken response: {json.dumps(response)[:500]}")
    return PatCredentials(uid=str(uid), token=key, description=description)
