"""Generated Visualization model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
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


class Visualization(BaseModel):
    """Generated model for DHIS2 `Visualization`.

    DHIS2 Visualization - persisted metadata (generated from /api/schemas at DHIS2 v44).


    API endpoint: /dev/api/visualizations.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: AggregationType | None = None

    attributeDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    axes: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    axis: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    baseLineLabel: str | None = None

    baseLineValue: float | None = None

    categoryDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    categoryOptionGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    code: str | None = None

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    colorSet: str | None = None

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

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    filterDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    filters: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    fixColumnHeaders: bool | None = None

    fixRowHeaders: bool | None = None

    fontSize: FontSize | None = None

    fontStyle: Any | None = Field(
        default=None, description="Reference to VisualizationFontStyle. Read-only (inverse side)."
    )

    formName: str | None = None

    hideEmptyColumns: bool | None = None

    hideEmptyRowItems: HideEmptyItemStrategy | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    icons: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    id: str | None = None

    interpretations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    itemOrganisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    legendDefinitions: Any | None = Field(
        default=None, description="Reference to LegendDefinitions. Read-only (inverse side)."
    )

    measureCriteria: str | None = None

    metaData: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    name: str | None = None

    noSpaceBetweenColumns: bool | None = None

    numberType: NumberType | None = None

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

    outlierAnalysis: Any | None = Field(
        default=None, description="Reference to OutlierAnalysis. Read-only (inverse side)."
    )

    parentGraphMap: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    percentStackedValues: bool | None = None

    periods: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    programIndicatorDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    rangeAxisDecimals: int | None = None

    rangeAxisLabel: str | None = None

    rangeAxisMaxValue: float | None = None

    rangeAxisMinValue: float | None = None

    rangeAxisSteps: int | None = None

    rawPeriods: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    regression: bool | None = None

    regressionType: RegressionType | None = None

    relatives: Any | None = Field(default=None, description="Reference to RelativePeriods. Read-only (inverse side).")

    reportingParams: Any | None = Field(
        default=None, description="Reference to ReportingParams. Read-only (inverse side)."
    )

    rowDimensions: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    seriesItems: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    seriesKey: Any | None = Field(default=None, description="Reference to SeriesKey. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    skipRounding: bool | None = None

    sortOrder: int | None = None

    sortingItems: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    startDate: datetime | None = None

    subscribed: bool | None = None

    subscribers: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    subtitle: str | None = None

    targetLineLabel: str | None = None

    targetLineValue: float | None = None

    timeField: str | None = None

    title: str | None = None

    topLimit: int | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    type: VisualizationType | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userOrgUnitType: UserOrgUnitType | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None

    visualizationPeriodName: str | None = None

    yearlySeries: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
