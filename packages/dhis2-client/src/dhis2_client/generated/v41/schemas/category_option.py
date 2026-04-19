"""Generated CategoryOption model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import AggregationType, DimensionItemType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class CategoryOption(BaseModel):
    """DHIS2 Category Option - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/categoryOptions.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: AggregationType | None = None

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )

    categoryOptionCombos: list[Any] | None = Field(
        default=None, description="Collection of CategoryOptionCombo. Read-only (inverse side)."
    )

    categoryOptionGroups: list[Any] | None = Field(
        default=None, description="Collection of CategoryOptionGroup. Read-only (inverse side)."
    )

    categorys: list[Any] | None = Field(default=None, description="Collection of Category. Read-only (inverse side).")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    default: bool | None = Field(default=None, description="Read-only.")

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    dimensionItem: str | None = Field(default=None, description="Read-only.")

    dimensionItemType: DimensionItemType | None = None

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    endDate: datetime | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    formName: str | None = Field(default=None, description="Length/value min=2, max=230.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet. Read-only (inverse side).")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    organisationUnits: list[Any] | None = Field(default=None, description="Collection of OrganisationUnit.")

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Unique. Length/value min=1, max=50.")

    startDate: datetime | None = None

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
