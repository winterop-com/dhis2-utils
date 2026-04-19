"""Generated DataElementGroupSet model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import AggregationType, DataDimensionType, DimensionType, ValueType


class DataElementGroupSet(BaseModel):
    """Generated model for DHIS2 `DataElementGroupSet`.

    DHIS2 Data Element Group Set - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/dataElementGroupSets.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")
    aggregationType: AggregationType | None = None
    allItems: bool | None = None
    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )
    code: str | None = None
    compulsory: bool | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    dataDimension: bool | None = None
    dataDimensionType: DataDimensionType | None = None
    dataElementGroups: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )
    description: str | None = None
    dimension: str | None = None
    dimensionItemKeywords: Any | None = Field(
        default=None, description="Reference to DimensionItemKeywords. Read-only (inverse side)."
    )
    dimensionType: DimensionType | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    eventRepetition: Any | None = Field(
        default=None, description="Reference to EventRepetition. Read-only (inverse side)."
    )
    favorite: bool | None = None
    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    filter: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    items: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")
    lastUpdated: datetime | None = None
    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")
    name: str | None = None
    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet. Read-only (inverse side).")
    program: Reference | None = Field(default=None, description="Reference to Program. Read-only (inverse side).")
    programStage: Reference | None = Field(
        default=None, description="Reference to ProgramStage. Read-only (inverse side)."
    )
    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")
    shortName: str | None = None
    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")
    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    valueType: ValueType | None = None
