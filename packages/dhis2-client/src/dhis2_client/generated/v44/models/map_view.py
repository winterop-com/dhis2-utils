"""Generated MapView model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class MapView(BaseModel):
    """DHIS2 MapView resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationType: str | None = None

    areaRadius: int | None = None

    attributeDimensions: list[Any] | None = None

    attributeValues: Any | None = None

    categoryDimensions: list[Any] | None = None

    categoryOptionGroupSetDimensions: list[Any] | None = None

    classes: int | None = None

    code: str | None = None

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    colorHigh: str | None = None

    colorLow: str | None = None

    colorScale: str | None = None

    columnDimensions: list[Any] | None = None

    columns: list[Any] | None = None

    completedOnly: bool | None = None

    config: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    cumulativeValues: bool | None = None

    dataDimensionItems: list[Any] | None = None

    dataElementDimensions: list[Any] | None = None

    dataElementGroupSetDimensions: list[Any] | None = None

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

    eventCoordinateFieldFallback: str | None = None

    eventPointColor: str | None = None

    eventPointRadius: int | None = None

    eventStatus: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    filterDimensions: list[Any] | None = None

    filters: list[Any] | None = None

    followUp: bool | None = None

    formName: str | None = None

    hidden: bool | None = None

    hideEmptyRowItems: str | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    interpretations: list[Any] | None = None

    itemOrganisationUnitGroups: list[Any] | None = None

    labelFontColor: str | None = None

    labelFontSize: str | None = None

    labelFontStyle: str | None = None

    labelFontWeight: str | None = None

    labelTemplate: str | None = None

    labels: bool | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    layer: str | None = None

    legendDefinitions: Any | None = None

    legendSet: Reference | None = None

    metaData: Any | None = None

    method: int | None = None

    name: str | None = None

    noDataColor: str | None = None

    noSpaceBetweenColumns: bool | None = None

    opacity: float | None = None

    orgUnitField: str | None = None

    orgUnitFieldDisplayName: str | None = None

    organisationUnitColor: str | None = None

    organisationUnitGroupSet: Reference | None = None

    organisationUnitGroupSetDimensions: list[Any] | None = None

    organisationUnitLevels: list[Any] | None = None

    organisationUnitSelectionMode: str | None = None

    organisationUnits: list[Any] | None = None

    parentGraph: str | None = None

    parentGraphMap: Any | None = None

    parentLevel: int | None = None

    percentStackedValues: bool | None = None

    persistedPeriods: list[Any] | None = None

    program: Reference | None = None

    programIndicatorDimensions: list[Any] | None = None

    programStage: Reference | None = None

    programStatus: str | None = None

    radiusHigh: int | None = None

    radiusLow: int | None = None

    rawPeriods: list[Any] | None = None

    regressionType: str | None = None

    relatives: Any | None = None

    renderingStrategy: str | None = None

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = None

    sharing: Any | None = None

    shortName: str | None = None

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    skipRounding: bool | None = None

    sortOrder: int | None = None

    startDate: datetime | None = None

    styleDataItem: Any | None = None

    subscribed: bool | None = None

    subscribers: list[Any] | None = None

    subtitle: str | None = None

    thematicMapType: str | None = None

    timeField: str | None = None

    title: str | None = None

    topLimit: int | None = None

    trackedEntityType: Reference | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    userOrgUnitType: str | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None
