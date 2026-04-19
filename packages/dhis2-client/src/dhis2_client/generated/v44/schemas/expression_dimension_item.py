"""Generated ExpressionDimensionItem model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import AggregationType, DimensionItemType, MissingValueStrategy


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class ExpressionDimensionItem(BaseModel):
    """DHIS2 Expression Dimension Item - persisted metadata (generated from /api/schemas at DHIS2 v44).

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregateExportAttributeOptionCombo: str | None = None

    aggregateExportCategoryOptionCombo: str | None = None

    aggregationType: AggregationType | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    code: str | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: DimensionItemType | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    expression: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    formName: str | None = None

    href: str | None = None

    id: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    missingValueStrategy: MissingValueStrategy | None = None

    name: str | None = None

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    slidingWindow: bool | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
