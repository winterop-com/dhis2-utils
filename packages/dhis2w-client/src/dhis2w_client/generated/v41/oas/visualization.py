"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .axis import Axis
    from .axis_v2 import AxisV2
    from .category_dimension import CategoryDimension
    from .category_option_group_set_dimension import CategoryOptionGroupSetDimension
    from .data_dimension_item import DataDimensionItem
    from .data_element_group_set_dimension import DataElementGroupSetDimension
    from .legend_definitions import LegendDefinitions
    from .organisation_unit_group_set_dimension import OrganisationUnitGroupSetDimension
    from .outlier_analysis import OutlierAnalysis
    from .relative_periods import RelativePeriods
    from .reporting_params import ReportingParams
    from .series import Series
    from .series_key import SeriesKey
    from .sharing import Sharing
    from .sorting import Sorting
    from .tracked_entity_attribute_dimension import TrackedEntityAttributeDimension
    from .tracked_entity_data_element_dimension import TrackedEntityDataElementDimension
    from .tracked_entity_program_indicator_dimension import TrackedEntityProgramIndicatorDimension
    from .translation import Translation
    from .visualization_font_style import VisualizationFontStyle
    from .visualization_icon import VisualizationIcon


class VisualizationColumns(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationFilters(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationInterpretations(_BaseModel):
    """A UID reference to a Interpretation  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationItemOrganisationUnitGroups(_BaseModel):
    """A UID reference to a OrganisationUnitGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationRows(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class VisualizationUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Visualization(_BaseModel):
    """OpenAPI schema `Visualization`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: (
        Literal[
            "SUM",
            "AVERAGE",
            "AVERAGE_SUM_ORG_UNIT",
            "LAST",
            "LAST_AVERAGE_ORG_UNIT",
            "LAST_LAST_ORG_UNIT",
            "LAST_IN_PERIOD",
            "LAST_IN_PERIOD_AVERAGE_ORG_UNIT",
            "FIRST",
            "FIRST_AVERAGE_ORG_UNIT",
            "FIRST_FIRST_ORG_UNIT",
            "COUNT",
            "STDDEV",
            "VARIANCE",
            "MIN",
            "MAX",
            "MIN_SUM_ORG_UNIT",
            "MAX_SUM_ORG_UNIT",
            "NONE",
            "CUSTOM",
            "DEFAULT",
        ]
        | None
    ) = None
    attributeDimensions: list[TrackedEntityAttributeDimension] | None = None
    attributeValues: list[AttributeValue] | None = None
    axes: list[AxisV2] | None = None
    baseLineLabel: str | None = None
    baseLineValue: float | None = None
    categoryDimensions: list[CategoryDimension] | None = None
    categoryOptionGroupSetDimensions: list[CategoryOptionGroupSetDimension] | None = None
    code: str | None = None
    colSubTotals: bool | None = None
    colTotals: bool | None = None
    colorSet: str | None = None
    columnDimensions: list[str] | None = None
    columns: list[VisualizationColumns] | None = None
    completedOnly: bool | None = None
    created: datetime | None = None
    createdBy: VisualizationCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItem] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimension] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimension] | None = None
    description: str | None = None
    digitGroupSeparator: Literal["COMMA", "SPACE", "NONE"] | None = None
    displayBaseLineLabel: str | None = None
    displayDensity: Literal["COMFORTABLE", "NORMAL", "COMPACT", "NONE"] | None = None
    displayDescription: str | None = None
    displayDomainAxisLabel: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayRangeAxisLabel: str | None = None
    displayShortName: str | None = None
    displaySubtitle: str | None = None
    displayTargetLineLabel: str | None = None
    displayTitle: str | None = None
    domainAxisLabel: str | None = None
    endDate: datetime | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[VisualizationFilters] | None = None
    fixColumnHeaders: bool | None = None
    fixRowHeaders: bool | None = None
    fontSize: Literal["LARGE", "NORMAL", "SMALL"] | None = None
    fontStyle: VisualizationFontStyle | None = None
    formName: str | None = None
    hideEmptyColumns: bool | None = None
    hideEmptyRowItems: Literal["NONE", "BEFORE_FIRST", "AFTER_LAST", "BEFORE_FIRST_AFTER_LAST", "ALL"] | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    href: str | None = None
    icons: list[VisualizationIcon] | None = None
    id: str | None = None
    interpretations: list[VisualizationInterpretations] | None = None
    itemOrganisationUnitGroups: list[VisualizationItemOrganisationUnitGroups] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: VisualizationLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    legend: LegendDefinitions | None = None
    measureCriteria: str | None = None
    name: str | None = None
    noSpaceBetweenColumns: bool | None = None
    numberType: Literal["VALUE", "ROW_PERCENTAGE", "COLUMN_PERCENTAGE"] | None = None
    optionalAxes: list[Axis] | None = None
    orgUnitField: str | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimension] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnits: list[VisualizationOrganisationUnits] | None = None
    outlierAnalysis: OutlierAnalysis | None = None
    parentGraphMap: dict[str, str] | None = None
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimension] | None = None
    rangeAxisDecimals: int | None = None
    rangeAxisLabel: str | None = None
    rangeAxisMaxValue: float | None = None
    rangeAxisMinValue: float | None = None
    rangeAxisSteps: int | None = None
    rawPeriods: list[str] | None = None
    regression: bool | None = None
    regressionType: Literal["NONE", "LINEAR", "POLYNOMIAL", "LOESS"] | None = None
    relativePeriods: RelativePeriods | None = None
    reportingParams: ReportingParams | None = None
    rowDimensions: list[str] | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[VisualizationRows] | None = None
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
    targetLineLabel: str | None = None
    targetLineValue: float | None = None
    timeField: str | None = None
    title: str | None = None
    topLimit: int | None = None
    translations: list[Translation] | None = None
    type: (
        Literal[
            "COLUMN",
            "STACKED_COLUMN",
            "BAR",
            "STACKED_BAR",
            "LINE",
            "AREA",
            "STACKED_AREA",
            "PIE",
            "RADAR",
            "GAUGE",
            "YEAR_OVER_YEAR_LINE",
            "YEAR_OVER_YEAR_COLUMN",
            "SCATTER",
            "BUBBLE",
            "SINGLE_VALUE",
            "PIVOT_TABLE",
            "OUTLIER_TABLE",
        ]
        | None
    ) = None
    user: VisualizationUser | None = _Field(default=None, description="A UID reference to a User  ")
    userOrgUnitType: Literal["DATA_CAPTURE", "DATA_OUTPUT", "TEI_SEARCH"] | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
    visualizationPeriodName: str | None = None
    yearlySeries: list[str] | None = None
