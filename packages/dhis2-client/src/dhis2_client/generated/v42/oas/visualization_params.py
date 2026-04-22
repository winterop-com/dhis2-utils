"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import (
    AggregationType,
    DigitGroupSeparator,
    DisplayDensity,
    FontSize,
    HideEmptyItemStrategy,
    NumberType,
    RegressionType,
    UserOrgUnitType,
    VisualizationType,
)

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .axis import Axis
    from .axis_v2 import AxisV2
    from .category_dimension_params import CategoryDimensionParams
    from .category_option_group_set_dimension_params import CategoryOptionGroupSetDimensionParams
    from .data_dimension_item_params import DataDimensionItemParams
    from .data_element_group_set_dimension_params import DataElementGroupSetDimensionParams
    from .legend_definitions_params import LegendDefinitionsParams
    from .metadata_item_params import MetadataItemParams
    from .organisation_unit_group_set_dimension_params import OrganisationUnitGroupSetDimensionParams
    from .outlier_analysis import OutlierAnalysis
    from .relative_periods import RelativePeriods
    from .reporting_params import ReportingParams
    from .series import Series
    from .series_key import SeriesKey
    from .sharing import Sharing
    from .sorting import Sorting
    from .tracked_entity_attribute_dimension_params import TrackedEntityAttributeDimensionParams
    from .tracked_entity_data_element_dimension_params import TrackedEntityDataElementDimensionParams
    from .tracked_entity_program_indicator_dimension_params import TrackedEntityProgramIndicatorDimensionParams
    from .translation import Translation
    from .visualization_font_style import VisualizationFontStyle
    from .visualization_icon import VisualizationIcon


class VisualizationParamsColumns(_BaseModel):
    """OpenAPI schema `VisualizationParamsColumns`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParamsCreatedBy(_BaseModel):
    """OpenAPI schema `VisualizationParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParamsFilters(_BaseModel):
    """OpenAPI schema `VisualizationParamsFilters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParamsInterpretations(_BaseModel):
    """OpenAPI schema `VisualizationParamsInterpretations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParamsItemOrganisationUnitGroups(_BaseModel):
    """OpenAPI schema `VisualizationParamsItemOrganisationUnitGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `VisualizationParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `VisualizationParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParamsRows(_BaseModel):
    """OpenAPI schema `VisualizationParamsRows`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationParams(_BaseModel):
    """OpenAPI schema `VisualizationParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    attributeDimensions: list[TrackedEntityAttributeDimensionParams] | None = None
    attributeValues: list[AttributeValueParams] | None = None
    axes: list[AxisV2] | None = None
    categoryDimensions: list[CategoryDimensionParams] | None = None
    categoryOptionGroupSetDimensions: list[CategoryOptionGroupSetDimensionParams] | None = None
    code: str | None = None
    colSubTotals: bool | None = None
    colTotals: bool | None = None
    colorSet: str | None = None
    columnDimensions: list[str] | None = None
    columns: list[VisualizationParamsColumns] | None = None
    completedOnly: bool | None = None
    created: datetime | None = None
    createdBy: VisualizationParamsCreatedBy | None = None
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItemParams] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimensionParams] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimensionParams] | None = None
    description: str | None = None
    digitGroupSeparator: DigitGroupSeparator | None = None
    displayBaseLineLabel: str | None = None
    displayDensity: DisplayDensity | None = None
    displayDescription: str | None = None
    displayDomainAxisLabel: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayRangeAxisLabel: str | None = None
    displayShortName: str | None = None
    displaySubtitle: str | None = None
    displayTargetLineLabel: str | None = None
    displayTitle: str | None = None
    endDate: datetime | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[VisualizationParamsFilters] | None = None
    fixColumnHeaders: bool | None = None
    fixRowHeaders: bool | None = None
    fontSize: FontSize | None = None
    fontStyle: VisualizationFontStyle | None = None
    formName: str | None = None
    hideEmptyColumns: bool | None = None
    hideEmptyRowItems: HideEmptyItemStrategy | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    icons: list[VisualizationIcon] | None = None
    id: str | None = None
    interpretations: list[VisualizationParamsInterpretations] | None = None
    itemOrganisationUnitGroups: list[VisualizationParamsItemOrganisationUnitGroups] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: VisualizationParamsLastUpdatedBy | None = None
    legend: LegendDefinitionsParams | None = None
    measureCriteria: str | None = None
    metaData: dict[str, MetadataItemParams] | None = None
    name: str | None = None
    noSpaceBetweenColumns: bool | None = None
    numberType: NumberType | None = None
    optionalAxes: list[Axis] | None = None
    orgUnitField: str | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimensionParams] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnits: list[VisualizationParamsOrganisationUnits] | None = None
    outlierAnalysis: OutlierAnalysis | None = None
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimensionParams] | None = None
    rawPeriods: list[str] | None = None
    regression: bool | None = None
    regressionType: RegressionType | None = None
    relativePeriods: RelativePeriods | None = None
    reportingParams: ReportingParams | None = None
    rowDimensions: list[str] | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[VisualizationParamsRows] | None = None
    series: list[Series] | None = None
    seriesKey: SeriesKey | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    skipRounding: bool | None = None
    sortOrder: int | None = None
    sorting: list[Sorting] | None = None
    startDate: datetime | None = None
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    subtitle: str | None = None
    timeField: str | None = None
    title: str | None = None
    topLimit: int | None = None
    translations: list[Translation] | None = None
    type: VisualizationType | None = None
    userOrgUnitType: UserOrgUnitType | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
    visualizationPeriodName: str | None = None
    yearlySeries: list[str] | None = None
