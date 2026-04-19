"""Generated Section model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Section(BaseModel):
    """DHIS2 Section - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/sections.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    categoryCombos: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataElements: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    dataSet: Reference | None = Field(default=None, description="Reference to DataSet. Read-only (inverse side).")

    description: str | None = None

    disableDataElementAutoGroup: bool | None = None

    displayName: str | None = None

    displayOptions: str | None = None

    greyedFields: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    indicators: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    name: str | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    showColumnTotals: bool | None = None

    showRowTotals: bool | None = None

    sortOrder: int | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
