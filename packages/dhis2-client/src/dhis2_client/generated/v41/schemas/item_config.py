"""Generated ItemConfig model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ..enums import Position


class ItemConfig(BaseModel):
    """Generated model for DHIS2 `ItemConfig`.

    DHIS2 Item Config - DHIS2 resource (generated from /api/schemas at DHIS2 v41).



    Transient — not stored in the DHIS2 database (computed / projection).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    insertHeight: int | None = Field(default=None, description="Length/value max=2147483647.")

    insertPosition: Position | None = None
