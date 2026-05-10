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
    from .sharing import Sharing
    from .translation import Translation


class ProgramStageDataElementCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataElementDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataElementLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataElementProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataElementUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramStageDataElement(_BaseModel):
    """OpenAPI schema `ProgramStageDataElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    allowFutureDate: bool | None = None
    allowProvidedElsewhere: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    compulsory: bool | None = None
    created: datetime | None = None
    createdBy: ProgramStageDataElementCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataElement: ProgramStageDataElementDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    displayInReports: bool | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramStageDataElementLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    programStage: ProgramStageDataElementProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    renderOptionsAsRadio: bool | None = None
    renderType: Any | None = _Field(default=None, description="The exact type is unknown.  ")
    sharing: Sharing | None = None
    skipAnalytics: bool | None = None
    skipSynchronization: bool | None = None
    sortOrder: int | None = None
    translations: list[Translation] | None = None
    user: ProgramStageDataElementUser | None = _Field(default=None, description="A UID reference to a User  ")
