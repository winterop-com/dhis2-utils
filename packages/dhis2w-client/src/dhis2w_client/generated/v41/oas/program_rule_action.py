"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class ProgramRuleActionCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionOption(_BaseModel):
    """A UID reference to a Option  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionOptionGroup(_BaseModel):
    """A UID reference to a OptionGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionProgramIndicator(_BaseModel):
    """A UID reference to a ProgramIndicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionProgramRule(_BaseModel):
    """A UID reference to a ProgramRule  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionProgramStageSection(_BaseModel):
    """A UID reference to a ProgramStageSection  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionTrackedEntityAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleActionUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleAction(_BaseModel):
    """OpenAPI schema `ProgramRuleAction`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    content: str | None = None
    created: datetime | None = None
    createdBy: ProgramRuleActionCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    data: str | None = None
    dataElement: ProgramRuleActionDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    displayContent: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramRuleActionLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    location: str | None = None
    name: str | None = None
    option: ProgramRuleActionOption | None = _Field(default=None, description="A UID reference to a Option  ")
    optionGroup: ProgramRuleActionOptionGroup | None = _Field(
        default=None, description="A UID reference to a OptionGroup  "
    )
    programIndicator: ProgramRuleActionProgramIndicator | None = _Field(
        default=None, description="A UID reference to a ProgramIndicator  "
    )
    programRule: ProgramRuleActionProgramRule | None = _Field(
        default=None, description="A UID reference to a ProgramRule  "
    )
    programRuleActionEvaluationEnvironments: list[str] | None = None
    programRuleActionEvaluationTime: str | None = None
    programRuleActionType: str | None = None
    programStage: ProgramRuleActionProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    programStageSection: ProgramRuleActionProgramStageSection | None = _Field(
        default=None, description="A UID reference to a ProgramStageSection  "
    )
    sharing: Sharing | None = None
    templateUid: str | None = None
    trackedEntityAttribute: ProgramRuleActionTrackedEntityAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
    translations: list[Translation] | None = None
    user: ProgramRuleActionUser | None = _Field(default=None, description="A UID reference to a User  ")
