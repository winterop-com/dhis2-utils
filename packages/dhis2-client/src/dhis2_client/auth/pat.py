"""DHIS2 Personal Access Token authentication."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PatAuth:
    """DHIS2 Personal Access Token — sent as Authorization: ApiToken <pat>."""

    token: str

    async def headers(self) -> dict[str, str]:
        """Return the Authorization: ApiToken header."""
        return {"Authorization": f"ApiToken {self.token}"}

    async def refresh_if_needed(self) -> None:
        """PATs are long-lived; nothing to refresh."""
        return None
