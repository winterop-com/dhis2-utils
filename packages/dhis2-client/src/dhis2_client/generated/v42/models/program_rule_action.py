"""Generated ProgramRuleAction model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramRuleAction(BaseModel):
    """DHIS2 ProgramRuleAction resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    attribute: Reference | None = None

    attributeValues: Any | None = None

    code: str | None = None

    content: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    data: str | None = None

    dataElement: Reference | None = None

    displayContent: str | None = None

    displayName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    location: str | None = None

    name: str | None = None

    option: Reference | None = None

    optionGroup: Reference | None = None

    programIndicator: Reference | None = None

    programRule: Reference | None = None

    programRuleActionEvaluationEnvironments: list[Any] | None = None

    programRuleActionEvaluationTime: str | None = None

    programRuleActionType: str | None = None

    programStage: Reference | None = None

    programStageSection: Reference | None = None

    sharing: Any | None = None

    templateUid: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
