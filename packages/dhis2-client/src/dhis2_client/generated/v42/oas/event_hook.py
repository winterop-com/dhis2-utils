"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .console_target import ConsoleTarget
    from .jms_target import JmsTarget
    from .kafka_target import KafkaTarget
    from .sharing import Sharing
    from .source import Source
    from .translation import Translation
    from .user_dto import UserDto
    from .webhook_target import WebhookTarget


class EventHook(_BaseModel):
    """OpenAPI schema `EventHook`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    description: str | None = None
    disabled: bool
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    sharing: Sharing | None = None
    source: Source
    targets: list[WebhookTarget | ConsoleTarget | JmsTarget | KafkaTarget]
    translations: list[Translation] | None = None
