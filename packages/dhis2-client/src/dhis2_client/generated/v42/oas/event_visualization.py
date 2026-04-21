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
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .base_nameable_object import BaseNameableObject
    from .category_dimension import CategoryDimension
    from .category_option_group_set_dimension import CategoryOptionGroupSetDimension
    from .data_dimension_item import DataDimensionItem
    from .data_element_group_set_dimension import DataElementGroupSetDimension
    from .dimensional_item_object import DimensionalItemObject
    from .dimensional_object import DimensionalObject
    from .event_repetition import EventRepetition
    from .legend_definitions import LegendDefinitions
    from .metadata_item import MetadataItem
    from .organisation_unit_group import OrganisationUnitGroup
    from .organisation_unit_group_set_dimension import OrganisationUnitGroupSetDimension
    from .program import Program
    from .relative_periods import RelativePeriods
    from .sharing import Sharing
    from .simple_dimension import SimpleDimension
    from .sorting import Sorting
    from .tracked_entity_attribute_dimension import TrackedEntityAttributeDimension
    from .tracked_entity_data_element_dimension import TrackedEntityDataElementDimension
    from .tracked_entity_program_indicator_dimension import TrackedEntityProgramIndicatorDimension
    from .translation import Translation
    from .user_dto import UserDto


class EventVisualization(_BaseModel):
    """OpenAPI schema `EventVisualization`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: AggregationType | None = None
    attributeDimensions: list[TrackedEntityAttributeDimension] | None = None
    attributeValueDimension: BaseIdentifiableObject | None = None
    attributeValues: list[AttributeValue] | None = None
    baseLineLabel: str | None = None
    baseLineValue: float | None = None
    categoryDimensions: list[CategoryDimension] | None = None
    categoryOptionGroupSetDimensions: list[CategoryOptionGroupSetDimension] | None = None
    code: str | None = None
    colSubTotals: bool | None = None
    colTotals: bool | None = None
    collapseDataDimensions: bool | None = None
    columnDimensions: list[str] | None = None
    columns: list[DimensionalObject] | None = None
    completedOnly: bool | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItem] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimension] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimension] | None = None
    dataElementValueDimension: BaseIdentifiableObject | None = None
    dataType: EventDataType | None = None
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
    domainAxisLabel: str | None = None
    endDate: datetime | None = None
    eventStatus: EventStatus | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[DimensionalObject] | None = None
    fontSize: FontSize | None = None
    formName: str | None = None
    hideEmptyRowItems: HideEmptyItemStrategy | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideNaData: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    href: str | None = None
    id: str | None = None
    interpretations: list[BaseIdentifiableObject] | None = None
    itemOrganisationUnitGroups: list[OrganisationUnitGroup] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legacy: bool | None = None
    legend: LegendDefinitions | None = None
    metaData: dict[str, MetadataItem] | None = None
    name: str | None = None
    noSpaceBetweenColumns: bool | None = None
    orgUnitField: str | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimension] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnits: list[BaseNameableObject] | None = None
    outputType: EventOutputType | None = None
    parentGraphMap: dict[str, str] | None = None
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    program: BaseIdentifiableObject | None = None
    programDimensions: list[Program] | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimension] | None = None
    programStage: BaseIdentifiableObject | None = None
    programStatus: EnrollmentStatus | None = None
    rangeAxisDecimals: int | None = None
    rangeAxisLabel: str | None = None
    rangeAxisMaxValue: float | None = None
    rangeAxisMinValue: float | None = None
    rangeAxisSteps: int | None = None
    rawPeriods: list[str] | None = None
    regressionType: RegressionType | None = None
    relativePeriods: RelativePeriods | None = None
    repetitions: list[EventRepetition] | None = None
    rowDimensions: list[str] | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[DimensionalObject] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    simpleDimensions: list[SimpleDimension] | None = None
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
    trackedEntityType: BaseIdentifiableObject | None = None
    translations: list[Translation] | None = None
    type: EventVisualizationType | None = None
    userOrgUnitType: UserOrgUnitType | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
    value: DimensionalItemObject | None = None
