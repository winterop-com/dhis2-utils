"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .program_params import ProgramParams
    from .sharing import Sharing
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .translation import Translation


class ProgramTrackedEntityAttributeParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeParams(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    allowFutureDate: bool | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramTrackedEntityAttributeParamsCreatedBy | None = None
    displayInList: bool | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramTrackedEntityAttributeParamsLastUpdatedBy | None = None
    mandatory: bool | None = None
    program: ProgramParams | None = None
    renderOptionsAsRadio: bool | None = None
    renderType: Any | None = None
    searchable: bool | None = None
    sharing: Sharing | None = None
    skipIndividualAnalytics: bool | None = None
    sortOrder: int | None = None
    trackedEntityAttribute: TrackedEntityAttributeParams | None = None
    translations: list[Translation] | None = None
    valueType: ValueType | None = None
