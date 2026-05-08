"""Create DHIS2 Personal Access Tokens via Playwright-authenticated API calls."""

from __future__ import annotations

import json
import time
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_browser.session import logged_in_page


class PatAttribute(BaseModel):
    """One attribute entry on a DHIS2 PAT V2 — carries an allowlist keyed by `type`.

    DHIS2 recognises three attribute types, each with its own allowlist field:
    `IpAllowedList` / `allowedIps`, `MethodAllowedList` / `allowedMethods`,
    `RefererAllowedList` / `allowedReferrers`. All fields except `type` are
    optional so a single `PatAttribute` class models every shape.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: str
    allowedIps: list[str] | None = None
    allowedMethods: list[str] | None = None
    allowedReferrers: list[str] | None = None


class PatPayload(BaseModel):
    """JSON body DHIS2 accepts at `POST /api/apiToken` for creating a V2 token."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: str
    name: str | None = None
    expire: int | None = None
    attributes: list[PatAttribute] = Field(default_factory=list)


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

    def to_payload(self) -> PatPayload:
        """Convert to the typed JSON body DHIS2 accepts at POST /api/apiToken."""
        attributes: list[PatAttribute] = []
        if self.allowed_ips:
            attributes.append(PatAttribute(type="IpAllowedList", allowedIps=list(self.allowed_ips)))
        if self.allowed_methods:
            attributes.append(
                PatAttribute(type="MethodAllowedList", allowedMethods=[m.upper() for m in self.allowed_methods])
            )
        if self.allowed_referrers:
            attributes.append(PatAttribute(type="RefererAllowedList", allowedReferrers=list(self.allowed_referrers)))
        return PatPayload(
            type=self.token_type,
            name=self.name,
            expire=self._resolve_expire(),
            attributes=attributes,
        )

    def _resolve_expire(self) -> int | None:
        """Resolve explicit-ms + days-from-now into the absolute epoch-ms DHIS2 expects."""
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
            data=payload.model_dump_json(exclude_none=True, by_alias=True),
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
