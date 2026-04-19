"""Generated ProgramStageDataElement model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class ProgramStageDataElement(BaseModel):
    """Generated model for DHIS2 `ProgramStageDataElement`.

    DHIS2 Program Stage Data Element - DHIS2 resource (generated from /api/schemas at DHIS2 v44).




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

    code: str | None = None

    compulsory: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataElement: Reference | None = Field(
        default=None, description="Reference to DataElement. Read-only (inverse side)."
    )

    displayInReports: bool | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    name: str | None = None

    programStage: Reference | None = Field(
        default=None, description="Reference to ProgramStage. Read-only (inverse side)."
    )

    renderOptionsAsRadio: bool | None = None

    renderType: Any | None = Field(
        default=None, description="Reference to DeviceRenderTypeMap. Read-only (inverse side)."
    )

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    skipAnalytics: bool | None = None

    skipSynchronization: bool | None = None

    sortOrder: int | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
