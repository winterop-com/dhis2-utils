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
    from .option_params import OptionParams
    from .program_params import ProgramParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .translation import Translation


class ProgramTrackedEntityAttributeOptionDimensionItemParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeOptionDimensionItemParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeOptionDimensionItemParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeOptionDimensionItemParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeOptionDimensionItemParamsLegendSet(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeOptionDimensionItemParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramTrackedEntityAttributeOptionDimensionItemParams(_BaseModel):
    """OpenAPI schema `ProgramTrackedEntityAttributeOptionDimensionItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: TrackedEntityAttributeParams | None = None
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramTrackedEntityAttributeOptionDimensionItemParamsCreatedBy | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramTrackedEntityAttributeOptionDimensionItemParamsLastUpdatedBy | None = None
    legendSet: ProgramTrackedEntityAttributeOptionDimensionItemParamsLegendSet | None = None
    option: OptionParams | None = None
    program: ProgramParams | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
