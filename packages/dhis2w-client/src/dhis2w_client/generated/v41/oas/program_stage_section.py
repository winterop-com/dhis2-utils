"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .object_style import ObjectStyle
    from .sharing import Sharing
    from .translation import Translation


class ProgramStageSectionCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageSectionDataElements(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageSectionLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageSectionProgramIndicators(_BaseModel):
    """A UID reference to a ProgramIndicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageSectionProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageSectionUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageSection(_BaseModel):
    """OpenAPI schema `ProgramStageSection`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramStageSectionCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataElements: list[ProgramStageSectionDataElements] | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramStageSectionLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    programIndicators: list[ProgramStageSectionProgramIndicators] | None = None
    programStage: ProgramStageSectionProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    renderType: Any | None = _Field(default=None, description="The exact type is unknown.  ")
    sharing: Sharing | None = None
    shortName: str | None = None
    sortOrder: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    user: ProgramStageSectionUser | None = _Field(default=None, description="A UID reference to a User  ")
