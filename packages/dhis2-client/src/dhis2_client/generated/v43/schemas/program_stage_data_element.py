"""Generated ProgramStageDataElement model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class ProgramStageDataElement(BaseModel):
    """Generated model for DHIS2 `ProgramStageDataElement`.

    DHIS2 Program Stage Data Element - DHIS2 resource (generated from /api/schemas at DHIS2 v43).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    allowFutureDate: bool | None = None
    allowProvidedElsewhere: bool | None = None
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    compulsory: bool | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dataElement: Reference | None = Field(default=None, description="Reference to DataElement.")
    displayInReports: bool | None = None
    displayName: str | None = Field(default=None, description="Read-only.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")
    renderOptionsAsRadio: bool | None = None
    renderType: Any | None = Field(default=None, description="Reference to DeviceRenderTypeMap. Length/value max=255.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    skipAnalytics: bool | None = None
    skipSynchronization: bool | None = None
    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")
    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
