"""Generated DataElement model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataElement(BaseModel):
    """DHIS2 DataElement resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationLevels: list[Any] | None = None

    aggregationType: str | None = None

    attributeValues: Any | None = None

    categoryCombo: Reference | None = None

    code: str | None = None

    commentOptionSet: Reference | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataSetElements: list[Any] | None = None

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    domainType: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    fieldMask: str | None = None

    formName: str | None = None

    groups: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legendSet: Reference | None = None

    legendSets: list[Any] | None = None

    name: str | None = None

    optionSet: Reference | None = None

    optionSetValue: bool | None = None

    queryMods: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    style: Any | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    url: str | None = None

    user: Reference | None = None

    valueType: str | None = None

    valueTypeOptions: Any | None = None

    zeroIsSignificant: bool | None = None
