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


class ProgramRuleVariableCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableTrackedEntityAttribute(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariableUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleVariable(_BaseModel):
    """OpenAPI schema `ProgramRuleVariable`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramRuleVariableCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataElement: ProgramRuleVariableDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramRuleVariableLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    program: ProgramRuleVariableProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programRuleVariableSourceType: str | None = None
    programStage: ProgramRuleVariableProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    sharing: Sharing | None = None
    trackedEntityAttribute: ProgramRuleVariableTrackedEntityAttribute | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
    translations: list[Translation] | None = None
    useCodeForOptionSet: bool | None = None
    user: ProgramRuleVariableUser | None = _Field(default=None, description="A UID reference to a User  ")
    valueType: str | None = None
