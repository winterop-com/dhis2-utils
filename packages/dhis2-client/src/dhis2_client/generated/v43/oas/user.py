"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .file_resource import FileResource
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class User(_BaseModel):
    """OpenAPI schema `User`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    accountExpiry: datetime | None = None
    attributeValues: list[AttributeValue] | None = None
    avatar: FileResource | None = None
    birthday: datetime | None = None
    catDimensionConstraints: list[BaseIdentifiableObject] | None = None
    code: str | None = None
    cogsDimensionConstraints: list[BaseIdentifiableObject] | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataViewMaxOrganisationUnitLevel: int | None = None
    dataViewOrganisationUnits: list[BaseIdentifiableObject] | None = None
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
    lastUpdatedBy: UserDto | None = None
    ldapId: str | None = None
    name: str | None = None
    nationality: str | None = None
    openId: str | None = None
    organisationUnits: list[BaseIdentifiableObject] | None = None
    password: str | None = None
    passwordLastUpdated: datetime | None = None
    phoneNumber: str | None = None
    selfRegistered: bool | None = None
    settings: dict[str, str] | None = None
    sharing: Sharing | None = None
    skype: str | None = None
    surname: str | None = None
    teiSearchOrganisationUnits: list[BaseIdentifiableObject] | None = None
    telegram: str | None = None
    translations: list[Translation] | None = None
    twitter: str | None = None
    userGroups: list[BaseIdentifiableObject] | None = None
    userRoles: list[BaseIdentifiableObject] | None = None
    username: str | None = None
    verifiedEmail: str | None = None
    welcomeMessage: str | None = None
    whatsApp: str | None = None
