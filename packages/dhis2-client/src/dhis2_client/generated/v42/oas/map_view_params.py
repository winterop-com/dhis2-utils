"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._aliases import Object
from ._enums import (
    AggregationType,
    DigitGroupSeparator,
    EnrollmentStatus,
    EventStatus,
    HideEmptyItemStrategy,
    MapViewRenderingStrategy,
    OrganisationUnitSelectionMode,
    RegressionType,
    ThematicMapType,
    UserOrgUnitType,
)

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_dimension_params import CategoryDimensionParams
    from .category_option_group_set_dimension_params import CategoryOptionGroupSetDimensionParams
    from .data_dimension_item_params import DataDimensionItemParams
    from .data_element_group_set_dimension_params import DataElementGroupSetDimensionParams
    from .legend_definitions_params import LegendDefinitionsParams
    from .legend_set_params import LegendSetParams
    from .metadata_item_params import MetadataItemParams
    from .organisation_unit_group_set_dimension_params import OrganisationUnitGroupSetDimensionParams
    from .organisation_unit_group_set_params import OrganisationUnitGroupSetParams
    from .program_params import ProgramParams
    from .program_stage_params import ProgramStageParams
    from .relative_periods import RelativePeriods
    from .sharing import Sharing
    from .tracked_entity_attribute_dimension_params import TrackedEntityAttributeDimensionParams
    from .tracked_entity_data_element_dimension_params import TrackedEntityDataElementDimensionParams
    from .tracked_entity_program_indicator_dimension_params import TrackedEntityProgramIndicatorDimensionParams
    from .translation import Translation


class MapViewParamsColumns(_BaseModel):
    """OpenAPI schema `MapViewParamsColumns`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsCreatedBy(_BaseModel):
    """OpenAPI schema `MapViewParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsFilters(_BaseModel):
    """OpenAPI schema `MapViewParamsFilters`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsInterpretations(_BaseModel):
    """OpenAPI schema `MapViewParamsInterpretations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsItemOrganisationUnitGroups(_BaseModel):
    """OpenAPI schema `MapViewParamsItemOrganisationUnitGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `MapViewParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `MapViewParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsRows(_BaseModel):
    """OpenAPI schema `MapViewParamsRows`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParamsTrackedEntityType(_BaseModel):
    """OpenAPI schema `MapViewParamsTrackedEntityType`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class MapViewParams(_BaseModel):
    """OpenAPI schema `MapViewParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType
    areaRadius: int | None = None
    attributeDimensions: list[TrackedEntityAttributeDimensionParams] | None = None
    attributeValues: list[AttributeValueParams] | None = None
    categoryDimensions: list[CategoryDimensionParams] | None = None
    categoryOptionGroupSetDimensions: list[CategoryOptionGroupSetDimensionParams] | None = None
    classes: int | None = None
    code: str | None = None
    colSubTotals: bool | None = None
    colTotals: bool | None = None
    colorHigh: str | None = None
    colorLow: str | None = None
    colorScale: str | None = None
    columnDimensions: list[str] | None = None
    columns: list[MapViewParamsColumns] | None = None
    completedOnly: bool | None = None
    config: str | None = None
    created: datetime | None = None
    createdBy: MapViewParamsCreatedBy | None = None
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItemParams] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimensionParams] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimensionParams] | None = None
    description: str | None = None
    digitGroupSeparator: DigitGroupSeparator
    displayBaseLineLabel: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    displaySubtitle: str | None = None
    displayTargetLineLabel: str | None = None
    displayTitle: str | None = None
    endDate: datetime | None = None
    eventClustering: bool | None = None
    eventCoordinateField: str | None = None
    eventPointColor: str | None = None
    eventPointRadius: int
    eventStatus: EventStatus
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[MapViewParamsFilters] | None = None
    followUp: bool | None = None
    formName: str | None = None
    hidden: bool | None = None
    hideEmptyRowItems: HideEmptyItemStrategy
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    id: str | None = None
    interpretations: list[MapViewParamsInterpretations] | None = None
    itemOrganisationUnitGroups: list[MapViewParamsItemOrganisationUnitGroups] | None = None
    labelFontColor: str | None = None
    labelFontSize: str | None = None
    labelFontStyle: str | None = None
    labelFontWeight: str | None = None
    labelTemplate: str | None = None
    labels: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: MapViewParamsLastUpdatedBy | None = None
    layer: str | None = None
    legend: LegendDefinitionsParams | None = None
    legendSet: LegendSetParams | None = None
    metaData: dict[str, MetadataItemParams] | None = None
    method: int | None = None
    name: str | None = None
    noDataColor: str | None = None
    noSpaceBetweenColumns: bool | None = None
    opacity: float | None = None
    orgUnitField: str | None = None
    orgUnitFieldDisplayName: str | None = None
    organisationUnitColor: str | None = None
    organisationUnitGroupSet: OrganisationUnitGroupSetParams | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimensionParams] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnitSelectionMode: OrganisationUnitSelectionMode
    organisationUnits: list[MapViewParamsOrganisationUnits] | None = None
    parentGraph: str | None = None
    parentLevel: int
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    program: ProgramParams | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimensionParams] | None = None
    programStage: ProgramStageParams | None = None
    programStatus: EnrollmentStatus
    radiusHigh: int | None = None
    radiusLow: int | None = None
    rawPeriods: list[str] | None = None
    regressionType: RegressionType
    relativePeriods: RelativePeriods | None = None
    renderingStrategy: MapViewRenderingStrategy
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[MapViewParamsRows] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    skipRounding: bool | None = None
    sortOrder: int
    startDate: datetime | None = None
    styleDataItem: Object | None = None
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    subtitle: str | None = None
    thematicMapType: ThematicMapType
    timeField: str | None = None
    title: str | None = None
    topLimit: int
    trackedEntityType: MapViewParamsTrackedEntityType | None = None
    translations: list[Translation] | None = None
    userOrgUnitType: UserOrgUnitType
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
