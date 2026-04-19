"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AnalyticsFavoriteType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .interpretation_comment import InterpretationComment
    from .mention import Mention
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class Interpretation(_BaseModel):
    """OpenAPI schema `Interpretation`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    comments: list[InterpretationComment] | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataSet: BaseIdentifiableObject | None = None
    displayName: str | None = None
    eventChart: BaseIdentifiableObject | None = None
    eventReport: BaseIdentifiableObject | None = None
    eventVisualization: BaseIdentifiableObject | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    likedBy: list[UserDto] | None = None
    likes: BaseIdentifiableObject
    map: BaseIdentifiableObject | None = None
    mentions: list[Mention] | None = None
    organisationUnit: BaseIdentifiableObject | None = None
    period: BaseIdentifiableObject | None = None
    sharing: Sharing | None = None
    text: str | None = None
    translations: list[Translation] | None = None
    type: AnalyticsFavoriteType
    visualization: BaseIdentifiableObject | None = None
