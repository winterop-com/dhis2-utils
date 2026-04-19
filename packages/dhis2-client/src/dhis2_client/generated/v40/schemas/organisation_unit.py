"""Generated OrganisationUnit model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DimensionItemType
from .attribute_value import AttributeValue


class OrganisationUnit(BaseModel):
    """Generated model for DHIS2 `OrganisationUnit`.

    DHIS2 Organisation Unit - persisted metadata (generated from /api/schemas at DHIS2 v40).

    API endpoint: /api/organisationUnits.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    address: str | None = Field(default=None, description="Length/value max=255.")
    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )
    childs: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnit. Read-only (inverse side)."
    )
    closedDate: datetime | None = None
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    comment: str | None = Field(default=None, description="Length/value max=2147483647.")
    contactPerson: str | None = Field(default=None, description="Length/value max=255.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dataSets: list[Any] | None = Field(default=None, description="Collection of DataSet. Read-only (inverse side).")
    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    dimensionItem: str | None = Field(default=None, description="Read-only.")
    dimensionItemType: DimensionItemType | None = None
    displayDescription: str | None = Field(default=None, description="Read-only.")
    displayFormName: str | None = Field(default=None, description="Read-only.")
    displayName: str | None = Field(default=None, description="Read-only.")
    displayShortName: str | None = Field(default=None, description="Read-only.")
    email: str | None = Field(default=None, description="Length/value max=150.")
    externalAccess: bool | None = None
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    formName: str | None = Field(default=None, description="Length/value max=2147483647.")
    geometry: Any | None = Field(default=None, description="Reference to Geometry. Length/value max=131072.")
    hierarchyLevel: str | None = Field(default=None, description="Length/value max=2147483647.")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    image: Reference | None = Field(default=None, description="Reference to FileResource.")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    leaf: bool | None = Field(default=None, description="Read-only.")
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet. Read-only (inverse side).")
    memberCount: int | None = Field(default=None, description="Length/value max=2147483647.")
    name: str | None = Field(default=None, description="Length/value min=1, max=230.")
    openingDate: datetime | None = None
    organisationUnitGroups: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnitGroup. Read-only (inverse side)."
    )
    organisationUnits: list[Any] | None = Field(
        default=None, description="Collection of OrganisationUnit. Read-only (inverse side)."
    )
    parent: Reference | None = Field(default=None, description="Reference to OrganisationUnit.")
    path: str | None = Field(default=None, description="Unique. Length/value max=255.")
    phoneNumber: str | None = Field(default=None, description="Length/value max=150.")
    programs: list[Any] | None = Field(default=None, description="Collection of Program. Read-only (inverse side).")
    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")
    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = Field(default=None, description="Length/value min=1, max=50.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    type: str | None = Field(default=None, description="Length/value max=2147483647.")
    url: str | None = Field(default=None, description="Length/value max=255.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    userAccess: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )
    userGroupAccess: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )
    userItems: list[Any] | None = Field(default=None, description="Collection of User. Read-only (inverse side).")
