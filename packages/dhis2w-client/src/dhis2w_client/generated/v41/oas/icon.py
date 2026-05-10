"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class IconCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class IconFileResource(_BaseModel):
    """A UID reference to a FileResource  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Icon(_BaseModel):
    """OpenAPI schema `Icon`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    createdBy: IconCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    custom: bool | None = None
    description: str | None = None
    fileResource: IconFileResource | None = _Field(default=None, description="A UID reference to a FileResource  ")
    href: str | None = None
    key: str | None = None
    keywords: list[str] | None = None
    lastUpdated: datetime | None = None
