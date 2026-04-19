"""Generated DashboardItem model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import DashboardItemShape, DashboardItemType
from .attribute_value import AttributeValue


class DashboardItem(BaseModel):
    """Generated model for DHIS2 `DashboardItem`.

    DHIS2 Dashboard Item - DHIS2 resource (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/dashboardItems.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    appKey: str | None = Field(default=None, description="Length/value max=255.")
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    contentCount: int | None = Field(default=None, description="Read-only.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    displayName: str | None = Field(default=None, description="Read-only.")
    eventChart: Reference | None = Field(default=None, description="Reference to EventChart.")
    eventReport: Reference | None = Field(default=None, description="Reference to EventReport.")
    eventVisualization: Reference | None = Field(default=None, description="Reference to EventVisualization.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    height: int | None = Field(default=None, description="Length/value max=2147483647.")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    interpretationCount: int | None = Field(default=None, description="Read-only.")
    interpretationLikeCount: int | None = Field(default=None, description="Read-only.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    map: Reference | None = Field(default=None, description="Reference to Map.")
    messages: bool | None = None
    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    reports: list[Any] | None = Field(default=None, description="Collection of Report.")
    resources: list[Any] | None = Field(default=None, description="Collection of Document.")
    shape: DashboardItemShape | None = None
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    text: str | None = Field(default=None, description="Length/value max=2147483647.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    type: DashboardItemType | None = Field(default=None, description="Read-only.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    users: list[Any] | None = Field(default=None, description="Collection of User.")
    visualization: Reference | None = Field(default=None, description="Reference to Visualization.")
    width: int | None = Field(default=None, description="Length/value max=2147483647.")
    x: int | None = Field(default=None, description="Length/value max=2147483647.")
    y: int | None = Field(default=None, description="Length/value max=2147483647.")
