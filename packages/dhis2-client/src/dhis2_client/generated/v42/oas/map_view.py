"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

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
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .base_nameable_object import BaseNameableObject
    from .category_dimension import CategoryDimension
    from .category_option_group_set_dimension import CategoryOptionGroupSetDimension
    from .data_dimension_item import DataDimensionItem
    from .data_element_group_set_dimension import DataElementGroupSetDimension
    from .dimensional_object import DimensionalObject
    from .legend_definitions import LegendDefinitions
    from .metadata_item import MetadataItem
    from .organisation_unit_group import OrganisationUnitGroup
    from .organisation_unit_group_set_dimension import OrganisationUnitGroupSetDimension
    from .relative_periods import RelativePeriods
    from .sharing import Sharing
    from .tracked_entity_attribute_dimension import TrackedEntityAttributeDimension
    from .tracked_entity_data_element_dimension import TrackedEntityDataElementDimension
    from .tracked_entity_program_indicator_dimension import TrackedEntityProgramIndicatorDimension
    from .tracked_entity_type import TrackedEntityType
    from .translation import Translation
    from .user_dto import UserDto


class MapView(_BaseModel):
    """OpenAPI schema `MapView`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: AggregationType | None = None
    areaRadius: int | None = None
    attributeDimensions: list[TrackedEntityAttributeDimension] | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryDimensions: list[CategoryDimension] | None = None
    categoryOptionGroupSetDimensions: list[CategoryOptionGroupSetDimension] | None = None
    classes: int | None = None
    code: str | None = None
    colSubTotals: bool | None = None
    colTotals: bool | None = None
    colorHigh: str | None = None
    colorLow: str | None = None
    colorScale: str | None = None
    columnDimensions: list[str] | None = None
    columns: list[DimensionalObject] | None = None
    completedOnly: bool | None = None
    config: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItem] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimension] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimension] | None = None
    description: str | None = None
    digitGroupSeparator: DigitGroupSeparator | None = None
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
    eventPointRadius: int | None = None
    eventStatus: EventStatus | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[DimensionalObject] | None = None
    followUp: bool | None = None
    formName: str | None = None
    hidden: bool | None = None
    hideEmptyRowItems: HideEmptyItemStrategy | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    href: str | None = None
    id: str | None = None
    interpretations: list[BaseIdentifiableObject] | None = None
    itemOrganisationUnitGroups: list[OrganisationUnitGroup] | None = None
    labelFontColor: str | None = None
    labelFontSize: str | None = None
    labelFontStyle: str | None = None
    labelFontWeight: str | None = None
    labelTemplate: str | None = None
    labels: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    layer: str | None = None
    legend: LegendDefinitions | None = None
    legendSet: BaseIdentifiableObject | None = None
    metaData: dict[str, MetadataItem] | None = None
    method: int | None = None
    name: str | None = None
    noDataColor: str | None = None
    noSpaceBetweenColumns: bool | None = None
    opacity: float | None = None
    orgUnitField: str | None = None
    orgUnitFieldDisplayName: str | None = None
    organisationUnitColor: str | None = None
    organisationUnitGroupSet: BaseIdentifiableObject | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimension] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnitSelectionMode: OrganisationUnitSelectionMode | None = None
    organisationUnits: list[BaseNameableObject] | None = None
    parentGraph: str | None = None
    parentGraphMap: dict[str, str] | None = None
    parentLevel: int | None = None
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    program: BaseIdentifiableObject | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimension] | None = None
    programStage: BaseIdentifiableObject | None = None
    programStatus: EnrollmentStatus | None = None
    radiusHigh: int | None = None
    radiusLow: int | None = None
    rawPeriods: list[str] | None = None
    regressionType: RegressionType | None = None
    relativePeriods: RelativePeriods | None = None
    renderingStrategy: MapViewRenderingStrategy | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[DimensionalObject] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    skipRounding: bool | None = None
    sortOrder: int | None = None
    startDate: datetime | None = None
    styleDataItem: Object | None = None
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    subtitle: str | None = None
    thematicMapType: ThematicMapType | None = None
    timeField: str | None = None
    title: str | None = None
    topLimit: int | None = None
    trackedEntityType: TrackedEntityType | None = None
    translations: list[Translation] | None = None
    userOrgUnitType: UserOrgUnitType | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
