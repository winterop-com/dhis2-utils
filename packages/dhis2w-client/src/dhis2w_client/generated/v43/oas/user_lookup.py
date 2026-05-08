"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class UserLookup(_BaseModel):
    """OpenAPI schema `UserLookup`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    displayName: str | None = None
    firstName: str | None = None
    groups: list[str] | None = None
    id: str | None = None
    roles: list[str] | None = None
    surname: str | None = None
    username: str | None = None
