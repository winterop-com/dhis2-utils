"""Generated MapView model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import (
    AggregationType,
    DigitGroupSeparator,
    EnrollmentStatus,
    HideEmptyItemStrategy,
    MappingEventStatus,
    MapViewRenderingStrategy,
    OrganisationUnitSelectionMode,
    RegressionType,
    ThematicMapType,
    UserOrgUnitType,
)


class MapView(BaseModel):
    """Generated model for DHIS2 `MapView`.

    DHIS2 Map View - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/mapViews.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    aggregationType: AggregationType | None = None
    areaRadius: int | None = None
    attributeDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
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
    classes: int | None = None
    code: str | None = None
    colSubTotals: bool | None = None
    colTotals: bool | None = None
    colorHigh: str | None = None
    colorLow: str | None = None
    colorScale: str | None = None
    columnDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    columns: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    completedOnly: bool | None = None
    config: str | None = None
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
    eventStatus: MappingEventStatus | None = None
    favorite: bool | None = None
    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    filterDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    filters: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    followUp: bool | None = None
    formName: str | None = None
    hidden: bool | None = None
    hideEmptyRowItems: HideEmptyItemStrategy | None = None
    hideEmptyRows: bool | None = None
    hideLegend: bool | None = None
    hideSubtitle: bool | None = None
    hideTitle: bool | None = None
    href: str | None = None
    id: str | None = None
    interpretations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    itemOrganisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    labelFontColor: str | None = None
    labelFontSize: str | None = None
    labelFontStyle: str | None = None
    labelFontWeight: str | None = None
    labelTemplate: str | None = None
    labels: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    layer: str | None = None
    legendDefinitions: Any | None = Field(
        default=None, description="Reference to LegendDefinitions. Read-only (inverse side)."
    )
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    metaData: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")
    method: int | None = None
    name: str | None = None
    noDataColor: str | None = None
    noSpaceBetweenColumns: bool | None = None
    opacity: float | None = None
    orgUnitField: str | None = None
    orgUnitFieldDisplayName: str | None = None
    organisationUnitColor: str | None = None
    organisationUnitGroupSet: Reference | None = Field(
        default=None, description="Reference to OrganisationUnitGroupSet. Read-only (inverse side)."
    )
    organisationUnitGroupSetDimensions: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    organisationUnitLevels: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    organisationUnitSelectionMode: OrganisationUnitSelectionMode | None = None
    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    parentGraph: str | None = None
    parentGraphMap: Any | None = Field(default=None, description="Reference to Map. Read-only (inverse side).")
    parentLevel: int | None = None
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
    radiusHigh: int | None = None
    radiusLow: int | None = None
    rawPeriods: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    regressionType: RegressionType | None = None
    relatives: Any | None = Field(default=None, description="Reference to RelativePeriods. Read-only (inverse side).")
    renderingStrategy: MapViewRenderingStrategy | None = None
    rowSubTotals: bool | None = None
    rowTotals: bool | None = None
    rows: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = None
    showData: bool | None = None
    showDimensionLabels: bool | None = None
    showHierarchy: bool | None = None
    skipRounding: bool | None = None
    sortOrder: int | None = None
    startDate: datetime | None = None
    styleDataItem: Any | None = Field(default=None, description="Reference to Object. Read-only (inverse side).")
    subscribed: bool | None = None
    subscribers: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    subtitle: str | None = None
    thematicMapType: ThematicMapType | None = None
    timeField: str | None = None
    title: str | None = None
    topLimit: int | None = None
    trackedEntityType: Reference | None = Field(
        default=None, description="Reference to TrackedEntityType. Read-only (inverse side)."
    )
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userOrgUnitType: UserOrgUnitType | None = None
    userOrganisationUnit: bool | None = None
    userOrganisationUnitChildren: bool | None = None
    userOrganisationUnitGrandChildren: bool | None = None
