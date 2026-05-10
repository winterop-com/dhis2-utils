"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

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
    from .event_repetition import EventRepetition
    from .legend_definitions import LegendDefinitions
    from .organisation_unit_group_set_dimension import OrganisationUnitGroupSetDimension
    from .relative_periods import RelativePeriods
    from .sharing import Sharing
    from .simple_dimension import SimpleDimension
    from .sorting import Sorting
    from .tracked_entity_attribute_dimension import TrackedEntityAttributeDimension
    from .tracked_entity_data_element_dimension import TrackedEntityDataElementDimension
    from .tracked_entity_program_indicator_dimension import TrackedEntityProgramIndicatorDimension
    from .translation import Translation


class EventVisualizationAttributeValueDimension(_BaseModel):
    """A UID reference to a TrackedEntityAttribute  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationColumns(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationDataElementValueDimension(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationFilters(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationInterpretations(_BaseModel):
    """A UID reference to a Interpretation  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationItemOrganisationUnitGroups(_BaseModel):
    """A UID reference to a OrganisationUnitGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationProgramDimensions(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationProgramStage(_BaseModel):
    """A UID reference to a ProgramStage  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationRows(_BaseModel):
    """A UID reference to a DimensionalObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationTrackedEntityType(_BaseModel):
    """A UID reference to a TrackedEntityType  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualizationValue(_BaseModel):
    """A UID reference to a DimensionalItemObject  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventVisualization(_BaseModel):
    """OpenAPI schema `EventVisualization`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: str | None = None
    attributeDimensions: list[TrackedEntityAttributeDimension] | None = None
    attributeValueDimension: EventVisualizationAttributeValueDimension | None = _Field(
        default=None, description="A UID reference to a TrackedEntityAttribute  "
    )
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
    columns: list[EventVisualizationColumns] | None = None
    completedOnly: bool | None = None
    created: datetime | None = None
    createdBy: EventVisualizationCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    cumulativeValues: bool | None = None
    dataDimensionItems: list[DataDimensionItem] | None = None
    dataElementDimensions: list[TrackedEntityDataElementDimension] | None = None
    dataElementGroupSetDimensions: list[DataElementGroupSetDimension] | None = None
    dataElementValueDimension: EventVisualizationDataElementValueDimension | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    dataType: str | None = None
    description: str | None = None
    digitGroupSeparator: str | None = None
    displayBaseLineLabel: str | None = None
    displayDensity: str | None = None
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
    eventStatus: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filterDimensions: list[str] | None = None
    filters: list[EventVisualizationFilters] | None = None
    fontSize: str | None = None
    formName: str | None = None
    hideEmptyRowItems: str | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideNaData: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    href: str | None = None
    id: str | None = None
    interpretations: list[EventVisualizationInterpretations] | None = None
    itemOrganisationUnitGroups: list[EventVisualizationItemOrganisationUnitGroups] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: EventVisualizationLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    legacy: bool | None = None
    legend: LegendDefinitions | None = None
    name: str | None = None
    noSpaceBetweenColumns: bool | None = None
    orgUnitField: str | None = None
    organisationUnitGroupSetDimensions: list[OrganisationUnitGroupSetDimension] | None = None
    organisationUnitLevels: list[int] | None = None
    organisationUnits: list[EventVisualizationOrganisationUnits] | None = None
    outputType: str | None = None
    parentGraphMap: dict[str, str] | None = None
    percentStackedValues: bool | None = None
    periods: list[str] | None = None
    program: EventVisualizationProgram | None = _Field(default=None, description="A UID reference to a Program  ")
    programDimensions: list[EventVisualizationProgramDimensions] | None = None
    programIndicatorDimensions: list[TrackedEntityProgramIndicatorDimension] | None = None
    programStage: EventVisualizationProgramStage | None = _Field(
        default=None, description="A UID reference to a ProgramStage  "
    )
    programStatus: str | None = None
    rangeAxisDecimals: int | None = None
    rangeAxisLabel: str | None = None
    rangeAxisMaxValue: float | None = None
    rangeAxisMinValue: float | None = None
    rangeAxisSteps: int | None = None
    rawPeriods: list[str] | None = None
    regressionType: str | None = None
    relativePeriods: RelativePeriods | None = None
    repetitions: list[EventRepetition] | None = None
    rowDimensions: list[str] | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[EventVisualizationRows] | None = None
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
    trackedEntityType: EventVisualizationTrackedEntityType | None = _Field(
        default=None, description="A UID reference to a TrackedEntityType  "
    )
    translations: list[Translation] | None = None
    type: str | None = None
    user: EventVisualizationUser | None = _Field(default=None, description="A UID reference to a User  ")
    userOrgUnitType: str | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
    value: EventVisualizationValue | None = _Field(
        default=None, description="A UID reference to a DimensionalItemObject  "
    )
