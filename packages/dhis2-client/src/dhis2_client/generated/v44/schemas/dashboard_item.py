"""Generated DashboardItem model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import DashboardItemShape, DashboardItemType


class DashboardItem(BaseModel):
    """Generated model for DHIS2 `DashboardItem`.

    DHIS2 Dashboard Item - DHIS2 resource (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/dashboardItems.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    appKey: str | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = None

    contentCount: int | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    displayText: str | None = None

    eventChart: Reference | None = Field(default=None, description="Reference to EventChart. Read-only (inverse side).")

    eventReport: Reference | None = Field(
        default=None, description="Reference to EventReport. Read-only (inverse side)."
    )

    eventVisualization: Reference | None = Field(
        default=None, description="Reference to EventVisualization. Read-only (inverse side)."
    )

    height: int | None = None

    href: str | None = None

    id: str | None = None

    interpretationCount: int | None = None

    interpretationLikeCount: int | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    map: Reference | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    messages: bool | None = None

    name: str | None = None

    reports: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    resources: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    shape: DashboardItemShape | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    text: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    type: DashboardItemType | None = None

    users: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    visualization: Reference | None = Field(
        default=None, description="Reference to Visualization. Read-only (inverse side)."
    )

    width: int | None = None

    x: int | None = None

    y: int | None = None
