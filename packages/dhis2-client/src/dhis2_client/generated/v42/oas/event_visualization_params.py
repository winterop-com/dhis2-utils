"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import (
    AggregationType,
    DigitGroupSeparator,
    DisplayDensity,
    EnrollmentStatus,
    EventDataType,
    EventOutputType,
    EventStatus,
    EventVisualizationType,
    FontSize,
    HideEmptyItemStrategy,
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
    from .event_repetition import EventRepetition
    from .legend_definitions_params import LegendDefinitionsParams
    from .metadata_item_params import MetadataItemParams
    from .organisation_unit_group_set_dimension_params import OrganisationUnitGroupSetDimensionParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .relative_periods import RelativePeriods
    from .sharing import Sharing
    from .simple_dimension import SimpleDimension
    from .sorting import Sorting
    from .tracked_entity_attribute_dimension_params import TrackedEntityAttributeDimensionParams
    from .tracked_entity_attribute_params import TrackedEntityAttributeParams
    from .tracked_entity_data_element_dimension_params import TrackedEntityDataElementDimensionParams
    from .tracked_entity_program_indicator_dimension_params import TrackedEntityProgramIndicatorDimensionParams
    from .tracked_entity_type_params import TrackedEntityTypeParams
    from .translation import Translation


class EventVisualizationParamsColumns(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsColumns`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsCreatedBy(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsFilters(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsFilters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsInterpretations(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsInterpretations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsItemOrganisationUnitGroups(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsItemOrganisationUnitGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsProgramDimensions(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsProgramDimensions`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsRows(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsRows`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParamsValue(_BaseModel):
    """OpenAPI schema `EventVisualizationParamsValue`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class EventVisualizationParams(_BaseModel):
    """OpenAPI schema `EventVisualizationParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType
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
    columns: list[EventVisualizationParamsColumns] | None = None
    completedOnly: bool | None = None
    created: datetime | None = None
    createdBy: EventVisualizationParamsCreatedBy | None = None
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItemParams] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimensionParams] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimensionParams] | None = None
    dataElementValueDimension: DataElementParams | None = None
    dataType: EventDataType
    description: str | None = None
    digitGroupSeparator: DigitGroupSeparator
    displayBaseLineLabel: str | None = None
    displayDensity: DisplayDensity
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
    eventStatus: EventStatus
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[EventVisualizationParamsFilters] | None = None
    fontSize: FontSize
    formName: str | None = None
    hideEmptyRowItems: HideEmptyItemStrategy
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideNaData: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    id: str | None = None
    interpretations: list[EventVisualizationParamsInterpretations] | None = None
    itemOrganisationUnitGroups: list[EventVisualizationParamsItemOrganisationUnitGroups] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: EventVisualizationParamsLastUpdatedBy | None = None
    legacy: bool | None = None
    legend: LegendDefinitionsParams | None = None
    metaData: dict[str, MetadataItemParams] | None = None
    name: str | None = None
    noSpaceBetweenColumns: bool | None = None
    orgUnitField: str | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimensionParams] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnits: list[EventVisualizationParamsOrganisationUnits] | None = None
    outputType: EventOutputType
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    program: ProgramParams | None = None
    programDimensions: list[EventVisualizationParamsProgramDimensions] | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimensionParams] | None = None
    programStage: ProgramStageParams | None = None
    programStatus: EnrollmentStatus
    rangeAxisDecimals: int | None = None
    rangeAxisLabel: str | None = None
    rangeAxisMaxValue: float | None = None
    rangeAxisMinValue: float | None = None
    rangeAxisSteps: int | None = None
    rawPeriods: list[str] | None = None
    regressionType: RegressionType
    relativePeriods: RelativePeriods | None = None
    repetitions: list[EventRepetition] | None = None
    rowDimensions: list[str] | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[EventVisualizationParamsRows] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    simpleDimensions: list[SimpleDimension] | None = None
    skipRounding: bool | None = None
    sortOrder: int
    sorting: list[Sorting] | None = None
    startDate: datetime | None = None
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    subtitle: str | None = None
    targetLineLabel: str | None = None
    targetLineValue: float | None = None
    timeField: str | None = None
    title: str | None = None
    topLimit: int
    trackedEntityType: TrackedEntityTypeParams | None = None
    translations: list[Translation] | None = None
    type: EventVisualizationType
    userOrgUnitType: UserOrgUnitType
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
    value: EventVisualizationParamsValue | None = None
