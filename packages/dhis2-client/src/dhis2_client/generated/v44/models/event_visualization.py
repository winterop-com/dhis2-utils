"""Generated EventVisualization model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class EventVisualization(BaseModel):
    """DHIS2 EventVisualization resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationType: str | None = None

    attributeDimensions: list[Any] | None = None

    attributeValueDimension: Reference | None = None

    attributeValues: Any | None = None

    baseLineLabel: str | None = None

    baseLineValue: float | None = None

    categoryDimensions: list[Any] | None = None

    categoryOptionGroupSetDimensions: list[Any] | None = None

    code: str | None = None

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    collapseDataDimensions: bool | None = None

    columnDimensions: list[Any] | None = None

    columns: list[Any] | None = None

    completedOnly: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    cumulativeValues: bool | None = None

    dataDimensionItems: list[Any] | None = None

    dataElementDimensions: list[Any] | None = None

    dataElementGroupSetDimensions: list[Any] | None = None

    dataElementValueDimension: Reference | None = None

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

    eventRepetitions: list[Any] | None = None

    eventStatus: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    filterDimensions: list[Any] | None = None

    filters: list[Any] | None = None

    fixColumnHeaders: bool | None = None

    fixRowHeaders: bool | None = None

    fontSize: str | None = None

    formName: str | None = None

    hideEmptyColumns: bool | None = None

    hideEmptyRowItems: str | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideNaData: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    interpretations: list[Any] | None = None

    itemOrganisationUnitGroups: list[Any] | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legacy: bool | None = None

    legendDefinitions: Any | None = None

    metaData: Any | None = None

    name: str | None = None

    noSpaceBetweenColumns: bool | None = None

    orgUnitField: str | None = None

    organisationUnitGroupSetDimensions: list[Any] | None = None

    organisationUnitLevels: list[Any] | None = None

    organisationUnits: list[Any] | None = None

    outputType: str | None = None

    parentGraphMap: Any | None = None

    percentStackedValues: bool | None = None

    persistedPeriods: list[Any] | None = None

    program: Reference | None = None

    programDimensions: list[Any] | None = None

    programIndicatorDimensions: list[Any] | None = None

    programStage: Reference | None = None

    programStatus: str | None = None

    rangeAxisDecimals: int | None = None

    rangeAxisLabel: str | None = None

    rangeAxisMaxValue: float | None = None

    rangeAxisMinValue: float | None = None

    rangeAxisSteps: int | None = None

    rawPeriods: list[Any] | None = None

    regressionType: str | None = None

    relatives: Any | None = None

    rowDimensions: list[Any] | None = None

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = None

    sharing: Any | None = None

    shortName: str | None = None

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    simpleDimensions: list[Any] | None = None

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

    trackedEntityType: Reference | None = None

    translations: list[Any] | None = None

    type: str | None = None

    uid: str | None = None

    user: Reference | None = None

    userOrgUnitType: str | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None

    value: Reference | None = None
