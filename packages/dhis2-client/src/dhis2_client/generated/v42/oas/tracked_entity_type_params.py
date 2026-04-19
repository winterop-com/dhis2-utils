"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import FeatureType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .object_style import ObjectStyle
    from .sharing import Sharing
    from .tracked_entity_type_attribute_params import TrackedEntityTypeAttributeParams
    from .translation import Translation


class TrackedEntityTypeParamsCreatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityTypeParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class TrackedEntityTypeParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityTypeParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class TrackedEntityTypeParams(_BaseModel):
    """OpenAPI schema `TrackedEntityTypeParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    allowAuditLog: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: TrackedEntityTypeParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    featureType: FeatureType
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: TrackedEntityTypeParamsLastUpdatedBy | None = None
    maxTeiCountToReturn: int
    minAttributesRequiredToSearch: int
    name: str | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    trackedEntityTypeAttributes: list[TrackedEntityTypeAttributeParams] | None = None
    translations: list[Translation] | None = None
