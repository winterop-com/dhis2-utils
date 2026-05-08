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
    from .object_style import ObjectStyle
    from .relationship_item_params import RelationshipItemParams
    from .relationship_type_params import RelationshipTypeParams
    from .sharing import Sharing
    from .translation import Translation


class RelationshipParamsCreatedBy(_BaseModel):
    """OpenAPI schema `RelationshipParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `RelationshipParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class RelationshipParams(_BaseModel):
    """OpenAPI schema `RelationshipParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdAtClient: datetime | None = None
    createdBy: RelationshipParamsCreatedBy | None = None
    deleted: bool | None = None
    description: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    from_: RelationshipItemParams | None = _Field(default=None, alias="from")
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: RelationshipParamsLastUpdatedBy | None = None
    name: str | None = None
    relationshipType: RelationshipTypeParams | None = None
    sharing: Sharing | None = None
    style: ObjectStyle | None = None
    to: RelationshipItemParams | None = None
    translations: list[Translation] | None = None
