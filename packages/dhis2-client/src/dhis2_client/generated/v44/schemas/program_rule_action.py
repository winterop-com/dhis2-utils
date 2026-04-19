"""Generated ProgramRuleAction model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import ProgramRuleActionEvaluationTime, ProgramRuleActionType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramRuleAction(BaseModel):
    """DHIS2 Program Rule Action - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/programRuleActions.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attribute: Reference | None = Field(
        default=None, description="Reference to TrackedEntityAttribute. Read-only (inverse side)."
    )

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = None

    content: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    data: str | None = None

    dataElement: Reference | None = Field(
        default=None, description="Reference to DataElement. Read-only (inverse side)."
    )

    displayContent: str | None = None

    displayName: str | None = None

    evaluationEnvironments: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    location: str | None = None

    name: str | None = None

    option: Reference | None = Field(default=None, description="Reference to Option. Read-only (inverse side).")

    optionGroup: Reference | None = Field(
        default=None, description="Reference to OptionGroup. Read-only (inverse side)."
    )

    priority: int | None = None

    programIndicator: Reference | None = Field(
        default=None, description="Reference to ProgramIndicator. Read-only (inverse side)."
    )

    programRule: Reference | None = Field(
        default=None, description="Reference to ProgramRule. Read-only (inverse side)."
    )

    programRuleActionEvaluationTime: ProgramRuleActionEvaluationTime | None = None

    programRuleActionType: ProgramRuleActionType | None = None

    programStage: Reference | None = Field(
        default=None, description="Reference to ProgramStage. Read-only (inverse side)."
    )

    programStageSection: Reference | None = Field(
        default=None, description="Reference to ProgramStageSection. Read-only (inverse side)."
    )

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    templateUid: str | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
