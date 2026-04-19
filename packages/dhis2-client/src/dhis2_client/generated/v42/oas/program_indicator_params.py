"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, AnalyticsType

if TYPE_CHECKING:
    from .analytics_period_boundary_params import AnalyticsPeriodBoundaryParams
    from .attribute_value_params import AttributeValueParams
    from .category_combo_params import CategoryComboParams
    from .object_style import ObjectStyle
    from .program_params import ProgramParams
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ProgramIndicatorParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ProgramIndicatorParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ProgramIndicatorParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorParamsLegendSet(_BaseModel):
    """OpenAPI schema `ProgramIndicatorParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorParamsLegendSets(_BaseModel):
    """OpenAPI schema `ProgramIndicatorParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorParamsProgramIndicatorGroups(_BaseModel):
    """OpenAPI schema `ProgramIndicatorParamsProgramIndicatorGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ProgramIndicatorParams(_BaseModel):
    """OpenAPI schema `ProgramIndicatorParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregateExportDataElement: str | None = None
    aggregationType: AggregationType
    analyticsPeriodBoundaries: list[AnalyticsPeriodBoundaryParams] | None = None
    analyticsType: AnalyticsType
    attributeCombo: CategoryComboParams | None = None
    attributeValues: list[AttributeValueParams] | None = None
    categoryCombo: CategoryComboParams | None = None
    categoryMappingIds: list[str] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ProgramIndicatorParamsCreatedBy | None = None
    decimals: int | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayInForm: bool | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    expression: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filter: str | None = None
    formName: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ProgramIndicatorParamsLastUpdatedBy | None = None
    legendSet: ProgramIndicatorParamsLegendSet | None = None
    legendSets: list[ProgramIndicatorParamsLegendSets] | None = None
    name: str | None = None
    orgUnitField: str | None = None
    program: ProgramParams | None = None
    programIndicatorGroups: list[ProgramIndicatorParamsProgramIndicatorGroups] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
