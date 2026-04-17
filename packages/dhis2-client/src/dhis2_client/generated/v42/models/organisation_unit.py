"""Generated OrganisationUnit model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class OrganisationUnit(BaseModel):
    """DHIS2 OrganisationUnit resource."""

    model_config = ConfigDict(extra="allow")

    access: Any | None = None

    address: str | None = None

    aggregationType: str | None = None

    ancestors: list[Any] | None = None

    attributeValues: Any | None = None

    children: list[Any] | None = None

    closedDate: datetime | None = None

    code: str | None = None

    comment: str | None = None

    contactPerson: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = None

    dataSets: list[Any] | None = None

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    email: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = None

    formName: str | None = None

    geometry: Any | None = None

    groups: list[Any] | None = None

    hierarchyLevel: int | None = None

    href: str | None = None

    image: Reference | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = None

    leaf: bool | None = None

    legendSet: Reference | None = None

    legendSets: list[Any] | None = None

    memberCount: int | None = None

    name: str | None = None

    openingDate: datetime | None = None

    parent: Reference | None = None

    path: str | None = None

    phoneNumber: str | None = None

    programs: list[Any] | None = None

    queryMods: Any | None = None

    sharing: Any | None = None

    shortName: str | None = None

    translations: list[Any] | None = None

    type: str | None = None

    uid: str | None = None

    url: str | None = None

    user: Reference | None = None

    users: list[Any] | None = None
