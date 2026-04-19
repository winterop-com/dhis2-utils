"""Generated TrackedEntityProgramIndicatorDimension model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class TrackedEntityProgramIndicatorDimension(BaseModel):
    """Generated model for DHIS2 `TrackedEntityProgramIndicatorDimension`.

    DHIS2 Tracked Entity Program Indicator Dimension - DHIS2 resource (generated from /api/schemas at DHIS2 v44).




    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    filter: str | None = None

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    programIndicator: Reference | None = Field(
        default=None, description="Reference to ProgramIndicator. Read-only (inverse side)."
    )
