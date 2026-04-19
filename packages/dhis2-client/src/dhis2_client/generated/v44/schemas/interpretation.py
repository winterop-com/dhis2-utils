"""Generated Interpretation model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AnalyticsFavoriteType


class Interpretation(BaseModel):
    """Generated model for DHIS2 `Interpretation`.

    DHIS2 Interpretation - DHIS2 resource (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/interpretations.



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

    comments: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataSet: Reference | None = Field(default=None, description="Reference to DataSet. Read-only (inverse side).")

    displayName: str | None = None

    eventChart: Reference | None = Field(default=None, description="Reference to EventChart. Read-only (inverse side).")

    eventReport: Reference | None = Field(
        default=None, description="Reference to EventReport. Read-only (inverse side)."
    )

    eventVisualization: Reference | None = Field(
        default=None, description="Reference to EventVisualization. Read-only (inverse side)."
    )

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    likeByUsers: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    likes: int | None = None

    map: Reference | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    mentions: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    name: str | None = None

    organisationUnit: Reference | None = Field(
        default=None, description="Reference to OrganisationUnit. Read-only (inverse side)."
    )

    period: Any | None = Field(default=None, description="Reference to Period. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    text: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    type: AnalyticsFavoriteType | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    visualization: Reference | None = Field(
        default=None, description="Reference to Visualization. Read-only (inverse side)."
    )
