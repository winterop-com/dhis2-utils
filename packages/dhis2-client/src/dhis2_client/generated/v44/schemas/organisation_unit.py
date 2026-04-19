"""Generated OrganisationUnit model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DimensionItemType


class OrganisationUnit(BaseModel):
    """Generated model for DHIS2 `OrganisationUnit`.

    DHIS2 Organisation Unit - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/organisationUnits.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    address: str | None = None
    aggregationType: AggregationType | None = None
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    childs: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    closedDate: datetime | None = None
    code: str | None = None
    comment: str | None = None
    contactPerson: str | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dataSets: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: DimensionItemType | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    email: str | None = None
    favorite: bool | None = None
    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    formName: str | None = None
    geometry: Any | None = Field(default=None, description="Reference to Geometry. Read-only (inverse side).")
    hierarchyLevel: int | None = None
    href: str | None = None
    id: str | None = None
    image: Reference | None = Field(default=None, description="Reference to FileResource. Read-only (inverse side).")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    leaf: bool | None = None
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    legendSets: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    memberCount: int | None = None
    name: str | None = None
    openingDate: datetime | None = None
    organisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of Set. Read-only (inverse side)."
    )
    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    parent: Reference | None = Field(
        default=None, description="Reference to OrganisationUnit. Read-only (inverse side)."
    )
    path: str | None = None
    phoneNumber: str | None = None
    programs: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = None
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    type: str | None = None
    url: str | None = None
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userItems: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
