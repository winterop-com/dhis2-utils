"""Generated EventReport model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import (
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


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class EventReport(BaseModel):
    """DHIS2 Event Report - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/eventReports.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: AggregationType | None = None

    attributeDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    attributeValueDimension: Reference | None = Field(
        default=None, description="Reference to TrackedEntityAttribute. Read-only (inverse side)."
    )

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    categoryDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    categoryOptionGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    code: str | None = None

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    collapseDataDimensions: bool | None = None

    columnDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    columns: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    completedOnly: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    cumulativeValues: bool | None = None

    dataDimensionItems: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    dataElementDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    dataElementGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    dataElementValueDimension: Reference | None = Field(
        default=None, description="Reference to DataElement. Read-only (inverse side)."
    )

    dataType: EventDataType | None = None

    description: str | None = None

    digitGroupSeparator: DigitGroupSeparator | None = None

    displayBaseLineLabel: str | None = None

    displayDensity: DisplayDensity | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    displaySubtitle: str | None = None

    displayTargetLineLabel: str | None = None

    displayTitle: str | None = None

    endDate: datetime | None = None

    eventStatus: EventStatus | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    filterDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    filters: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    fixColumnHeaders: bool | None = None

    fixRowHeaders: bool | None = None

    fontSize: FontSize | None = None

    formName: str | None = None

    hideEmptyColumns: bool | None = None

    hideEmptyRowItems: HideEmptyItemStrategy | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideNaData: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    id: str | None = None

    interpretations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    itemOrganisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    legacy: bool | None = None

    legendDefinitions: Any | None = Field(
        default=None, description="Reference to LegendDefinitions. Read-only (inverse side)."
    )

    metaData: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    name: str | None = None

    noSpaceBetweenColumns: bool | None = None

    orgUnitField: str | None = None

    organisationUnitGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    organisationUnitLevels: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    outputType: EventOutputType | None = None

    parentGraphMap: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    percentStackedValues: bool | None = None

    periods: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    program: Reference | None = Field(default=None, description="Reference to Program. Read-only (inverse side).")

    programIndicatorDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    programStage: Reference | None = Field(
        default=None, description="Reference to ProgramStage. Read-only (inverse side)."
    )

    programStatus: EnrollmentStatus | None = None

    rawPeriods: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    regressionType: RegressionType | None = None

    relatives: Any | None = Field(default=None, description="Reference to RelativePeriods. Read-only (inverse side).")

    rowDimensions: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    simpleDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    skipRounding: bool | None = None

    sortOrder: int | None = None

    startDate: datetime | None = None

    subscribed: bool | None = None

    subscribers: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    subtitle: str | None = None

    timeField: str | None = None

    title: str | None = None

    topLimit: int | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    type: EventVisualizationType | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userOrgUnitType: UserOrgUnitType | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None

    value: Reference | None = Field(
        default=None, description="Reference to DimensionalItemObject. Read-only (inverse side)."
    )
