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
    from .user_credentials_dto import UserCredentialsDto
    from .user_settings import UserSettings


class UserAvatar(_BaseModel):
    """A UID reference to a FileResource  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserCatDimensionConstraints(_BaseModel):
    """A UID reference to a Category  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserCogsDimensionConstraints(_BaseModel):
    """A UID reference to a CategoryOptionGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserDataViewOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserTeiSearchOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserUserGroups(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserUserRoles(_BaseModel):
    """A UID reference to a UserRole  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class User(_BaseModel):
    """OpenAPI schema `User`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    accountExpiry: datetime | None = None
    attributeValues: list[AttributeValue] | None = None
    avatar: UserAvatar | None = _Field(default=None, description="A UID reference to a FileResource  ")
    birthday: datetime | None = None
    catDimensionConstraints: list[UserCatDimensionConstraints] | None = None
    code: str | None = None
    cogsDimensionConstraints: list[UserCogsDimensionConstraints] | None = None
    created: datetime | None = None
    createdBy: UserCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataViewMaxOrganisationUnitLevel: int | None = None
    dataViewOrganisationUnits: list[UserDataViewOrganisationUnits] | None = None
    disabled: bool | None = None
    displayName: str | None = None
    education: str | None = None
    email: str | None = None
    employer: str | None = None
    externalAuth: bool | None = None
    facebookMessenger: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    firstName: str | None = None
    gender: str | None = None
    href: str | None = None
    id: str | None = None
    interests: str | None = None
    introduction: str | None = None
    invitation: bool | None = None
    jobTitle: str | None = None
    languages: str | None = None
    lastCheckedInterpretations: datetime | None = None
    lastLogin: datetime | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    ldapId: str | None = None
    nationality: str | None = None
    openId: str | None = None
    organisationUnits: list[UserOrganisationUnits] | None = None
    password: str | None = None
    passwordLastUpdated: datetime | None = None
    phoneNumber: str | None = None
    selfRegistered: bool | None = None
    settings: UserSettings | None = None
    sharing: Sharing | None = None
    skype: str | None = None
    surname: str | None = None
    teiSearchOrganisationUnits: list[UserTeiSearchOrganisationUnits] | None = None
    telegram: str | None = None
    translations: list[Translation] | None = None
    twitter: str | None = None
    twoFactorEnabled: bool | None = None
    user: UserUser | None = _Field(default=None, description="A UID reference to a User  ")
    userCredentials: UserCredentialsDto | None = None
    userGroups: list[UserUserGroups] | None = None
    userRoles: list[UserUserRoles] | None = None
    username: str | None = None
    welcomeMessage: str | None = None
    whatsApp: str | None = None
