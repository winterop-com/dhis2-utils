"""Generated LegendDefinitions model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import LegendDisplayStrategy, LegendDisplayStyle


class LegendDefinitions(BaseModel):
    """Generated model for DHIS2 `LegendDefinitions`.

    DHIS2 Legend Definitions - DHIS2 resource (generated from /api/schemas at DHIS2 v44).




    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    legendDisplayStrategy: LegendDisplayStrategy | None = None

    legendDisplayStyle: LegendDisplayStyle | None = None

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    showKey: bool | None = None
