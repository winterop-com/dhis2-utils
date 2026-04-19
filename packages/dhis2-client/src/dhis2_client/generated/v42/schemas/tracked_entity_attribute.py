"""Generated TrackedEntityAttribute model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import AggregationType, DimensionItemType, ValueType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class TrackedEntityAttribute(BaseModel):
    """DHIS2 Tracked Entity Attribute - persisted metadata (generated from /api/schemas at DHIS2 v42).

    API endpoint: /api/trackedEntityAttributes.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: AggregationType | None = None

    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    confidential: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    description: str | None = Field(default=None, description="Length/value min=2, max=2147483647.")

    dimensionItem: str | None = Field(default=None, description="Read-only.")

    dimensionItemType: DimensionItemType | None = None

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayInListNoProgram: bool | None = None

    displayName: str | None = Field(default=None, description="Read-only.")

    displayOnVisitSchedule: bool | None = None

    displayShortName: str | None = Field(default=None, description="Read-only.")

    expression: str | None = Field(default=None, description="Length/value max=255.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    fieldMask: str | None = Field(default=None, description="Length/value max=255.")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    generated: bool | None = None

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    inherit: bool | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet.")

    optionSetValue: bool | None = Field(default=None, description="Read-only.")

    orgunitScope: bool | None = None

    pattern: str | None = Field(default=None, description="Length/value max=255.")

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Unique. Length/value min=1, max=50.")

    skipSynchronization: bool | None = None

    sortOrderInListNoProgram: int | None = Field(default=None, description="Length/value max=2147483647.")

    sortOrderInVisitSchedule: int | None = Field(default=None, description="Length/value max=2147483647.")

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    unique: bool | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    valueType: ValueType | None = None
