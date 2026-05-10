"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .access import Access
    from .sharing import Sharing


class UserCredentialsDtoCatDimensionConstraints(_BaseModel):
    """A UID reference to a Category  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserCredentialsDtoCogsDimensionConstraints(_BaseModel):
    """A UID reference to a CategoryOptionGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserCredentialsDtoUserRoles(_BaseModel):
    """A UID reference to a UserRole  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserCredentialsDto(_BaseModel):
    """OpenAPI schema `UserCredentialsDto`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    accountExpiry: datetime | None = None
    catDimensionConstraints: list[UserCredentialsDtoCatDimensionConstraints] | None = None
    cogsDimensionConstraints: list[UserCredentialsDtoCogsDimensionConstraints] | None = None
    disabled: bool | None = None
    externalAuth: bool | None = None
    id: str | None = None
    idToken: str | None = None
    invitation: bool | None = None
    lastLogin: datetime | None = None
    ldapId: str | None = None
    openId: str | None = None
    password: str | None = None
    passwordLastUpdated: datetime | None = None
    previousPasswords: list[str] | None = None
    restoreExpiry: datetime | None = None
    restoreToken: str | None = None
    selfRegistered: bool | None = None
    sharing: Sharing | None = None
    twoFA: bool | None = None
    uid: str | None = None
    userRoles: list[UserCredentialsDtoUserRoles] | None = None
    username: str | None = None
    uuid: str | None = None
