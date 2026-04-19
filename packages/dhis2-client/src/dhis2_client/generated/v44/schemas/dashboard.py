"""Generated Dashboard model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class Dashboard(BaseModel):
    """Generated model for DHIS2 `Dashboard`.

    DHIS2 Dashboard - persisted metadata (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/dashboards.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    allowedFilters: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dashboardItems: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    description: str | None = None

    displayDescription: str | None = None

    displayName: str | None = None

    embedded: Any | None = Field(default=None, description="Reference to EmbeddedDashboard. Read-only (inverse side).")

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    itemConfig: Any | None = Field(default=None, description="Reference to ItemConfig. Read-only (inverse side).")

    itemCount: int | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    layout: Any | None = Field(default=None, description="Reference to Layout. Read-only (inverse side).")

    name: str | None = None

    restrictFilters: bool | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
