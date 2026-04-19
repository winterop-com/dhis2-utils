"""Generated Attribute model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import ValueType


class Attribute(BaseModel):
    """Generated model for DHIS2 `Attribute`.

    DHIS2 Attribute - persisted metadata (generated from /api/schemas at DHIS2 v42).


    API endpoint: /api/attributes.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: Any | None = Field(
        default=None, description="Reference to AttributeValues. Read-only (inverse side)."
    )

    categoryAttribute: bool | None = None

    categoryOptionAttribute: bool | None = None

    categoryOptionComboAttribute: bool | None = None

    categoryOptionGroupAttribute: bool | None = None

    categoryOptionGroupSetAttribute: bool | None = None

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    constantAttribute: bool | None = None

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    dataElementAttribute: bool | None = None

    dataElementGroupAttribute: bool | None = None

    dataElementGroupSetAttribute: bool | None = None

    dataSetAttribute: bool | None = None

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    documentAttribute: bool | None = None

    eventChartAttribute: bool | None = None

    eventReportAttribute: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    indicatorAttribute: bool | None = None

    indicatorGroupAttribute: bool | None = None

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendSetAttribute: bool | None = None

    mandatory: bool | None = None

    mapAttribute: bool | None = None

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    objectTypes: list[Any] | None = Field(
        default=None, description="Collection of String. Read-only. Length/value max=255."
    )

    optionAttribute: bool | None = None

    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet.")

    optionSetAttribute: bool | None = None

    organisationUnitAttribute: bool | None = None

    organisationUnitGroupAttribute: bool | None = None

    organisationUnitGroupSetAttribute: bool | None = None

    programAttribute: bool | None = None

    programIndicatorAttribute: bool | None = None

    programStageAttribute: bool | None = None

    relationshipTypeAttribute: bool | None = None

    sectionAttribute: bool | None = None

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=50.")

    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")

    sqlViewAttribute: bool | None = None

    trackedEntityAttributeAttribute: bool | None = None

    trackedEntityTypeAttribute: bool | None = None

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    unique: bool | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAttribute: bool | None = None

    userGroupAttribute: bool | None = None

    validationRuleAttribute: bool | None = None

    validationRuleGroupAttribute: bool | None = None

    valueType: ValueType | None = None

    visualizationAttribute: bool | None = None
