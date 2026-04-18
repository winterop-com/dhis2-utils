"""DHIS2 Personal Access Token authentication."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class PatAuth(BaseModel):
    """DHIS2 Personal Access Token — sent as Authorization: ApiToken <pat>."""

    model_config = ConfigDict(frozen=True)

    token: str

    async def headers(self) -> dict[str, str]:
        """Return the Authorization: ApiToken header."""
        return {"Authorization": f"ApiToken {self.token}"}

    async def refresh_if_needed(self) -> None:
        """PATs are long-lived; nothing to refresh."""
        return None
