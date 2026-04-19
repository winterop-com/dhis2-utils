"""Generated Attribute model for DHIS2 v40. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import ValueType
from .attribute_value import AttributeValue


class Attribute(BaseModel):
    """Generated model for DHIS2 `Attribute`.

    DHIS2 Attribute - persisted metadata (generated from /api/schemas at DHIS2 v40).


    API endpoint: /api/attributes.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access: Any | None = Field(default=None, description="Reference to Access. Read-only (inverse side).")

    attributeValues: list[AttributeValue] | None = Field(
        default=None, description="Collection of AttributeValue. Read-only (inverse side)."
    )

    categoryAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    categoryOptionAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    categoryOptionComboAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    categoryOptionGroupAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    categoryOptionGroupSetAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    code: str | None = Field(default=None, description="Unique. Length/value max=50.")

    constantAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    dataElementAttribute: bool | None = None

    dataElementGroupAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    dataElementGroupSetAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    dataSetAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    description: str | None = Field(default=None, description="Length/value min=1, max=2147483647.")

    displayDescription: str | None = Field(default=None, description="Read-only.")

    displayFormName: str | None = Field(default=None, description="Read-only.")

    displayName: str | None = Field(default=None, description="Read-only.")

    displayShortName: str | None = Field(default=None, description="Read-only.")

    documentAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    eventChartAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    eventReportAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    externalAccess: bool | None = None

    favorite: bool | None = Field(default=None, description="Read-only.")

    favorites: list[Any] | None = Field(default=None, description="Collection of String. Read-only (inverse side).")

    formName: str | None = Field(default=None, description="Length/value max=2147483647.")

    href: str | None = None

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    indicatorAttribute: bool | None = None

    indicatorGroupAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    lastUpdated: datetime | None = None

    lastUpdatedBy: Reference | None = Field(default=None, description="Reference to User.")

    legendSetAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    mandatory: bool | None = None

    mapAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    name: str | None = Field(default=None, description="Unique. Length/value min=1, max=230.")

    objectTypes: list[str] | None = Field(
        default=None, description="Collection of String. Read-only. Length/value max=255."
    )

    optionAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    optionSet: Reference | None = Field(default=None, description="Reference to OptionSet.")

    optionSetAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    organisationUnitAttribute: bool | None = None

    organisationUnitGroupAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    organisationUnitGroupSetAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    programAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    programIndicatorAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    programStageAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    publicAccess: str | None = Field(default=None, description="Length/value min=8, max=8.")

    relationshipTypeAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    sectionAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    sharing: Any | None = Field(default=None, description="Reference to Sharing. Length/value max=255.")

    shortName: str | None = Field(default=None, description="Length/value min=1, max=50.")

    sortOrder: int | None = Field(default=None, description="Length/value max=2147483647.")

    sqlViewAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    trackedEntityAttributeAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    trackedEntityTypeAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    translations: list[Any] | None = Field(default=None, description="Collection of Translation. Length/value max=255.")

    unique: bool | None = None

    user: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")

    userAccess: list[Any] | None = Field(
        default=None, description="Collection of UserAccess. Read-only (inverse side)."
    )

    userAttribute: bool | None = None

    userGroupAccess: list[Any] | None = Field(
        default=None, description="Collection of UserGroupAccess. Read-only (inverse side)."
    )

    userGroupAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    validationRuleAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    validationRuleGroupAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")

    valueType: ValueType | None = None

    visualizationAttribute: str | None = Field(default=None, description="Length/value max=2147483647.")
