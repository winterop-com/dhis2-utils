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
    from .event_query_criteria import EventQueryCriteria
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class EventFilter(_BaseModel):
    """OpenAPI schema `EventFilter`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayName: str | None = None
    eventQueryCriteria: EventQueryCriteria | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    program: str | None = None
    programStage: str | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
