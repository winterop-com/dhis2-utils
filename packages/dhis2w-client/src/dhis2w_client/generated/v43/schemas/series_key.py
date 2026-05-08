"""Generated SeriesKey model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SeriesKey(BaseModel):
    """Generated model for DHIS2 `SeriesKey`.

    DHIS2 Series Key - DHIS2 resource (generated from /api/schemas at DHIS2 v43).

    Transient — not stored in the DHIS2 database (computed / projection).

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    hidden: bool | None = None
    label: Any | None = Field(default=None, description="Reference to StyledObject. Read-only (inverse side).")
