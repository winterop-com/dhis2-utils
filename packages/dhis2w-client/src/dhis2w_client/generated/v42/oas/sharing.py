"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .user_access import UserAccess
    from .user_group_access import UserGroupAccess


class Sharing(_BaseModel):
    """OpenAPI schema `Sharing`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    external: bool | None = None
    owner: str | None = None
    public: str | None = None
    userGroups: dict[str, UserGroupAccess] | None = None
    users: dict[str, UserAccess] | None = None
