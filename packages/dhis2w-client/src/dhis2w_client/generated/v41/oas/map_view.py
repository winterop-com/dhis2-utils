"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .category_dimension import CategoryDimension
    from .category_option_group_set_dimension import CategoryOptionGroupSetDimension
    from .data_dimension_item import DataDimensionItem
    from .data_element_group_set_dimension import DataElementGroupSetDimension
    from .legend_definitions import LegendDefinitions
    from .organisation_unit_group_set_dimension import OrganisationUnitGroupSetDimension
    from .relative_periods import RelativePeriods
    from .sharing import Sharing
    from .tracked_entity_attribute_dimension import TrackedEntityAttributeDimension
    from .tracked_entity_data_element_dimension import TrackedEntityDataElementDimension
    from .tracked_entity_program_indicator_dimension import TrackedEntityProgramIndicatorDimension
    from .translation import Translation


class MapViewColumns(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewFilters(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewInterpretations(_BaseModel):
    """A UID reference to a Interpretation  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewItemOrganisationUnitGroups(_BaseModel):
    """A UID reference to a OrganisationUnitGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewOrganisationUnitGroupSet(_BaseModel):
    """A UID reference to a OrganisationUnitGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewRows(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewTrackedEntityType(_BaseModel):
    """A UID reference to a TrackedEntityType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapViewUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MapView(_BaseModel):
    """OpenAPI schema `MapView`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: str | None = None
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
    columns: list[MapViewColumns] | None = None
    completedOnly: bool | None = None
    config: str | None = None
    created: datetime | None = None
    createdBy: MapViewCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItem] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimension] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimension] | None = None
    description: str | None = None
    digitGroupSeparator: str | None = None
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
    eventStatus: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[MapViewFilters] | None = None
    followUp: bool | None = None
    formName: str | None = None
    hidden: bool | None = None
    hideEmptyRowItems: str | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    href: str | None = None
    id: str | None = None
    interpretations: list[MapViewInterpretations] | None = None
    itemOrganisationUnitGroups: list[MapViewItemOrganisationUnitGroups] | None = None
    labelFontColor: str | None = None
    labelFontSize: str | None = None
    labelFontStyle: str | None = None
    labelFontWeight: str | None = None
    labelTemplate: str | None = None
    labels: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: MapViewLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    layer: str | None = None
    legend: LegendDefinitions | None = None
    legendSet: MapViewLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    method: int | None = None
    noDataColor: str | None = None
    noSpaceBetweenColumns: bool | None = None
    opacity: float | None = None
    orgUnitField: str | None = None
    orgUnitFieldDisplayName: str | None = None
    organisationUnitColor: str | None = None
    organisationUnitGroupSet: MapViewOrganisationUnitGroupSet | None = _Field(
        default=None, description="A UID reference to a OrganisationUnitGroupSet  "
    )
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimension] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnitSelectionMode: str | None = None
    organisationUnits: list[MapViewOrganisationUnits] | None = None
    parentGraph: str | None = None
    parentGraphMap: dict[str, str] | None = None
    parentLevel: int | None = None
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    program: MapViewProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimension] | None = None
    programStage: MapViewProgramStage | None = _Field(default=None, description="A UID reference to a ProgramStage  ")
    programStatus: str | None = None
    radiusHigh: int | None = None
    radiusLow: int | None = None
    rawPeriods: list[str] | None = None
    regressionType: str | None = None
    relativePeriods: RelativePeriods | None = None
    renderingStrategy: str | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[MapViewRows] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    skipRounding: bool | None = None
    sortOrder: int | None = None
    startDate: datetime | None = None
    styleDataItem: dict[str, Any] | None = _Field(default=None, description="The actual type is unknown.  ")
    subscribed: bool | None = None
    subscribers: list[str] | None = None
    subtitle: str | None = None
    thematicMapType: str | None = None
    timeField: str | None = None
    title: str | None = None
    topLimit: int | None = None
    trackedEntityType: MapViewTrackedEntityType | None = _Field(
        default=None, description="A UID reference to a TrackedEntityType  "
    )
    translations: list[Translation] | None = None
    user: MapViewUser | None = _Field(default=None, description="A UID reference to a User  ")
    userOrgUnitType: str | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
