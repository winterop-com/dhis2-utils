"""Generated DataApprovalWorkflow model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import PeriodType


class DataApprovalWorkflow(BaseModel):
    """Generated model for DHIS2 `DataApprovalWorkflow`.

    DHIS2 Data Approval Workflow - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/dataApprovalWorkflows.

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
    categoryCombo: Reference | None = Field(default=None, description="Reference to CategoryCombo.")
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dataApprovalLevels: list[Any] | None = Field(default=None, description="Collection of DataApprovalLevel.")
    dataSets: list[Any] | None = Field(default=None, description="Collection of DataSet. Read-only (inverse side).")
    displayName: str | None = Field(default=None, description="Read-only.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")
    periodType: PeriodType | None = Field(default=None, description="Reference to PeriodType. Length/value max=255.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
