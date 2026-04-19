"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import TwoFactorType

if TYPE_CHECKING:
    from .granted_authority import GrantedAuthority


class UserDetails(_BaseModel):
    """OpenAPI schema `UserDetails`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    accountNonExpired: bool | None = None
    accountNonLocked: bool | None = None
    allAuthorities: list[str] | None = None
    authorities: list[GrantedAuthority] | None = None
    code: str | None = None
    credentialsNonExpired: bool | None = None
    emailVerified: bool | None = None
    enabled: bool | None = None
    externalAuth: bool | None = None
    firstName: str | None = None
    id: int | None = None
    managedGroupLongIds: list[int] | None = None
    password: str | None = None
    secret: str | None = None
    super: bool | None = None
    surname: str | None = None
    twoFactorEnabled: bool | None = None
    twoFactorType: TwoFactorType | None = None
    uid: str | None = None
    userDataOrgUnitIds: list[str] | None = None
    userEffectiveSearchOrgUnitIds: list[str] | None = None
    userGroupIds: list[str] | None = None
    userOrgUnitIds: list[str] | None = None
    userRoleIds: list[str] | None = None
    userRoleLongIds: list[int] | None = None
    userSearchOrgUnitIds: list[str] | None = None
    username: str | None = None
