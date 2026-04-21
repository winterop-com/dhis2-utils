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
    EnrollmentStatus,
    EventOutputType,
    EventStatus,
    EventVisualizationType,
    HideEmptyItemStrategy,
    LegendDisplayStrategy,
    RegressionType,
    UserOrgUnitType,
)

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_dimension_params import CategoryDimensionParams
    from .category_option_group_set_dimension_params import CategoryOptionGroupSetDimensionParams
    from .data_dimension_item_params import DataDimensionItemParams
    from .data_element_group_set_dimension_params import DataElementGroupSetDimensionParams
    from .data_element_params import DataElementParams
    from .legend_definitions_params import LegendDefinitionsParams
    from .legend_set_params import LegendSetParams
    from .metadata_item_params import MetadataItemParams
    from .organisation_unit_group_set_dimension_params import OrganisationUnitGroupSetDimensionParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .relative_periods import RelativePeriods
    from .sharing import Sharing
    from .tracked_entity_attribute_dimension_params import TrackedEntityAttributeDimensionParams
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .tracked_entity_data_element_dimension_params import TrackedEntityDataElementDimensionParams
    from .tracked_entity_program_indicator_dimension_params import TrackedEntityProgramIndicatorDimensionParams
    from .translation import Translation


class EventChartParamsColumns(_BaseModel):
    """OpenAPI schema `EventChartParamsColumns`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsCreatedBy(_BaseModel):
    """OpenAPI schema `EventChartParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsFilters(_BaseModel):
    """OpenAPI schema `EventChartParamsFilters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsInterpretations(_BaseModel):
    """OpenAPI schema `EventChartParamsInterpretations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsItemOrganisationUnitGroups(_BaseModel):
    """OpenAPI schema `EventChartParamsItemOrganisationUnitGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `EventChartParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `EventChartParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsPeriods(_BaseModel):
    """OpenAPI schema `EventChartParamsPeriods`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsRows(_BaseModel):
    """OpenAPI schema `EventChartParamsRows`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParamsValue(_BaseModel):
    """OpenAPI schema `EventChartParamsValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventChartParams(_BaseModel):
    """OpenAPI schema `EventChartParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType | None = None
    attributeDimensions: list[TrackedEntityAttributeDimensionParams] | None = None
    attributeValueDimension: TrackedEntityAttributeParams | None = None
    attributeValues: list[AttributeValueParams] | None = None
    baseLineLabel: str | None = None
    baseLineValue: float | None = None
    categoryDimensions: list[CategoryDimensionParams] | None = None
    categoryOptionGroupSetDimensions: list[CategoryOptionGroupSetDimensionParams] | None = None
    code: str | None = None
    colSubTotals: bool | None = None
    colTotals: bool | None = None
    collapseDataDimensions: bool | None = None
    columnDimensions: list[str] | None = None
    columns: list[EventChartParamsColumns] | None = None
    completedOnly: bool | None = None
    created: datetime | None = None
    createdBy: EventChartParamsCreatedBy | None = None
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItemParams] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimensionParams] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimensionParams] | None = None
    dataElementValueDimension: DataElementParams | None = None
    description: str | None = None
    digitGroupSeparator: DigitGroupSeparator | None = None
    displayBaseLineLabel: str | None = None
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
    eventStatus: EventStatus | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[EventChartParamsFilters] | None = None
    fixColumnHeaders: bool | None = None
    fixRowHeaders: bool | None = None
    formName: str | None = None
    hideEmptyColumns: bool | None = None
    hideEmptyRowItems: HideEmptyItemStrategy | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideNaData: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    id: str | None = None
    interpretations: list[EventChartParamsInterpretations] | None = None
    itemOrganisationUnitGroups: list[EventChartParamsItemOrganisationUnitGroups] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: EventChartParamsLastUpdatedBy | None = None
    legacy: bool | None = None
    legend: LegendDefinitionsParams | None = None
    legendDisplayStrategy: LegendDisplayStrategy | None = None
    legendSet: LegendSetParams | None = None
    metaData: dict[str, MetadataItemParams] | None = None
    name: str | None = None
    noSpaceBetweenColumns: bool | None = None
    orgUnitField: str | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimensionParams] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnits: list[EventChartParamsOrganisationUnits] | None = None
    outputType: EventOutputType | None = None
    percentStackedValues: bool | None = None
    periods: list[EventChartParamsPeriods] | None = None
    program: ProgramParams | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimensionParams] | None = None
    programStage: ProgramStageParams | None = None
    programStatus: EnrollmentStatus | None = None
    rangeAxisDecimals: int | None = None
    rangeAxisLabel: str | None = None
    rangeAxisMaxValue: float | None = None
    rangeAxisMinValue: float | None = None
    rangeAxisSteps: int | None = None
    rawPeriods: list[str] | None = None
    regressionType: RegressionType | None = None
    relativePeriods: RelativePeriods | None = None
    rowDimensions: list[str] | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[EventChartParamsRows] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    skipRounding: bool | None = None
    sortOrder: int | None = None
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
    type: EventVisualizationType | None = None
    userOrgUnitType: UserOrgUnitType | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
    value: EventChartParamsValue | None = None
    yearlySeries: list[str] | None = None
