"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .expression import Expression
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ValidationRuleCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleLegendSet(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleLegendSets(_BaseModel):
    """A UID reference to a LegendSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleNotificationTemplates(_BaseModel):
    """A UID reference to a ValidationNotificationTemplate  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRuleValidationRuleGroups(_BaseModel):
    """A UID reference to a ValidationRuleGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationRule(_BaseModel):
    """OpenAPI schema `ValidationRule`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: str | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ValidationRuleCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayInstruction: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    importance: str | None = None
    instruction: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ValidationRuleLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    leftSide: Expression | None = None
    legendSet: ValidationRuleLegendSet | None = _Field(default=None, description="A UID reference to a LegendSet  ")
    legendSets: list[ValidationRuleLegendSets] | None = None
    name: str | None = None
    notificationTemplates: list[ValidationRuleNotificationTemplates] | None = None
    operator: str | None = None
    organisationUnitLevels: list[int] | None = None
    periodType: str | None = None
    queryMods: QueryModifiers | None = None
    rightSide: Expression | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipFormValidation: bool | None = None
    translations: list[Translation] | None = None
    user: ValidationRuleUser | None = _Field(default=None, description="A UID reference to a User  ")
    validationRuleGroups: list[ValidationRuleValidationRuleGroups] | None = None
