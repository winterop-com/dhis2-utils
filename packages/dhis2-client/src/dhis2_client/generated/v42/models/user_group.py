"""Generated UserGroup model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class UserGroup(BaseModel):
    """DHIS2 User Group - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/userGroups.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    displayName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    managedByGroups: list[Any] | None = Field(
        default=None, description="Collection of UserGroup. Read-only (inverse side)."
    )

    managedGroups: list[Any] | None = Field(default=None, description="Collection of UserGroup.")

    members: list[Any] | None = Field(default=None, description="Collection of User.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
