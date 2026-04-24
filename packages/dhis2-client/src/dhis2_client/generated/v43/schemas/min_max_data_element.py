"""Generated MinMaxDataElement model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class MinMaxDataElement(BaseModel):
    """Generated model for DHIS2 `MinMaxDataElement`.

    DHIS2 Min Max Data Element - DHIS2 resource (generated from /api/schemas at DHIS2 v43).

    API endpoint: /dev-2-43/api/minMaxDataElements.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    dataElement: Reference | None = Field(default=None, description="Reference to DataElement.")
    generated: bool | None = None
    max: int | None = Field(default=None, description="Length/value max=2147483647.")
    min: int | None = Field(default=None, description="Length/value max=2147483647.")
    optionCombo: Reference | None = Field(default=None, description="Reference to CategoryOptionCombo.")
    source: Reference | None = Field(default=None, description="Reference to OrganisationUnit.")
