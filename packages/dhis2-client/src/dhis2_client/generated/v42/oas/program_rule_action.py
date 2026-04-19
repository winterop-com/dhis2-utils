"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ProgramRuleActionEvaluationEnvironment, ProgramRuleActionEvaluationTime, ProgramRuleActionType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .option import Option
    from .option_group import OptionGroup
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class ProgramRuleAction(_BaseModel):
    """OpenAPI schema `ProgramRuleAction`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    content: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    data: str | None = None
    dataElement: BaseIdentifiableObject | None = None
    displayContent: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    location: str | None = None
    name: str | None = None
    option: Option | None = None
    optionGroup: OptionGroup | None = None
    programIndicator: BaseIdentifiableObject | None = None
    programRule: BaseIdentifiableObject | None = None
    programRuleActionEvaluationEnvironments: list[ProgramRuleActionEvaluationEnvironment] | None = None
    programRuleActionEvaluationTime: ProgramRuleActionEvaluationTime
    programRuleActionType: ProgramRuleActionType
    programStage: BaseIdentifiableObject | None = None
    programStageSection: BaseIdentifiableObject | None = None
    sharing: Sharing | None = None
    templateUid: str | None = None
    trackedEntityAttribute: BaseIdentifiableObject | None = None
    translations: list[Translation] | None = None
