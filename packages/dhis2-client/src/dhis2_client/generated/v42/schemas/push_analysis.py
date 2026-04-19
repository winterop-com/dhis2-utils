"""Generated PushAnalysis model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class PushAnalysis(BaseModel):
    """DHIS2 Push Analysis - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/pushAnalysis.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dashboard: Reference | None = Field(default=None, description="Reference to Dashboard.")

    displayName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    message: str | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Length/value max=255.")

    recipientUserGroups: list[Any] | None = Field(default=None, description="Collection of UserGroup.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    title: str | None = Field(default=None, description="Length/value max=255.")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
