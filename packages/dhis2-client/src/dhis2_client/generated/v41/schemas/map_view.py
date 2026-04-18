"""Generated MapView model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class MapView(BaseModel):
    """DHIS2 Map View - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/mapViews.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: str | None = None

    areaRadius: int | None = Field(default=None, description="Length/value max=2147483647.")

    attributeDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityAttributeDimension."
    )

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )

    categoryDimensions: list[Any] | None = Field(default=None, description="Collection of CategoryDimension.")

    categoryOptionGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of CategoryOptionGroupSetDimension."
    )

    classes: int | None = Field(default=None, description="Length/value max=2147483647.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    colSubTotals: bool | None = None

    colTotals: bool | None = None

    colorHigh: str | None = Field(default=None, description="Length/value max=255.")

    colorLow: str | None = Field(default=None, description="Length/value max=255.")

    colorScale: str | None = Field(default=None, description="Length/value max=255.")

    columnDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    columns: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    completedOnly: bool | None = None

    config: str | None = Field(default=None, description="Length/value max=2147483647.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    cumulativeValues: bool | None = None

    dataDimensionItems: list[Any] | None = Field(default=None, description="Collection of DataDimensionItem.")

    dataElementDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityDataElementDimension."
    )

    dataElementGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of DataElementGroupSetDimension. Read-only (inverse side)."
    )

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    digitGroupSeparator: str | None = None

    displayBaseLineLabel: str | None = Field(default=None, description="Read-only.")

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    displaySubtitle: str | None = Field(default=None, description="Read-only.")

    displayTargetLineLabel: str | None = Field(default=None, description="Read-only.")

    displayTitle: str | None = Field(default=None, description="Read-only.")

    endDate: datetime | None = None

    eventClustering: bool | None = None

    eventCoordinateField: str | None = Field(default=None, description="Length/value max=255.")

    eventPointColor: str | None = Field(default=None, description="Length/value max=255.")

    eventPointRadius: int | None = Field(default=None, description="Length/value max=2147483647.")

    eventStatus: str | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    filterDimensions: list[Any] | None = Field(default=None, description="Collection of String.")

    filters: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    followUp: bool | None = None

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    hidden: bool | None = None

    hideEmptyRowItems: str | None = None

    hideEmptyRows: bool | None = None

    hideLegend: bool | None = None

    hideSubtitle: bool | None = None

    hideTitle: bool | None = None

    href: str | None = None

    interpretations: list[Any] | None = Field(
        default=None, description="Collection of Interpretation. Read-only (inverse side)."
    )

    itemOrganisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnitGroup."
    )

    labelFontColor: str | None = Field(default=None, description="Length/value max=255.")

    labelFontSize: str | None = Field(default=None, description="Length/value max=255.")

    labelFontStyle: str | None = Field(default=None, description="Length/value max=255.")

    labelFontWeight: str | None = Field(default=None, description="Length/value max=255.")

    labelTemplate: str | None = Field(default=None, description="Length/value max=50.")

    labels: bool | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    layer: str | None = Field(default=None, description="Length/value max=255.")

    legendDefinitions: Any | None = Field(
        default=None, description="Reference to LegendDefinitions. Read-only (inverse side)."
    )

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet.")

    method: int | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Length/value max=2147483647.")

    noDataColor: str | None = Field(default=None, description="Length/value min=7, max=7.")

    noSpaceBetweenColumns: bool | None = None

    opacity: float | None = None

    orgUnitField: str | None = Field(default=None, description="Length/value max=255.")

    orgUnitFieldDisplayName: str | None = Field(default=None, description="Length/value max=2147483647.")

    organisationUnitColor: str | None = Field(default=None, description="Length/value min=7, max=7.")

    organisationUnitGroupSet: Reference | None = Field(
        default=None, description="Reference to OrganisationUnitGroupSet."
    )

    organisationUnitGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnitGroupSetDimension."
    )

    organisationUnitLevels: list[Any] | None = Field(default=None, description="Collection of Integer.")

    organisationUnitSelectionMode: str | None = None

    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")

    parentGraph: str | None = Field(default=None, description="Length/value max=2147483647.")

    parentGraphMap: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")

    parentLevel: int | None = Field(default=None, description="Length/value max=2147483647.")

    percentStackedValues: bool | None = None

    periods: list[Any] | None = Field(default=None, description="Collection of Period.")

    program: Reference | None = Field(default=None, description="Reference to Program.")

    programIndicatorDimensions: list[Any] | None = Field(
        default=None, description="Collection of TrackedEntityProgramIndicatorDimension. Read-only (inverse side)."
    )

    programStage: Reference | None = Field(default=None, description="Reference to ProgramStage.")

    programStatus: str | None = None

    radiusHigh: int | None = Field(default=None, description="Length/value max=2147483647.")

    radiusLow: int | None = Field(default=None, description="Length/value max=2147483647.")

    rawPeriods: list[Any] | None = Field(default=None, description="Collection of String. Length/value max=255.")

    regressionType: str | None = None

    relatives: Any | None = Field(default=None, description="Reference to RelativePeriods. Read-only (inverse side).")

    renderingStrategy: str | None = None

    rowSubTotals: bool | None = None

    rowTotals: bool | None = None

    rows: list[Any] | None = Field(
        default=None, description="Collection of DimensionalObject. Read-only (inverse side)."
    )

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    showData: bool | None = None

    showDimensionLabels: bool | None = None

    showHierarchy: bool | None = None

    skipRounding: bool | None = None

    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")

    startDate: datetime | None = None

    styleDataItem: Any | None = Field(default=None, description="Reference to Object. Length/value max=255.")

    subscribed: bool | None = Field(default=None, description="Read-only.")

    subscribers: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    subtitle: str | None = Field(default=None, description="Length/value max=2147483647.")

    thematicMapType: str | None = None

    timeField: str | None = Field(default=None, description="Length/value max=2147483647.")

    title: str | None = Field(default=None, description="Length/value max=2147483647.")

    topLimit: int | None = Field(default=None, description="Length/value max=2147483647.")

    trackedEntityType: Reference | None = Field(default=None, description="Reference to TrackedEntityType.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userOrgUnitType: str | None = None

    userOrganisationUnit: bool | None = None

    userOrganisationUnitChildren: bool | None = None

    userOrganisationUnitGrandChildren: bool | None = None
