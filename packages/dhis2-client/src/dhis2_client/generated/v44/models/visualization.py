"""Generated Visualization model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Visualization(BaseModel):
    """DHIS2 Visualization resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationType: str | None = None

    attributeDimensions: list[Any] | None = None

    attributeValues: Any | None = None

    axes: list[Any] | None = None

    baseLineLabel: str | None = None

    baseLineValue: float | None = None

    categoryDimensions: list[Any] | None = None

    categoryOptionGroupSetDimensions: list[Any] | None = None

    code: str | None = None

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    colorSet: str | None = None

    columnDimensions: list[Any] | None = None

    columns: list[Any] | None = None

    completedOnly: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    cumulativeValues: bool | None = None

    dataDimensionItems: list[Any] | None = None

    dataElementDimensions: list[Any] | None = None

    dataElementGroupSetDimensions: list[Any] | None = None

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

    favorite: bool | None = None

    favorites: list[Any] | None = None

    filterDimensions: list[Any] | None = None

    filters: list[Any] | None = None

    fixColumnHeaders: bool | None = None

    fixRowHeaders: bool | None = None

    fontSize: str | None = None

    fontStyle: Any | None = None

    formName: str | None = None

    hideEmptyColumns: bool | None = None

    hideEmptyRowItems: str | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    icons: list[Any] | None = None

    interpretations: list[Any] | None = None

    itemOrganisationUnitGroups: list[Any] | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legendDefinitions: Any | None = None

    measureCriteria: str | None = None

    metaData: Any | None = None

    name: str | None = None

    noSpaceBetweenColumns: bool | None = None

    numberType: str | None = None

    optionalAxes: list[Any] | None = None

    orgUnitField: str | None = None

    organisationUnitGroupSetDimensions: list[Any] | None = None

    organisationUnitLevels: list[Any] | None = None

    organisationUnits: list[Any] | None = None

    outlierAnalysis: Any | None = None

    parentGraphMap: Any | None = None

    percentStackedValues: bool | None = None

    persistedPeriods: list[Any] | None = None

    programIndicatorDimensions: list[Any] | None = None

    rangeAxisDecimals: int | None = None

    rangeAxisLabel: str | None = None

    rangeAxisMaxValue: float | None = None

    rangeAxisMinValue: float | None = None

    rangeAxisSteps: int | None = None

    rawPeriods: list[Any] | None = None

    regression: bool | None = None

    regressionType: str | None = None

    relatives: Any | None = None

    reportingParams: Any | None = None

    rowDimensions: list[Any] | None = None

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = None

    series: list[Any] | None = None

    seriesKey: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    skipRounding: bool | None = None

    sortOrder: int | None = None

    sorting: list[Any] | None = None

    startDate: datetime | None = None

    subscribed: bool | None = None

    subscribers: list[Any] | None = None

    subtitle: str | None = None

    targetLineLabel: str | None = None

    targetLineValue: float | None = None

    timeField: str | None = None

    title: str | None = None

    topLimit: int | None = None

    translations: list[Any] | None = None

    type: str | None = None

    uid: str | None = None

    user: Reference | None = None

    userOrgUnitType: str | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None

    visualizationPeriodName: str | None = None

    yearlySeries: list[Any] | None = None
