"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class UserMessageUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class UserMessage(_BaseModel):
    """OpenAPI schema `UserMessage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    followUp: bool | None = None
    key: str | None = None
    read: bool | None = None
    user: UserMessageUser | None = _Field(default=None, description="A UID reference to a User  ")
