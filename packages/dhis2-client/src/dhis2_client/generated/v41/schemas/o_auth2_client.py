"""Generated OAuth2Client model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class OAuth2Client(BaseModel):
    """DHIS2 O Auth2 Client - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/oAuth2Clients.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )

    cid: str | None = Field(default=None, description="Unique. Length/value max=230.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    displayName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    grantTypes: list[Any] | None = Field(default=None, description="Collection of String.")

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    redirectUris: list[Any] | None = Field(default=None, description="Collection of String.")

    secret: str | None = Field(default=None, description="Length/value min=36, max=36.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
