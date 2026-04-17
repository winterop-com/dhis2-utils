"""Create DHIS2 Personal Access Tokens via Playwright-authenticated API calls."""

from __future__ import annotations

import json
import time
from typing import Any

from pydantic import BaseModel, Field

from dhis2_browser.session import logged_in_page


class PatOptions(BaseModel):
    """Optional knobs for a DHIS2 Personal Access Token (V2)."""

    name: str | None = Field(default=None, description="Friendly display name for the token.")
    expires_in_days: int | None = Field(
        default=None,
        description="Token lifetime; converted to a DHIS2 `expire` epoch-ms value. None = no expiry.",
    )
    expires_at_ms: int | None = Field(
        default=None,
        description="Explicit expiry as unix epoch milliseconds (overrides expires_in_days).",
    )
    allowed_ips: list[str] | None = Field(
        default=None,
        description="CIDR/IP allowlist. Token only works when the request originates here.",
    )
    allowed_methods: list[str] | None = Field(
        default=None,
        description="HTTP method allowlist (e.g. ['GET', 'POST']). Default: all methods allowed.",
    )
    allowed_referrers: list[str] | None = Field(
        default=None,
        description="Referer URL allowlist. Useful when the token is used from a web origin.",
    )
    token_type: str = Field(
        default="PERSONAL_ACCESS_TOKEN_V2",
        description="DHIS2 token type; V2 is the current format (V1 exists for legacy reasons).",
    )

    def to_payload(self) -> dict[str, Any]:
        """Convert to the JSON body accepted by POST /api/apiToken on DHIS2 v2.42+."""
        payload: dict[str, Any] = {"type": self.token_type, "attributes": []}
        if self.name is not None:
            payload["name"] = self.name
        expire = self._resolve_expire()
        if expire is not None:
            payload["expire"] = expire
        attributes: list[dict[str, Any]] = []
        if self.allowed_ips:
            attributes.append({"type": "IpAllowedList", "allowedIps": list(self.allowed_ips)})
        if self.allowed_methods:
            attributes.append(
                {"type": "MethodAllowedList", "allowedMethods": [m.upper() for m in self.allowed_methods]}
            )
        if self.allowed_referrers:
            attributes.append({"type": "RefererAllowedList", "allowedReferrers": list(self.allowed_referrers)})
        if attributes:
            payload["attributes"] = attributes
        return payload

    def _resolve_expire(self) -> int | None:
        if self.expires_at_ms is not None:
            return self.expires_at_ms
        if self.expires_in_days is not None:
            now_ms = int(time.time() * 1000)
            return now_ms + self.expires_in_days * 86_400_000
        return None


async def create_pat(
    base_url: str,
    username: str,
    password: str,
    *,
    options: PatOptions | None = None,
    headless: bool | None = None,
) -> str:
    """Log in via Playwright and create a new PAT; returns the token value (`d2p_...`).

    The token is only returned by DHIS2 once, at creation — store it somewhere
    persistent; there is no way to recover it later from the server.

    `headless=None` (default) honors the `DHIS2_HEADFUL=1` env var so you can
    watch the browser during tests or smoke runs without threading a flag through.
    """
    url = base_url.rstrip("/")
    resolved = options or PatOptions()
    payload = resolved.to_payload()
    async with logged_in_page(url, username, password, headless=headless) as (_, page):
        response = await page.request.post(
            f"{url}/api/apiToken",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )
        if not response.ok:
            body = await response.text()
            raise RuntimeError(f"PAT creation failed ({response.status}): {body[:500]}")
        body_text = await response.json()
    key = _extract_token_key(body_text)
    if key is None:
        raise RuntimeError(f"unexpected PAT response shape: {json.dumps(body_text)[:500]}")
    return key


def _extract_token_key(payload: dict[str, Any]) -> str | None:
    """Pull the token value from the DHIS2 response, tolerating shape variation."""
    candidates = (
        payload.get("key"),
        (payload.get("response") or {}).get("key"),
        (payload.get("response") or {}).get("token"),
        payload.get("token"),
    )
    for candidate in candidates:
        if isinstance(candidate, str) and candidate:
            return candidate
    return None
