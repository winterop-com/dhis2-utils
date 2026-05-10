"""Generated TrackedEntityAttributeValue model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class TrackedEntityAttributeValue(BaseModel):
    """Generated model for DHIS2 `TrackedEntityAttributeValue`.

    DHIS2 Tracked Entity Attribute Value - DHIS2 resource (generated from /api/schemas at DHIS2 v41).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    created: datetime | None = None
    lastUpdated: datetime | None = None
    storedBy: str | None = Field(default=None, description="Length/value max=255.")
    trackedEntityAttribute: Reference | None = Field(
        default=None, description="Reference to TrackedEntityAttribute. Read-only (inverse side)."
    )
    trackedEntityInstance: Reference | None = Field(
        default=None, description="Reference to TrackedEntity. Read-only (inverse side)."
    )
    value: str | None = Field(default=None, description="Length/value max=2147483647.")
