"""Generated Dashboard model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Dashboard(BaseModel):
    """DHIS2 Dashboard - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/dashboards.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    allowedFilters: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    itemConfig: Any | None = Field(default=None, description="Reference to ItemConfig. Length/value max=255.")

    itemCount: int | None = Field(default=None, description="Read-only.")

    items: list[Any] | None = Field(default=None, description="Collection of DashboardItem.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    layout: Any | None = Field(default=None, description="Reference to Layout. Length/value max=255.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    restrictFilters: bool | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
