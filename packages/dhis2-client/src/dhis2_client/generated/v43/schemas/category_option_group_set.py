"""Generated CategoryOptionGroupSet model for DHIS2 v43. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DataDimensionType, DimensionType, ValueType


class CategoryOptionGroupSet(BaseModel):
    """Generated model for DHIS2 `CategoryOptionGroupSet`.

    DHIS2 Category Option Group Set - persisted metadata (generated from /api/schemas at DHIS2 v43).

    API endpoint: /api/categoryOptionGroupSets.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    aggregationType: AggregationType | None = None
    allItems: bool | None = None
    attributeValues: Any | None = Field(default=None, description="Reference to AttributeValues. Length/value max=255.")
    categoryOptionGroups: list[Any] | None = Field(default=None, description="Collection of CategoryOptionGroup.")
    code: str | None = Field(default=None, description="Unique. Length/value max=50.")
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User.")
    dataDimension: bool | None = None
    dataDimensionType: DataDimensionType | None = None
    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")
    dimension: str | None = Field(default=None, description="Length/value max=2147483647.")
    dimensionItemKeywords: Any | None = Field(
        default=None, description="Reference to DimensionItemKeywords. Read-only (inverse side)."
    )
    dimensionType: DimensionType | None = None
    displayDescription: str | None = Field(default=None, description="Read-only.")
    displayFormName: str | None = Field(default=None, description="Read-only.")
    displayName: str | None = Field(default=None, description="Read-only.")
    displayShortName: str | None = Field(default=None, description="Read-only.")
    eventRepetition: Any | None = Field(
        default=None, description="Reference to EventRepetition. Read-only (inverse side)."
    )
    favorite: bool | None = Field(default=None, description="Read-only.")
    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")
    filter: str | None = Field(default=None, description="Length/value max=2147483647.")
    formName: str | None = Field(default=None, description="Length/value max=2147483647.")
    href: str | None = None
    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")
    items: list[Any] | None = Field(
        default=None, description="Collection of DimensionalItemObject. Read-only (inverse side)."
    )
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")
    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet. Read-only (inverse side).")
    program: Reference | None = Field(default=None, description="Reference to Program. Read-only (inverse side).")
    programStage: Reference | None = Field(
        default=None, description="Reference to ProgramStage. Read-only (inverse side)."
    )
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")
    shortName: str | None = Field(default=None, description="Unique. Length/value min=1, max=50.")
    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    valueType: ValueType | None = Field(default=None, description="Read-only.")
