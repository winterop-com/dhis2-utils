"""Generated Indicator model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Indicator(BaseModel):
    """DHIS2 Indicator resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregateExportAttributeOptionCombo: str | None = None

    aggregateExportCategoryOptionCombo: str | None = None

    aggregationType: str | None = None

    annualized: bool | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataSets: list[Any] | None = None

    decimals: int | None = None

    denominator: str | None = None

    denominatorDescription: str | None = None

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDenominatorDescription: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayNumeratorDescription: str | None = None

    displayShortName: str | None = None

    explodedDenominator: str | None = None

    explodedNumerator: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    formName: str | None = None

    groups: list[Any] | None = None

    href: str | None = None

    indicatorType: Reference | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legendSet: Reference | None = None

    legendSets: list[Any] | None = None

    name: str | None = None

    numerator: str | None = None

    numeratorDescription: str | None = None

    queryMods: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    style: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    url: str | None = None

    user: Reference | None = None
