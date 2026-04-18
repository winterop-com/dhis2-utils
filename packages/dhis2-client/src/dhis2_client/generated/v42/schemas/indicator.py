"""Generated Indicator model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Indicator(BaseModel):
    """DHIS2 Indicator - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/indicators.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregateExportAttributeOptionCombo: str | None = Field(default=None, description="Length/value max=255.")

    aggregateExportCategoryOptionCombo: str | None = Field(default=None, description="Length/value max=255.")

    aggregationType: str | None = None

    annualized: bool | None = None

    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    dataSets: list[Any] | None = Field(default=None, description="Collection of DataSet. Read-only (inverse side).")

    decimals: int | None = Field(default=None, description="Length/value max=2147483647.")

    denominator: str | None = Field(default=None, description="Length/value max=2147483647.")

    denominatorDescription: str | None = Field(default=None, description="Length/value max=2147483647.")

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    dimensionItem: str | None = Field(default=None, description="Read-only.")

    dimensionItemType: str | None = None

    displayDenominatorDescription: str | None = Field(default=None, description="Read-only.")

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayNumeratorDescription: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    explodedDenominator: str | None = Field(default=None, description="Length/value max=2147483647.")

    explodedNumerator: str | None = Field(default=None, description="Length/value max=2147483647.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    groups: list[Any] | None = Field(
        default=None, description="Collection of IndicatorGroup. Read-only (inverse side)."
    )

    href: str | None = None

    indicatorType: Reference | None = Field(default=None, description="Reference to IndicatorType.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet.")

    name: str | None = Field(default=None, description="Length/value min=1, max=230.")

    numerator: str | None = Field(default=None, description="Length/value max=2147483647.")

    numeratorDescription: str | None = Field(default=None, description="Length/value max=2147483647.")

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=50.")

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    uid: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    url: str | None = Field(default=None, description="Length/value max=255.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
