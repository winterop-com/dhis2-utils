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
    from .program_stage_query_criteria import ProgramStageQueryCriteria
    from .sharing import Sharing
    from .translation import Translation


class ProgramStageWorkingListCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageWorkingListLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageWorkingListProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageWorkingListProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageWorkingListUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageWorkingList(_BaseModel):
    """OpenAPI schema `ProgramStageWorkingList`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramStageWorkingListCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayDescription: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramStageWorkingListLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    program: ProgramStageWorkingListProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programStage: ProgramStageWorkingListProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    programStageQueryCriteria: ProgramStageQueryCriteria | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    user: ProgramStageWorkingListUser | None = _Field(default=None, description="A UID reference to a User  ")
