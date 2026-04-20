"""Generated IndicatorGroup model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class IndicatorGroup(BaseModel):
    """Generated model for DHIS2 `IndicatorGroup`.

    DHIS2 Indicator Group - persisted metadata (generated from /api/schemas at DHIS2 v43).

    API endpoint: /dev-2-43/api/indicatorGroups.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    description: str | None = Field(default=None, description="Length/value min=2, max=255.")
    displayName: str | None = Field(default=None, description="Read-only.")
    groupSet: Reference | None = Field(
        default=None, description="Reference to IndicatorGroupSet. Read-only (inverse side)."
    )
    groupSets: list[Any] | None = Field(
        default=None, description="Collection of IndicatorGroupSet. Read-only (inverse side)."
    )
    href: str | None = Field(default=None, description="Length/value max=2147483647.")
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    indicators: list[Any] | None = Field(default=None, description="Collection of Indicator.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
