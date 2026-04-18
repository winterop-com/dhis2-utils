"""Generated DataElement model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class DataElement(BaseModel):
    """DHIS2 Data Element - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/dataElements.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    aggregationLevels: list[Any] | None = Field(
        default=None, description="Collection of List. Read-only (inverse side)."
    )

    aggregationType: str | None = None

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    categoryCombo: Reference | None = Field(
        default=None, description="Reference to CategoryCombo. Read-only (inverse side)."
    )

    code: str | None = None

    commentOptionSet: Reference | None = Field(
        default=None, description="Reference to OptionSet. Read-only (inverse side)."
    )

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataSetElements: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    description: str | None = None

    dimensionItem: str | None = None

    dimensionItemType: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    domainType: str | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    fieldMask: str | None = None

    formName: str | None = None

    groups: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    href: str | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    legendSet: Reference | None = Field(default=None, description="Reference to LegendSet. Read-only (inverse side).")

    legendSets: list[Any] | None = Field(default=None, description="Collection of List. Read-only (inverse side).")

    name: str | None = None

    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet. Read-only (inverse side).")

    optionSetValue: bool | None = None

    queryMods: Any | None = Field(default=None, description="Reference to QueryModifiers. Read-only (inverse side).")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    style: Any | None = Field(default=None, description="Reference to ObjectStyle. Read-only (inverse side).")

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    uid: str | None = None

    url: str | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    valueType: str | None = None

    valueTypeOptions: Any | None = Field(
        default=None, description="Reference to ValueTypeOptions. Read-only (inverse side)."
    )

    zeroIsSignificant: bool | None = None
