"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class UserParamsAvatar(_BaseModel):
    """OpenAPI schema `UserParamsAvatar`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsCatDimensionConstraints(_BaseModel):
    """OpenAPI schema `UserParamsCatDimensionConstraints`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsCogsDimensionConstraints(_BaseModel):
    """OpenAPI schema `UserParamsCogsDimensionConstraints`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsCreatedBy(_BaseModel):
    """OpenAPI schema `UserParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsDataViewOrganisationUnits(_BaseModel):
    """OpenAPI schema `UserParamsDataViewOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `UserParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `UserParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsTeiSearchOrganisationUnits(_BaseModel):
    """OpenAPI schema `UserParamsTeiSearchOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsUserGroups(_BaseModel):
    """OpenAPI schema `UserParamsUserGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParamsUserRoles(_BaseModel):
    """OpenAPI schema `UserParamsUserRoles`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class UserParams(_BaseModel):
    """OpenAPI schema `UserParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    accountExpiry: datetime | None = None
    attributeValues: list[AttributeValueParams] | None = None
    avatar: UserParamsAvatar | None = None
    birthday: datetime | None = None
    catDimensionConstraints: list[UserParamsCatDimensionConstraints] | None = None
    code: str | None = None
    cogsDimensionConstraints: list[UserParamsCogsDimensionConstraints] | None = None
    created: datetime | None = None
    createdBy: UserParamsCreatedBy | None = None
    dataViewMaxOrganisationUnitLevel: int | None = None
    dataViewOrganisationUnits: list[UserParamsDataViewOrganisationUnits] | None = None
    disabled: bool | None = None
    displayName: str | None = None
    education: str | None = None
    email: str | None = None
    emailVerificationToken: str | None = None
    emailVerified: bool | None = None
    employer: str | None = None
    externalAuth: bool | None = None
    facebookMessenger: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    firstName: str | None = None
    gender: str | None = None
    id: str | None = None
    interests: str | None = None
    introduction: str | None = None
    invitation: bool | None = None
    jobTitle: str | None = None
    languages: str | None = None
    lastCheckedInterpretations: datetime | None = None
    lastLogin: datetime | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserParamsLastUpdatedBy | None = None
    ldapId: str | None = None
    nationality: str | None = None
    openId: str | None = None
    organisationUnits: list[UserParamsOrganisationUnits] | None = None
    password: str | None = None
    passwordLastUpdated: datetime | None = None
    phoneNumber: str | None = None
    selfRegistered: bool | None = None
    settings: dict[str, str] | None = None
    sharing: Sharing | None = None
    skype: str | None = None
    surname: str | None = None
    teiSearchOrganisationUnits: list[UserParamsTeiSearchOrganisationUnits] | None = None
    telegram: str | None = None
    translations: list[Translation] | None = None
    twitter: str | None = None
    userGroups: list[UserParamsUserGroups] | None = None
    userRoles: list[UserParamsUserRoles] | None = None
    username: str | None = None
    verifiedEmail: str | None = None
    welcomeMessage: str | None = None
    whatsApp: str | None = None
