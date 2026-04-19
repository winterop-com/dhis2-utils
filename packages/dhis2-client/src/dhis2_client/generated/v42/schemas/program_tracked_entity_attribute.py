"""Generated ProgramTrackedEntityAttribute model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import ValueType


class ProgramTrackedEntityAttribute(BaseModel):
    """Generated model for DHIS2 `ProgramTrackedEntityAttribute`.

    DHIS2 Program Tracked Entity Attribute - DHIS2 resource (generated from /api/schemas at DHIS2 v42).




    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    allowFutureDate: bool | None = None

    attribute: Reference | None = Field(default=None, description="Reference to TrackedEntityAttribute.")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    displayInList: bool | None = None

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    mandatory: bool | None = None

    name: str | None = Field(default=None, description="Length/value max=2147483647.")

    program: Reference | None = Field(default=None, description="Reference to Program.")

    renderOptionsAsRadio: bool | None = None

    renderType: Any | None = Field(default=None, description="Reference to DeviceRenderTypeMap. Length/value max=255.")

    searchable: bool | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    skipIndividualAnalytics: bool | None = None

    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    valueType: ValueType | None = Field(default=None, description="Read-only.")
