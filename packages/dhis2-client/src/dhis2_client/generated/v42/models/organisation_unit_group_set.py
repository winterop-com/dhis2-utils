"""Generated OrganisationUnitGroupSet model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class OrganisationUnitGroupSet(BaseModel):
    """DHIS2 OrganisationUnitGroupSet resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    aggregationType: str | None = None

    allItems: bool | None = None

    attributeValues: Any | None = None

    code: str | None = None

    compulsory: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataDimension: bool | None = None

    dataDimensionType: str | None = None

    description: str | None = None

    dimension: str | None = None

    dimensionItemKeywords: Any | None = None

    dimensionType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    eventRepetition: Any | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    filter: str | None = None

    formName: str | None = None

    href: str | None = None

    includeSubhierarchyInAnalytics: bool | None = None

    items: list[Any] | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    legendSet: Reference | None = None

    name: str | None = None

    optionSet: Reference | None = None

    organisationUnitGroups: list[Any] | None = None

    program: Reference | None = None

    programStage: Reference | None = None

    sharing: Any | None = None

    shortName: str | None = None

    translations: list[Any] | None = None

    uid: str | None = None

    user: Reference | None = None

    valueType: str | None = None
