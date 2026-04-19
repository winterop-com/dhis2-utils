"""Generated ProgramDataElementDimensionItem model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DimensionItemType, ValueType


class ProgramDataElementDimensionItem(BaseModel):
    """Generated model for DHIS2 `ProgramDataElementDimensionItem`.

    DHIS2 Program Data Element Dimension Item - DHIS2 resource (generated from /api/schemas at DHIS2 v42).


    API endpoint: /api/programDataElements.


    Transient — not stored in the DHIS2 database (computed / projection).


    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationType: AggregationType | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataElement: Reference | None = Field(
        default=None, description="Reference to DataElement. Read-only (inverse side)."
    )

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    dimensionItem: str | None = Field(default=None, description="Read-only.")

    dimensionItemType: DimensionItemType | None = None

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    id: str | None = Field(default=None, description="Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet. Read-only (inverse side).")

    name: str | None = Field(default=None, description="Length/value max=2147483647.")

    program: Reference | None = Field(default=None, description="Reference to Program. Read-only (inverse side).")

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = Field(default=None, description="Length/value max=2147483647.")

    translations: list[Any] | None = Field(
        default=None, description="Collection of Translation. Read-only (inverse side)."
    )

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    valueType: ValueType | None = Field(default=None, description="Read-only.")
