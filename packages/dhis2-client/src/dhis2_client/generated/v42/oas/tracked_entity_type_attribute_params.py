"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .tracked_entity_type_params import TrackedEntityTypeParams
    from .translation import Translation


class TrackedEntityTypeAttributeParamsCreatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityTypeAttributeParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class TrackedEntityTypeAttributeParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityTypeAttributeParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class TrackedEntityTypeAttributeParams(_BaseModel):
    """OpenAPI schema `TrackedEntityTypeAttributeParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: TrackedEntityTypeAttributeParamsCreatedBy | None = None
    displayInList: bool | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: TrackedEntityTypeAttributeParamsLastUpdatedBy | None = None
    mandatory: bool | None = None
    searchable: bool | None = None
    sharing: Sharing | None = None
    trackedEntityAttribute: TrackedEntityAttributeParams | None = None
    trackedEntityType: TrackedEntityTypeParams | None = None
    translations: list[Translation] | None = None
    valueType: ValueType
