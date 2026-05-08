"""Generated Axis model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Axis(BaseModel):
    """Generated model for DHIS2 `Axis`.

    DHIS2 Axis - DHIS2 resource (generated from /api/schemas at DHIS2 v41).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    axis: int | None = Field(default=None, description="Length/value max=2147483647.")
    dimensionalItem: str | None = Field(default=None, description="Length/value max=255.")
