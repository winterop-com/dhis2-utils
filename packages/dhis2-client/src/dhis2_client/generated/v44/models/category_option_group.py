"""Generated CategoryOptionGroup model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class CategoryOptionGroup(BaseModel):
    """DHIS2 CategoryOptionGroup resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationType: str | None = None

    attributeValues: Any | None = None

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataDimensionType: str | None = None

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    formName: str | None = None

    groupSets: list[Any] | None = None

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legendSet: Reference | None = None

    legendSets: list[Any] | None = None

    members: list[Any] | None = None

    name: str | None = None

    queryMods: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None
