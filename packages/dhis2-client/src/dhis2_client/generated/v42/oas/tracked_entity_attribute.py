"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, ValueType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .legend_set import LegendSet
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class TrackedEntityAttribute(_BaseModel):
    """OpenAPI schema `TrackedEntityAttribute`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    confidential: bool | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayInListNoProgram: bool | None = None
    displayName: str | None = None
    displayOnVisitSchedule: bool | None = None
    displayShortName: str | None = None
    expression: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldMask: str | None = None
    formName: str | None = None
    generated: bool | None = None
    href: str | None = None
    id: str | None = None
    inherit: bool | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legendSet: LegendSet | None = None
    legendSets: list[LegendSet] | None = None
    name: str | None = None
    optionSet: BaseIdentifiableObject | None = None
    optionSetValue: bool | None = None
    orgunitScope: bool | None = None
    pattern: str | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipSynchronization: bool | None = None
    sortOrderInListNoProgram: int | None = None
    sortOrderInVisitSchedule: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    unique: bool | None = None
    valueType: ValueType | None = None
