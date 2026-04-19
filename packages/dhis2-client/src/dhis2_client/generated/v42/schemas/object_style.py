"""Generated ObjectStyle model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ObjectStyle(BaseModel):
    """Generated model for DHIS2 `ObjectStyle`.

    DHIS2 Object Style - DHIS2 resource (generated from /api/schemas at DHIS2 v42).



    Transient — not stored in the DHIS2 database (computed / projection).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    color: str | None = Field(default=None, description="Length/value max=2147483647.")

    icon: str | None = Field(default=None, description="Length/value max=2147483647.")
