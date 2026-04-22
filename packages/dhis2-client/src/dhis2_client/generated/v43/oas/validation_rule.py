"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import AggregationType, DimensionItemType, Importance, Operator

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .expression import Expression
    from .identifiable_object import IdentifiableObject
    from .legend_set import LegendSet
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class ValidationRule(_BaseModel):
    """OpenAPI schema `ValidationRule`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregateExportAttributeOptionCombo: str | None = None
    aggregateExportCategoryOptionCombo: str | None = None
    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    description: str | None = None
    dimensionItem: str | None = None
    dimensionItemType: DimensionItemType | None = None
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
    importance: Importance | None = None
    instruction: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    leftSide: Expression | None = None
    legendSet: LegendSet | None = None
    legendSets: list[LegendSet] | None = None
    name: str | None = None
    notificationTemplates: list[IdentifiableObject] | None = None
    operator: Operator | None = None
    organisationUnitLevels: list[int] | None = None
    periodType: str | None = None
    queryMods: QueryModifiers | None = None
    rightSide: Expression | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipFormValidation: bool | None = None
    translations: list[Translation] | None = None
    validationRuleGroups: list[BaseIdentifiableObject] | None = None
