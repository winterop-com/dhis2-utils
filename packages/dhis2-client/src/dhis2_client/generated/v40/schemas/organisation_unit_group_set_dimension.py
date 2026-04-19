"""Generated OrganisationUnitGroupSetDimension model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class OrganisationUnitGroupSetDimension(BaseModel):
    """Generated model for DHIS2 `OrganisationUnitGroupSetDimension`.

    DHIS2 Organisation Unit Group Set Dimension - DHIS2 resource (generated from /api/schemas at DHIS2 v40).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dimension: Reference | None = Field(default=None, description="Reference to OrganisationUnitGroupSet.")
    organisationUnitGroups: list[Reference] | None = Field(
        default=None, description="Collection of OrganisationUnitGroup."
    )
