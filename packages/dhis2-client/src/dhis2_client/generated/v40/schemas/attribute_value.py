"""Generated AttributeValue model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class AttributeValue(BaseModel):
    """Generated model for DHIS2 `AttributeValue`.

    DHIS2 Attribute Value - DHIS2 resource (generated from /api/schemas at DHIS2 v40).

    Transient — not stored in the DHIS2 database (computed / projection).

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    attribute: Reference | None = Field(default=None, description="Reference to Attribute. Read-only (inverse side).")
    value: str | None = Field(default=None, description="Length/value max=2147483647.")
