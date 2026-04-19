"""Generated ProgramIndicator model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import AggregationType, AnalyticsType, DimensionItemType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ProgramIndicator(BaseModel):
    """DHIS2 Program Indicator - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/programIndicators.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregateExportAttributeOptionCombo: str | None = Field(default=None, description="Length/value max=255.")

    aggregateExportCategoryOptionCombo: str | None = Field(default=None, description="Length/value max=255.")

    aggregationType: AggregationType | None = None

    analyticsPeriodBoundarys: list[Any] | None = Field(
        default=None, description="Collection of AnalyticsPeriodBoundary."
    )

    analyticsType: AnalyticsType | None = None

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    decimals: int | None = Field(default=None, description="Length/value max=2147483647.")

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    dimensionItem: str | None = Field(default=None, description="Read-only.")

    dimensionItemType: DimensionItemType | None = None

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayInForm: bool | None = None

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    expression: str | None = Field(default=None, description="Length/value max=2147483647.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    filter: str | None = Field(default=None, description="Length/value max=2147483647.")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    orgUnitField: str | None = Field(default=None, description="Length/value max=2147483647.")

    program: Reference | None = Field(default=None, description="Reference to Program.")

    programIndicatorGroups: list[Any] | None = Field(
        default=None, description="Collection of ProgramIndicatorGroup. Read-only (inverse side)."
    )

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Unique. Length/value min=1, max=50.")

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
