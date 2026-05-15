"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class SqlViewCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SqlViewLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SqlViewUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SqlView(_BaseModel):
    """OpenAPI schema `SqlView`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    cacheStrategy: (
        Literal[
            "NO_CACHE",
            "CACHE_1_MINUTE",
            "CACHE_5_MINUTES",
            "CACHE_10_MINUTES",
            "CACHE_15_MINUTES",
            "CACHE_30_MINUTES",
            "CACHE_1_HOUR",
            "CACHE_6AM_TOMORROW",
            "CACHE_TWO_WEEKS",
            "RESPECT_SYSTEM_SETTING",
        ]
        | None
    ) = None
    code: str | None = None
    created: datetime | None = None
    createdBy: SqlViewCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: SqlViewLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    sharing: Sharing | None = None
    sqlQuery: str | None = None
    translations: list[Translation] | None = None
    type: Literal["VIEW", "MATERIALIZED_VIEW", "QUERY"] | None = None
    updateJobId: str | None = None
    user: SqlViewUser | None = _Field(default=None, description="A UID reference to a User  ")
