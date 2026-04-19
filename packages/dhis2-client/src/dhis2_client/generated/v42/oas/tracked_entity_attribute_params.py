"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, ValueType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .object_style import ObjectStyle
    from .option_set_params import OptionSetParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class TrackedEntityAttributeParamsCreatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeParamsLegendSet(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeParamsLegendSets(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityAttributeParams(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    confidential: bool | None = None
    created: datetime | None = None
    createdBy: TrackedEntityAttributeParamsCreatedBy | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayInListNoProgram: bool | None = None
    displayName: str | None = None
    displayOnVisitSchedule: bool | None = None
    displayShortName: str | None = None
    expression: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldMask: str | None = None
    formName: str | None = None
    generated: bool | None = None
    id: str | None = None
    inherit: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: TrackedEntityAttributeParamsLastUpdatedBy | None = None
    legendSet: TrackedEntityAttributeParamsLegendSet | None = None
    legendSets: list[TrackedEntityAttributeParamsLegendSets] | None = None
    name: str | None = None
    optionSet: OptionSetParams | None = None
    optionSetValue: bool | None = None
    orgunitScope: bool | None = None
    pattern: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipSynchronization: bool | None = None
    sortOrderInListNoProgram: int | None = None
    sortOrderInVisitSchedule: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    unique: bool | None = None
    valueType: ValueType | None = None
