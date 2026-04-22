"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .console_target import ConsoleTarget
    from .jms_target import JmsTarget
    from .kafka_target import KafkaTarget
    from .sharing import Sharing
    from .source import Source
    from .translation import Translation
    from .webhook_target import WebhookTarget


class EventHookParamsCreatedBy(_BaseModel):
    """OpenAPI schema `EventHookParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventHookParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `EventHookParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EventHookParams(_BaseModel):
    """OpenAPI schema `EventHookParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: EventHookParamsCreatedBy | None = None
    description: str | None = None
    disabled: bool | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: EventHookParamsLastUpdatedBy | None = None
    name: str | None = None
    sharing: Sharing | None = None
    source: Source | None = None
    targets: list[WebhookTarget | ConsoleTarget | JmsTarget | KafkaTarget] | None = None
    translations: list[Translation] | None = None
