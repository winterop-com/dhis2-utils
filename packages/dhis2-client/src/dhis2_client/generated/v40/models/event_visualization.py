"""Generated EventVisualization model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class EventVisualization(BaseModel):
    """DHIS2 Event Visualization - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/eventVisualizations.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: str | None = None

    attributeDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityAttributeDimension."
    )

    attributeValueDimension: Reference | None = Field(default=None, description="Reference to TrackedEntityAttribute.")

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )

    baseLineLabel: str | None = Field(default=None, description="Length/value max=255.")

    baseLineValue: float | None = None

    categoryDimensions: list[Any] | None = Field(default=None, description="Collection of CategoryDimension.")

    categoryOptionGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of CategoryOptionGroupSetDimension."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    collapseDataDimensions: bool | None = None

    columnDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    columns: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    completedOnly: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    cumulativeValues: bool | None = None

    dataDimensionItems: list[Any] | None = Field(
        default=None, description="Collection of DataDimensionItem. Read-only (inverse side)."
    )

    dataElementDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityDataElementDimension."
    )

    dataElementGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of DataElementGroupSetDimension. Read-only (inverse side)."
    )

    dataElementValueDimension: Reference | None = Field(default=None, description="Reference to DataElement.")

    dataType: str | None = None

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    digitGroupSeparator: str | None = None

    displayBaseLineLabel: str | None = Field(default=None, description="Read-only.")

    displayDensity: str | None = None

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayDomainAxisLabel: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayRangeAxisLabel: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    displaySubtitle: str | None = Field(default=None, description="Read-only.")

    displayTargetLineLabel: str | None = Field(default=None, description="Read-only.")

    displayTitle: str | None = Field(default=None, description="Read-only.")

    domainAxisLabel: str | None = Field(default=None, description="Length/value max=255.")

    endDate: datetime | None = None

    eventRepetitions: list[Any] | None = Field(
        default=None, description="Collection of EventRepetition. Length/value max=255."
    )

    eventStatus: str | None = None

    externalAccess: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    filterDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    filters: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    fontSize: str | None = None

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    hideEmptyRowItems: str | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideNaData: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    interpretations: list[Any] | None = Field(
        default=None, description="Collection of Interpretation. Read-only (inverse side)."
    )

    itemOrganisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnitGroup."
    )

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legacy: bool | None = None

    legendDefinitions: Any | None = Field(default=None, description="Reference to LegendDefinitions.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    noSpaceBetweenColumns: bool | None = None

    orgUnitField: str | None = Field(default=None, description="Length/value max=255.")

    organisationUnitGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnitGroupSetDimension."
    )

    organisationUnitLevels: list[Any] | None = Field(default=None, description="Collection of Integer.")

    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")

    outputType: str | None = None

    parentGraphMap: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    percentStackedValues: bool | None = None

    periods: list[Any] | None = Field(default=None, description="Collection of Period.")

    program: Reference | None = Field(default=None, description="Reference to Program.")

    programIndicatorDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityProgramIndicatorDimension."
    )

    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")

    programStatus: str | None = None

    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")

    rangeAxisDecimals: int | None = Field(default=None, description="Length/value max=2147483647.")

    rangeAxisLabel: str | None = Field(default=None, description="Length/value max=255.")

    rangeAxisMaxValue: float | None = None

    rangeAxisMinValue: float | None = None

    rangeAxisSteps: int | None = Field(default=None, description="Length/value max=2147483647.")

    rawPeriods: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    regressionType: str | None = None

    relatives: Any | None = Field(default=None, description="Reference to RelativePeriods. Read-only (inverse side).")

    rowDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    simpleDimensions: list[Any] | None = Field(
        default=None, description="Collection of SimpleDimension. Length/value max=255."
    )

    skipRounding: bool | None = None

    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")

    sorting: list[Any] | None = Field(default=None, description="Collection of Sorting. Length/value max=255.")

    startDate: datetime | None = None

    subscribed: bool | None = Field(default=None, description="Read-only.")

    subscribers: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    subtitle: str | None = Field(default=None, description="Length/value max=255.")

    targetLineLabel: str | None = Field(default=None, description="Length/value max=255.")

    targetLineValue: float | None = None

    timeField: str | None = Field(default=None, description="Length/value max=255.")

    title: str | None = Field(default=None, description="Length/value max=255.")

    topLimit: int | None = Field(default=None, description="Length/value max=2147483647.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    type: str | None = None

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )

    userGroupAccesses: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )

    userOrgUnitType: str | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None

    value: Reference | None = Field(
        default=None, description="Reference to DimensionalItemObject. Read-only (inverse side)."
    )
