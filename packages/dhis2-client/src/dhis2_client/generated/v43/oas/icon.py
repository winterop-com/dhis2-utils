"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .user import User


class Icon(_BaseModel):
    """OpenAPI schema `Icon`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    created: datetime | None = None
    createdBy: User | None = None
    custom: bool | None = None
    description: str | None = None
    fileResource: BaseIdentifiableObject | None = None
    href: str | None = None
    key: str | None = None
    keywords: list[str] | None = None
    lastUpdated: datetime | None = None
