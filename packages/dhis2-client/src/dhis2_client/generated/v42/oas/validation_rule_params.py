"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DimensionItemType, Importance, Operator

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .expression import Expression
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class ValidationRuleParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ValidationRuleParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ValidationRuleParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ValidationRuleParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ValidationRuleParamsLegendSet(_BaseModel):
    """OpenAPI schema `ValidationRuleParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ValidationRuleParamsLegendSets(_BaseModel):
    """OpenAPI schema `ValidationRuleParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ValidationRuleParamsNotificationTemplates(_BaseModel):
    """OpenAPI schema `ValidationRuleParamsNotificationTemplates`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ValidationRuleParamsValidationRuleGroups(_BaseModel):
    """OpenAPI schema `ValidationRuleParamsValidationRuleGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class ValidationRuleParams(_BaseModel):
    """OpenAPI schema `ValidationRuleParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: AggregationType
    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ValidationRuleParamsCreatedBy | None = None
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: DimensionItemType
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayInstruction: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    id: str | None = None
    importance: Importance
    instruction: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ValidationRuleParamsLastUpdatedBy | None = None
    leftSide: Expression | None = None
    legendSet: ValidationRuleParamsLegendSet | None = None
    legendSets: list[ValidationRuleParamsLegendSets] | None = None
    name: str | None = None
    notificationTemplates: list[ValidationRuleParamsNotificationTemplates] | None = None
    operator: Operator
    organisationUnitLevels: list[int] | None = None
    periodType: str | None = None
    queryMods: QueryModifiers | None = None
    rightSide: Expression | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipFormValidation: bool | None = None
    translations: list[Translation] | None = None
    validationRuleGroups: list[ValidationRuleParamsValidationRuleGroups] | None = None
