"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import AggregationType, QueryOperator, ValueType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .identifiable_object import IdentifiableObject
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
    blockedSearchOperators: list[QueryOperator] | None = _Field(
        default=None,
        description="Set of `QueryOperator`s that cannot be used with the current Tracked Entity Attribute.",
    )
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
    minCharactersToSearch: int | None = _Field(
        default=None,
        description="Minimum number of characters required to search within the current Tracked Entity Attribute. A value of 0 means no minimum.",
    )
    name: str | None = None
    optionSet: IdentifiableObject | None = None
    optionSetValue: bool | None = None
    orgunitScope: bool | None = None
    pattern: str | None = None
    preferredSearchOperator: QueryOperator | None = _Field(
        default=None, description="Suggested `QueryOperator` to use for the current Tracked Entity Attribute."
    )
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipAnalytics: bool | None = _Field(
        default=None, description="Indicates whether this attribute should be excluded from analytics."
    )
    skipSynchronization: bool | None = None
    sortOrderInListNoProgram: int | None = None
    sortOrderInVisitSchedule: int | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    trigramIndexable: bool | None = None
    trigramIndexed: bool | None = None
    unique: bool | None = None
    valueType: ValueType | None = None
