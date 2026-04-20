"""Generated CategoryOptionGroupSetDimension model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class CategoryOptionGroupSetDimension(BaseModel):
    """Generated model for DHIS2 `CategoryOptionGroupSetDimension`.

    DHIS2 Category Option Group Set Dimension - DHIS2 resource (generated from /api/schemas at DHIS2 v43).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    categoryOptionGroups: list[Reference] | None = Field(default=None, description="Collection of CategoryOptionGroup.")
    dimension: Reference | None = Field(default=None, description="Reference to CategoryOptionGroupSet.")
