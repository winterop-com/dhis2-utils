"""Generated Interpretation model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AnalyticsFavoriteType


class Interpretation(BaseModel):
    """Generated model for DHIS2 `Interpretation`.

    DHIS2 Interpretation - DHIS2 resource (generated from /api/schemas at DHIS2 v43).

    API endpoint: /api/interpretations.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = None
    comments: list[Any] | None = Field(default=None, description="Collection of InterpretationComment.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dataSet: Reference | None = Field(default=None, description="Reference to DataSet.")
    displayName: str | None = Field(default=None, description="Read-only.")
    eventChart: Reference | None = Field(default=None, description="Reference to EventChart.")
    eventReport: Reference | None = Field(default=None, description="Reference to EventReport.")
    eventVisualization: Reference | None = Field(default=None, description="Reference to EventVisualization.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    likeByUsers: list[Any] | None = Field(default=None, description="Collection of User.")
    likes: int | None = Field(default=None, description="Length/value max=2147483647.")
    map: Reference | None = Field(default=None, description="Reference to Map.")
    mentions: list[Any] | None = Field(default=None, description="Collection of Mention. Length/value max=255.")
    name: str | None = Field(default=None, description="Length/value max=2147483647.")
    organisationUnit: Reference | None = Field(default=None, description="Reference to OrganisationUnit.")
    period: Any | None = Field(default=None, description="Reference to Period. Length/value max=255.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    text: str | None = Field(default=None, description="Length/value max=2147483647.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    type: AnalyticsFavoriteType | None = Field(default=None, description="Read-only.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    visualization: Reference | None = Field(default=None, description="Reference to Visualization.")
