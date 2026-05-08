"""Generated PushAnalysis model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from .attribute_value import AttributeValue


class PushAnalysis(BaseModel):
    """Generated model for DHIS2 `PushAnalysis`.

    DHIS2 Push Analysis - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/pushAnalysis.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dashboard: Reference | None = Field(default=None, description="Reference to Dashboard.")
    displayName: str | None = Field(default=None, description="Read-only.")
    externalAccess: bool | None = None
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    message: str | None = Field(default=None, description="Length/value max=2147483647.")
    name: str | None = Field(default=None, description="Length/value max=255.")
    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")
    recipientUserGroups: list[Any] | None = Field(default=None, description="Collection of UserGroup.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    title: str | None = Field(default=None, description="Length/value max=255.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userAccess: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )
    userGroupAccess: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )
