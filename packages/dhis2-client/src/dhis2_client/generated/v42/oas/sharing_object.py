"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .sharing_user import SharingUser
    from .sharing_user_access import SharingUserAccess
    from .sharing_user_group_access import SharingUserGroupAccess


class SharingObject(_BaseModel):
    """OpenAPI schema `SharingObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    displayName: str | None = None
    externalAccess: bool | None = None
    id: str | None = None
    name: str | None = None
    publicAccess: str | None = None
    user: SharingUser | None = None
    userAccesses: list[SharingUserAccess] | None = None
    userGroupAccesses: list[SharingUserGroupAccess] | None = None
