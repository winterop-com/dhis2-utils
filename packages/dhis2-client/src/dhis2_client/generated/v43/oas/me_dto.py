"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import TwoFactorType

if TYPE_CHECKING:
    from .access import Access
    from .api_token import ApiToken
    from .attribute_values import AttributeValues
    from .base_identifiable_object import BaseIdentifiableObject
    from .file_resource import FileResource
    from .sharing import Sharing
    from .translation import Translation
    from .user_access import UserAccess
    from .user_group_access import UserGroupAccess


class MeDto(_BaseModel):
    """OpenAPI schema `MeDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: AttributeValues | None = None
    authorities: list[str] | None = None
    avatar: FileResource | None = None
    birthday: datetime | None = None
    canImpersonate: bool | None = None
    created: datetime | None = None
    dataSets: list[str] | None = None
    dataViewOrganisationUnits: list[BaseIdentifiableObject] | None = None
    displayName: str | None = None
    education: str | None = None
    email: str | None = None
    emailVerified: bool | None = None
    employer: str | None = None
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
    organisationUnits: list[BaseIdentifiableObject] | None = None
    patTokens: list[ApiToken] | None = None
    phoneNumber: str | None = None
    programs: list[str] | None = None
    settings: dict[str, Any] | None = None
    sharing: Sharing | None = None
    skype: str | None = None
    surname: str | None = None
    teiSearchOrganisationUnits: list[BaseIdentifiableObject] | None = None
    telegram: str | None = None
    translations: list[Translation] | None = None
    twitter: str | None = None
    twoFactorType: TwoFactorType | None = None
    userAccesses: list[UserAccess] | None = None
    userGroupAccesses: list[UserGroupAccess] | None = None
    userGroups: list[BaseIdentifiableObject] | None = None
    userRoles: list[BaseIdentifiableObject] | None = None
    username: str | None = None
    whatsApp: str | None = None
