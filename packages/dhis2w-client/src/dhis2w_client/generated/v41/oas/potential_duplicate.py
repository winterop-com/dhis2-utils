"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .sharing import Sharing
    from .translation import Translation


class PotentialDuplicateCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PotentialDuplicateLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PotentialDuplicateUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PotentialDuplicate(_BaseModel):
    """OpenAPI schema `PotentialDuplicate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: PotentialDuplicateCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    createdByUserName: str | None = None
    displayName: str | None = None
    duplicate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: PotentialDuplicateLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    lastUpdatedByUserName: str | None = None
    name: str | None = None
    original: str | None = None
    sharing: Sharing | None = None
    status: str | None = None
    translations: list[Translation] | None = None
    user: PotentialDuplicateUser | None = _Field(default=None, description="A UID reference to a User  ")
