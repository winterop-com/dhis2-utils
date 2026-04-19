"""Generated DataElement model for DHIS2 v41. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import AggregationType, DataElementDomain, DimensionItemType, ValueType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataElement(BaseModel):
    """DHIS2 Data Element - persisted metadata (generated from /api/schemas at DHIS2 v41).

    API endpoint: /api/dataElements.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationLevels: list[Any] | None = Field(default=None, description="Collection of Integer.")

    aggregationType: AggregationType | None = None

    attributeValues: list[Any] | None = Field(
        default=None, description="Collection of AttributeValue. Length/value max=255."
    )

    categoryCombo: Reference | None = Field(default=None, description="Reference to CategoryCombo.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    commentOptionSet: Reference | None = Field(default=None, description="Reference to OptionSet.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    dataElementGroups: list[Any] | None = Field(
        default=None, description="Collection of DataElementGroup. Read-only (inverse side)."
    )

    dataSetElements: list[Any] | None = Field(
        default=None, description="Collection of DataSetElement. Read-only (inverse side)."
    )

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    dimensionItem: str | None = Field(default=None, description="Read-only.")

    dimensionItemType: DimensionItemType | None = None

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    domainType: DataElementDomain | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    fieldMask: str | None = Field(default=None, description="Length/value max=255.")

    formName: str | None = Field(default=None, description="Length/value min=2, max=230.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of LegendSet.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet.")

    optionSetValue: bool | None = Field(default=None, description="Read-only.")

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Unique. Length/value min=1, max=50.")

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Length/value max=255.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    url: str | None = Field(default=None, description="Length/value max=255.")

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    valueType: ValueType | None = None

    valueTypeOptions: Any | None = Field(
        default=None, description="Reference to ValueTypeOptions. Length/value max=255."
    )

    zeroIsSignificant: bool | None = None
