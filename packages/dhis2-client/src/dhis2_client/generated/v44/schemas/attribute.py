"""Generated Attribute model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..enums import ValueType


class Reference(BaseModel):
    """Minimal reference to another DHIS2 metadata object."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None


class Attribute(BaseModel):
    """DHIS2 Attribute - persisted metadata (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/attributes.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow")

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    categoryAttribute: bool | None = None

    categoryOptionAttribute: bool | None = None

    categoryOptionComboAttribute: bool | None = None

    categoryOptionGroupAttribute: bool | None = None

    categoryOptionGroupSetAttribute: bool | None = None

    code: str | None = None

    constantAttribute: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    dataElementAttribute: bool | None = None

    dataElementGroupAttribute: bool | None = None

    dataElementGroupSetAttribute: bool | None = None

    dataSetAttribute: bool | None = None

    description: str | None = None

    displayDescription: str | None = None

    displayFormName: str | None = None

    displayName: str | None = None

    displayShortName: str | None = None

    documentAttribute: bool | None = None

    eventChartAttribute: bool | None = None

    eventReportAttribute: bool | None = None

    favorite: bool | None = None

    favorites: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    formName: str | None = None

    href: str | None = None

    id: str | None = None

    indicatorAttribute: bool | None = None

    indicatorGroupAttribute: bool | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    legendSetAttribute: bool | None = None

    mandatory: bool | None = None

    mapAttribute: bool | None = None

    name: str | None = None

    objectTypes: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    optionAttribute: bool | None = None

    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet. Read-only (inverse side).")

    optionSetAttribute: bool | None = None

    organisationUnitAttribute: bool | None = None

    organisationUnitGroupAttribute: bool | None = None

    organisationUnitGroupSetAttribute: bool | None = None

    programAttribute: bool | None = None

    programIndicatorAttribute: bool | None = None

    programStageAttribute: bool | None = None

    relationshipTypeAttribute: bool | None = None

    sectionAttribute: bool | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Read-only (inverse side).")

    shortName: str | None = None

    sortOrder: int | None = None

    sqlViewAttribute: bool | None = None

    trackedEntityAttributeAttribute: bool | None = None

    trackedEntityTypeAttribute: bool | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Set. Read-only (inverse side).")

    unique: bool | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAttribute: bool | None = None

    userGroupAttribute: bool | None = None

    validationRuleAttribute: bool | None = None

    validationRuleGroupAttribute: bool | None = None

    valueType: ValueType | None = None

    visualizationAttribute: bool | None = None
