"""Generated ProgramRuleAction model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import ProgramRuleActionEvaluationTime, ProgramRuleActionType


class ProgramRuleAction(BaseModel):
    """Generated model for DHIS2 `ProgramRuleAction`.

    DHIS2 Program Rule Action - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/programRuleActions.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    attribute: Reference | None = Field(default=None, description="Reference to TrackedEntityAttribute.")
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    content: str | None = Field(default=None, description="Length/value max=2147483647.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    data: str | None = Field(default=None, description="Length/value max=2147483647.")
    dataElement: Reference | None = Field(default=None, description="Reference to DataElement.")
    displayContent: str | None = Field(default=None, description="Read-only.")
    displayName: str | None = Field(default=None, description="Read-only.")
    evaluationEnvironments: list[Any] | None = Field(
        default=None, description="Collection of ProgramRuleActionEvaluationEnvironment. Length/value max=255."
    )
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    location: str | None = Field(default=None, description="Length/value max=255.")
    name: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    option: Reference | None = Field(default=None, description="Reference to Option.")
    optionGroup: Reference | None = Field(default=None, description="Reference to OptionGroup.")
    programIndicator: Reference | None = Field(default=None, description="Reference to ProgramIndicator.")
    programRule: Reference | None = Field(default=None, description="Reference to ProgramRule.")
    programRuleActionEvaluationTime: ProgramRuleActionEvaluationTime | None = None
    programRuleActionType: ProgramRuleActionType | None = None
    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")
    programStageSection: Reference | None = Field(default=None, description="Reference to ProgramStageSection.")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    templateUid: str | None = Field(default=None, description="Length/value max=2147483647.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
