"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .program_params import ProgramParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .translation import Translation


class ProgramTrackedEntityAttributeDimensionItemParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeDimensionItemParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeDimensionItemParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemParamsLegendSet(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeDimensionItemParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeDimensionItemParams(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeDimensionItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: TrackedEntityAttributeParams | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramTrackedEntityAttributeDimensionItemParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramTrackedEntityAttributeDimensionItemParamsLastUpdatedBy | None = None
    legendSet: ProgramTrackedEntityAttributeDimensionItemParamsLegendSet | None = None
    program: ProgramParams | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
