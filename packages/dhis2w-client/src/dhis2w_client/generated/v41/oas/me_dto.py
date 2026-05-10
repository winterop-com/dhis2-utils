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
    from .user_access import UserAccess
    from .user_credentials_dto import UserCredentialsDto
    from .user_group_access import UserGroupAccess


class MeDtoAvatar(_BaseModel):
    """A UID reference to a FileResource  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MeDtoDataViewOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MeDtoOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MeDtoPatTokens(_BaseModel):
    """A UID reference to a ApiToken  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MeDtoTeiSearchOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MeDtoUserGroups(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MeDtoUserRoles(_BaseModel):
    """A UID reference to a UserRole  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MeDto(_BaseModel):
    """OpenAPI schema `MeDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    authorities: list[str] | None = None
    avatar: MeDtoAvatar | None = _Field(default=None, description="A UID reference to a FileResource  ")
    birthday: datetime | None = None
    created: datetime | None = None
    dataSets: list[str] | None = None
    dataViewOrganisationUnits: list[MeDtoDataViewOrganisationUnits] | None = None
    displayName: str | None = None
    education: str | None = None
    email: str | None = None
    employer: str | None = None
    externalAccess: bool | None = None
    facebookMessenger: str | None = None
    favorites: list[str] | None = None
    firstName: str | None = None
    gender: str | None = None
    id: str | None = None
    impersonation: str | None = None
    interests: str | None = None
    introduction: str | None = None
    jobTitle: str | None = None
    languages: str | None = None
    lastUpdated: datetime | None = None
    name: str | None = None
    nationality: str | None = None
    organisationUnits: list[MeDtoOrganisationUnits] | None = None
    patTokens: list[MeDtoPatTokens] | None = None
    phoneNumber: str | None = None
    programs: list[str] | None = None
    settings: dict[str, str | float | bool] | None = None
    sharing: Sharing | None = None
    skype: str | None = None
    surname: str | None = None
    teiSearchOrganisationUnits: list[MeDtoTeiSearchOrganisationUnits] | None = None
    telegram: str | None = None
    translations: list[Translation] | None = None
    twitter: str | None = None
    userAccesses: list[UserAccess] | None = None
    userCredentials: UserCredentialsDto | None = None
    userGroupAccesses: list[UserGroupAccess] | None = None
    userGroups: list[MeDtoUserGroups] | None = None
    userRoles: list[MeDtoUserRoles] | None = None
    username: str | None = None
    whatsApp: str | None = None
