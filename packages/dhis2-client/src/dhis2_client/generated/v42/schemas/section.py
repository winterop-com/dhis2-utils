"""Generated Section model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class Section(BaseModel):
    """Generated model for DHIS2 `Section`.

    DHIS2 Section - persisted metadata (generated from /api/schemas at DHIS2 v42).


    API endpoint: /api/sections.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")

    categoryCombos: list[Any] | None = Field(
        default=None, description="Collection of CategoryCombo. Read-only (inverse side)."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataElements: list[Any] | None = Field(default=None, description="Collection of DataElement.")

    dataSet: Reference | None = Field(default=None, description="Reference to DataSet.")

    description: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    disableDataElementAutoGroup: bool | None = None

    displayName: str | None = Field(default=None, description="Read-only.")

    displayOptions: str | None = Field(default=None, description="Length/value max=50000.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    greyedFields: list[Any] | None = Field(default=None, description="Collection of DataElementOperand.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    indicators: list[Any] | None = Field(default=None, description="Collection of Indicator.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    showColumnTotals: bool | None = None

    showRowTotals: bool | None = None

    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
