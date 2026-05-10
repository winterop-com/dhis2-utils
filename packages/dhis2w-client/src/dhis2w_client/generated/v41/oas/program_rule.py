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


class ProgramRuleCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleProgramRuleActions(_BaseModel):
    """A UID reference to a ProgramRuleAction  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRuleUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramRule(_BaseModel):
    """OpenAPI schema `ProgramRule`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    condition: str | None = None
    created: datetime | None = None
    createdBy: ProgramRuleCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramRuleLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    priority: int | None = None
    program: ProgramRuleProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programRuleActions: list[ProgramRuleProgramRuleActions] | None = None
    programStage: ProgramRuleProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: ProgramRuleUser | None = _Field(default=None, description="A UID reference to a User  ")
