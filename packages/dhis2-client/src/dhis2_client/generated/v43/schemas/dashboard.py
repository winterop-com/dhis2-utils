"""Generated Dashboard model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class Dashboard(BaseModel):
    """Generated model for DHIS2 `Dashboard`.

    DHIS2 Dashboard - persisted metadata (generated from /api/schemas at DHIS2 v43).

    API endpoint: /dev-2-43/api/dashboards.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    allowedFilters: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dashboardItems: list[Any] | None = Field(default=None, description="Collection of DashboardItem.")
    description: str | None = Field(default=None, description="Length/value max=255.")
    displayDescription: str | None = Field(default=None, description="Read-only.")
    displayName: str | None = Field(default=None, description="Read-only.")
    embedded: Any | None = Field(default=None, description="Reference to EmbeddedDashboard. Length/value max=255.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    itemConfig: Any | None = Field(default=None, description="Reference to ItemConfig. Length/value max=255.")
    itemCount: int | None = Field(default=None, description="Read-only.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    layout: Any | None = Field(default=None, description="Reference to Layout. Length/value max=255.")
    name: str | None = Field(default=None, description="Length/value min=1, max=230.")
    restrictFilters: bool | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
