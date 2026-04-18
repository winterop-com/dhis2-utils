"""Generated TrackedEntityType model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class TrackedEntityType(BaseModel):
    """DHIS2 Tracked Entity Type - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/trackedEntityTypes.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    allowAuditLog: bool | None = None

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    externalAccess: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    featureType: str | None = None

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    maxTeiCountToReturn: int | None = Field(default=None, description="Length/value max=2147483647.")

    minAttributesRequiredToSearch: int | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    trackedEntityTypeAttributes: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityTypeAttribute."
    )

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )

    userGroupAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )
