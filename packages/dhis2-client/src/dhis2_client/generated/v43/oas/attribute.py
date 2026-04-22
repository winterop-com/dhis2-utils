"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ValueType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .option_set import OptionSet
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class Attribute(_BaseModel):
    """OpenAPI schema `Attribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryAttribute: bool | None = None
    categoryOptionAttribute: bool | None = None
    categoryOptionComboAttribute: bool | None = None
    categoryOptionGroupAttribute: bool | None = None
    categoryOptionGroupSetAttribute: bool | None = None
    code: str | None = None
    constantAttribute: bool | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
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
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    indicatorAttribute: bool | None = None
    indicatorGroupAttribute: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legendSetAttribute: bool | None = None
    mandatory: bool | None = None
    mapAttribute: bool | None = None
    name: str | None = None
    objectTypes: list[str] | None = None
    optionAttribute: bool | None = None
    optionSet: OptionSet | None = None
    optionSetAttribute: bool | None = None
    organisationUnitAttribute: bool | None = None
    organisationUnitGroupAttribute: bool | None = None
    organisationUnitGroupSetAttribute: bool | None = None
    programAttribute: bool | None = None
    programIndicatorAttribute: bool | None = None
    programStageAttribute: bool | None = None
    relationshipTypeAttribute: bool | None = None
    sectionAttribute: bool | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    sortOrder: int | None = None
    sqlViewAttribute: bool | None = None
    trackedEntityAttributeAttribute: bool | None = None
    trackedEntityTypeAttribute: bool | None = None
    translations: list[Translation] | None = None
    unique: bool | None = None
    userAttribute: bool | None = None
    userGroupAttribute: bool | None = None
    validationRuleAttribute: bool | None = None
    validationRuleGroupAttribute: bool | None = None
    valueType: ValueType | None = None
    visualizationAttribute: bool | None = None
