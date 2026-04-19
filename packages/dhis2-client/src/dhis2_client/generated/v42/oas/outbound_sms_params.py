"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import OutboundSmsStatus

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class OutboundSmsParamsCreatedBy(_BaseModel):
    """OpenAPI schema `OutboundSmsParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OutboundSmsParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `OutboundSmsParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OutboundSmsParams(_BaseModel):
    """OpenAPI schema `OutboundSmsParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OutboundSmsParamsCreatedBy | None = None
    date: datetime | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OutboundSmsParamsLastUpdatedBy | None = None
    message: str | None = None
    name: str | None = None
    recipients: list[str] | None = None
    sender: str | None = None
    sharing: Sharing | None = None
    status: OutboundSmsStatus
    subject: str | None = None
    translations: list[Translation] | None = None
