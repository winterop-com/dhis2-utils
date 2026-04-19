"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import SmsMessageEncoding, SmsMessageStatus

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class IncomingSmsParamsCreatedBy(_BaseModel):
    """OpenAPI schema `IncomingSmsParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class IncomingSmsParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `IncomingSmsParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class IncomingSmsParams(_BaseModel):
    """OpenAPI schema `IncomingSmsParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: IncomingSmsParamsCreatedBy | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    gatewayid: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: IncomingSmsParamsLastUpdatedBy | None = None
    name: str | None = None
    originator: str | None = None
    receiveddate: datetime | None = None
    sentdate: datetime | None = None
    sharing: Sharing | None = None
    smsencoding: SmsMessageEncoding | None = None
    smsstatus: SmsMessageStatus | None = None
    text: str | None = None
    translations: list[Translation] | None = None
