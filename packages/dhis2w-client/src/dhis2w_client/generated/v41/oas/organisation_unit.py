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
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class OrganisationUnitAncestors(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitChildren(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitDataSets(_BaseModel):
    """A UID reference to a DataSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitImage(_BaseModel):
    """A UID reference to a FileResource  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitOrganisationUnitGroups(_BaseModel):
    """A UID reference to a OrganisationUnitGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitParent(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitPrograms(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnit(_BaseModel):
    """OpenAPI schema `OrganisationUnit`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    address: str | None = None
    aggregationType: str | None = None
    ancestors: list[OrganisationUnitAncestors] | None = None
    attributeValues: list[AttributeValue] | None = None
    children: list[OrganisationUnitChildren] | None = None
    closedDate: datetime | None = None
    code: str | None = None
    comment: str | None = None
    contactPerson: str | None = None
    created: datetime | None = None
    createdBy: OrganisationUnitCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataSets: list[OrganisationUnitDataSets] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    email: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    geometry: dict[str, Any] | None = None
    href: str | None = None
    id: str | None = None
    image: OrganisationUnitImage | None = _Field(default=None, description="A UID reference to a FileResource  ")
    lastUpdated: datetime | None = None
    lastUpdatedBy: OrganisationUnitLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    leaf: bool | None = None
    legendSet: OrganisationUnitLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[OrganisationUnitLegendSets] | None = None
    level: int | None = None
    memberCount: int | None = None
    name: str | None = None
    openingDate: datetime | None = None
    organisationUnitGroups: list[OrganisationUnitOrganisationUnitGroups] | None = None
    parent: OrganisationUnitParent | None = _Field(default=None, description="A UID reference to a OrganisationUnit  ")
    path: str | None = None
    phoneNumber: str | None = None
    programs: list[OrganisationUnitPrograms] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    type: str | None = None
    url: str | None = None
    user: OrganisationUnitUser | None = _Field(default=None, description="A UID reference to a User  ")
    users: list[UserDto] | None = None
