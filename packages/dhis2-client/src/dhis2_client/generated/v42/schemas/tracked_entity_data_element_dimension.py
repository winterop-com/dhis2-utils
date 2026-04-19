"""Generated TrackedEntityDataElementDimension model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class TrackedEntityDataElementDimension(BaseModel):
    """Generated model for DHIS2 `TrackedEntityDataElementDimension`.

    DHIS2 Tracked Entity Data Element Dimension - DHIS2 resource (generated from /api/schemas at DHIS2 v42).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dataElement: Reference | None = Field(default=None, description="Reference to DataElement.")
    filter: str | None = Field(default=None, description="Length/value max=2147483647.")
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet.")
    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")
