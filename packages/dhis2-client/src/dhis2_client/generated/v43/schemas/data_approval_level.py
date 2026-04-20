"""Generated DataApprovalLevel model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference


class DataApprovalLevel(BaseModel):
    """Generated model for DHIS2 `DataApprovalLevel`.

    DHIS2 Data Approval Level - persisted metadata (generated from /api/schemas at DHIS2 v43).

    API endpoint: /dev-2-43/api/dataApprovalLevels.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    categoryOptionGroupSet: Reference | None = Field(default=None, description="Reference to CategoryOptionGroupSet.")
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    displayName: str | None = Field(default=None, description="Read-only.")
    href: str | None = Field(default=None, description="Length/value max=2147483647.")
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    level: int | None = Field(default=None, description="Length/value max=2147483647.")
    name: str | None = Field(default=None, description="Unique. Length/value max=230.")
    orgUnitLevel: int | None = Field(default=None, description="Length/value max=2147483647.")
    orgUnitLevelName: str | None = Field(default=None, description="Length/value max=2147483647.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
