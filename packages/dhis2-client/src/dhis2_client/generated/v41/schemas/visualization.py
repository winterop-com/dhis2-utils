"""Generated Visualization model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import (
    AggregationType,
    DigitGroupSeparator,
    DisplayDensity,
    FontSize,
    HideEmptyItemStrategy,
    NumberType,
    RegressionType,
    UserOrgUnitType,
    VisualizationType,
)


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Visualization(BaseModel):
    """DHIS2 Visualization - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/visualizations.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: AggregationType | None = None

    attributeDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityAttributeDimension. Read-only (inverse side)."
    )

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )

    axes: list[Any] | None = Field(default=None, description="Collection of AxisV2. Length/value max=255.")

    axis: list[Any] | None = Field(default=None, description="Collection of Axis.")

    baseLineLabel: str | None = Field(default=None, description="Length/value max=2147483647.")

    baseLineValue: float | None = None

    categoryDimensions: list[Any] | None = Field(default=None, description="Collection of CategoryDimension.")

    categoryOptionGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of CategoryOptionGroupSetDimension."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    colorSet: str | None = Field(default=None, description="Length/value max=255.")

    columnDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    columns: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    completedOnly: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    cumulativeValues: bool | None = None

    dataDimensionItems: list[Any] | None = Field(default=None, description="Collection of DataDimensionItem.")

    dataElementDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityDataElementDimension. Read-only (inverse side)."
    )

    dataElementGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of DataElementGroupSetDimension."
    )

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    digitGroupSeparator: DigitGroupSeparator | None = None

    displayBaseLineLabel: str | None = Field(default=None, description="Read-only.")

    displayDensity: DisplayDensity | None = None

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayDomainAxisLabel: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayRangeAxisLabel: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    displaySubtitle: str | None = Field(default=None, description="Read-only.")

    displayTargetLineLabel: str | None = Field(default=None, description="Read-only.")

    displayTitle: str | None = Field(default=None, description="Read-only.")

    domainAxisLabel: str | None = Field(default=None, description="Length/value max=2147483647.")

    endDate: datetime | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    filterDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    filters: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    fixColumnHeaders: bool | None = None

    fixRowHeaders: bool | None = None

    fontSize: FontSize | None = None

    fontStyle: Any | None = Field(
        default=None, description="Reference to VisualizationFontStyle. Length/value max=255."
    )

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    hideEmptyColumns: bool | None = None

    hideEmptyRowItems: HideEmptyItemStrategy | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    icons: list[Any] | None = Field(default=None, description="Collection of Icon. Length/value max=255.")

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    interpretations: list[Any] | None = Field(
        default=None, description="Collection of Interpretation. Read-only (inverse side)."
    )

    itemOrganisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnitGroup."
    )

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendDefinitions: Any | None = Field(default=None, description="Reference to LegendDefinitions.")

    measureCriteria: str | None = Field(default=None, description="Length/value max=255.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    noSpaceBetweenColumns: bool | None = None

    numberType: NumberType | None = None

    orgUnitField: str | None = Field(default=None, description="Length/value max=2147483647.")

    organisationUnitGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnitGroupSetDimension."
    )

    organisationUnitLevels: list[Any] | None = Field(default=None, description="Collection of Integer.")

    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")

    outlierAnalysis: Any | None = Field(default=None, description="Reference to OutlierAnalysis. Length/value max=255.")

    parentGraphMap: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    percentStackedValues: bool | None = None

    periods: list[Any] | None = Field(default=None, description="Collection of Period.")

    programIndicatorDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityProgramIndicatorDimension. Read-only (inverse side)."
    )

    rangeAxisDecimals: int | None = Field(default=None, description="Length/value max=2147483647.")

    rangeAxisLabel: str | None = Field(default=None, description="Length/value max=2147483647.")

    rangeAxisMaxValue: float | None = None

    rangeAxisMinValue: float | None = None

    rangeAxisSteps: int | None = Field(default=None, description="Length/value max=2147483647.")

    rawPeriods: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    regression: bool | None = None

    regressionType: RegressionType | None = None

    relatives: Any | None = Field(default=None, description="Reference to RelativePeriods. Read-only (inverse side).")

    reportingParams: Any | None = Field(default=None, description="Reference to ReportingParams.")

    rowDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    seriesItems: list[Any] | None = Field(default=None, description="Collection of Series. Length/value max=255.")

    seriesKey: Any | None = Field(default=None, description="Reference to SeriesKey. Length/value max=255.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    skipRounding: bool | None = None

    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")

    sortingItems: list[Any] | None = Field(default=None, description="Collection of Sorting. Length/value max=255.")

    startDate: datetime | None = None

    subscribed: bool | None = Field(default=None, description="Read-only.")

    subscribers: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    subtitle: str | None = Field(default=None, description="Length/value max=255.")

    targetLineLabel: str | None = Field(default=None, description="Length/value max=2147483647.")

    targetLineValue: float | None = None

    timeField: str | None = Field(default=None, description="Length/value max=2147483647.")

    title: str | None = Field(default=None, description="Length/value max=255.")

    topLimit: int | None = Field(default=None, description="Length/value max=2147483647.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    type: VisualizationType | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userOrgUnitType: UserOrgUnitType | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None

    visualizationPeriodName: str | None = Field(default=None, description="Length/value max=2147483647.")

    yearlySeries: list[Any] | None = Field(default=None, description="Collection of String.")
