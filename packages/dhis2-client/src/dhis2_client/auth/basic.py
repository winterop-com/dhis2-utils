"""HTTP Basic authentication provider."""

from __future__ import annotations

import base64
from dataclasses import dataclass


@dataclass(frozen=True)
class BasicAuth:
    """HTTP Basic auth — username/password encoded into Authorization header."""

    username: str
    password: str

    async def headers(self) -> dict[str, str]:
        """Return the Authorization: Basic header for this credential pair."""
        token = base64.b64encode(f"{self.username}:{self.password}".encode()).decode("ascii")
        return {"Authorization": f"Basic {token}"}

    async def refresh_if_needed(self) -> None:
        """Basic auth has no expiry; nothing to refresh."""
        return None
