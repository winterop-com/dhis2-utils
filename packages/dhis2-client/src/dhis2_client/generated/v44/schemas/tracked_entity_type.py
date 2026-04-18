"""Generated TrackedEntityType model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class TrackedEntityType(BaseModel):
    """DHIS2 Tracked Entity Type - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/trackedEntityTypes.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    allowAuditLog: bool | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    displayTrackedEntityTypesLabel: str | None = None

    enableChangeLog: bool | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    featureType: str | None = None

    formName: str | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    maxTeiCountToReturn: int | None = None

    minAttributesRequiredToSearch: int | None = None

    name: str | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Read-only (inverse side).")

    trackedEntityTypeAttributes: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    trackedEntityTypesLabel: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    uid: str | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
