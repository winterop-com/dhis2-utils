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
    from .relationship_constraint import RelationshipConstraint
    from .sharing import Sharing
    from .translation import Translation


class RelationshipTypeCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipTypeLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipTypeUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipType(_BaseModel):
    """OpenAPI schema `RelationshipType`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    bidirectional: bool | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: RelationshipTypeCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    displayFromToName: str | None = None
    displayName: str | None = None
    displayToFromName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fromConstraint: RelationshipConstraint | None = None
    fromToName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: RelationshipTypeLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    name: str | None = None
    referral: bool | None = None
    sharing: Sharing | None = None
    toConstraint: RelationshipConstraint | None = None
    toFromName: str | None = None
    translations: list[Translation] | None = None
    user: RelationshipTypeUser | None = _Field(default=None, description="A UID reference to a User  ")
