"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .relationship_constraint_params import RelationshipConstraintParams
    from .sharing import Sharing
    from .translation import Translation


class RelationshipTypeParamsCreatedBy(_BaseModel):
    """OpenAPI schema `RelationshipTypeParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipTypeParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `RelationshipTypeParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipTypeParams(_BaseModel):
    """OpenAPI schema `RelationshipTypeParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    bidirectional: bool | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: RelationshipTypeParamsCreatedBy | None = None
    description: str | None = None
    displayFromToName: str | None = None
    displayName: str | None = None
    displayToFromName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fromConstraint: RelationshipConstraintParams | None = None
    fromToName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: RelationshipTypeParamsLastUpdatedBy | None = None
    name: str | None = None
    referral: bool | None = None
    sharing: Sharing | None = None
    toConstraint: RelationshipConstraintParams | None = None
    toFromName: str | None = None
    translations: list[Translation] | None = None
