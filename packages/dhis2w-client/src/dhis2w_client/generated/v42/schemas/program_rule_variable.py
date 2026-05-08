"""Generated ProgramRuleVariable model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import ProgramRuleVariableSourceType, ValueType


class ProgramRuleVariable(BaseModel):
    """Generated model for DHIS2 `ProgramRuleVariable`.

    DHIS2 Program Rule Variable - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/programRuleVariables.

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
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dataElement: Reference | None = Field(default=None, description="Reference to DataElement.")
    displayName: str | None = Field(default=None, description="Read-only.")
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    name: str | None = Field(default=None, description="Length/value min=1, max=230.")
    program: Reference | None = Field(default=None, description="Reference to Program.")
    programRuleVariableSourceType: ProgramRuleVariableSourceType | None = None
    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    trackedEntityAttribute: Reference | None = Field(default=None, description="Reference to TrackedEntityAttribute.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    useCodeForOptionSet: bool | None = None
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    valueType: ValueType | None = None
