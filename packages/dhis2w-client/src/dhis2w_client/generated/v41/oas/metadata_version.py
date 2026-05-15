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


class MetadataVersionCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MetadataVersionLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MetadataVersionUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MetadataVersion(_BaseModel):
    """OpenAPI schema `MetadataVersion`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: MetadataVersionCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    hashCode: str | None = None
    href: str | None = None
    id: str | None = None
    importDate: datetime | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: MetadataVersionLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    type: Literal["BEST_EFFORT", "ATOMIC"] | None = None
    user: MetadataVersionUser | None = _Field(default=None, description="A UID reference to a User  ")
