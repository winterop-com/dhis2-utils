"""Generated Indicator model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DimensionItemType


class Indicator(BaseModel):
    """Generated model for DHIS2 `Indicator`.

    DHIS2 Indicator - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/indicators.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: AggregationType | None = None
    annualized: bool | None = None
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dataSets: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    decimals: int | None = None
    denominator: str | None = None
    denominatorDescription: str | None = None
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: DimensionItemType | None = None
    displayDenominatorDescription: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayNumeratorDescription: str | None = None
    displayShortName: str | None = None
    explodedDenominator: str | None = None
    explodedNumerator: str | None = None
    favorite: bool | None = None
    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    indicatorGroups: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    indicatorType: Reference | None = Field(
        default=None, description="Reference to IndicatorType. Read-only (inverse side)."
    )
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    legendSets: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    name: str | None = None
    numerator: str | None = None
    numeratorDescription: str | None = None
    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = None
    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Read-only (inverse side).")
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    url: str | None = None
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
