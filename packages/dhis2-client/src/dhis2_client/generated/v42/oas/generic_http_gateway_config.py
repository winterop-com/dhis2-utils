"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import ContentType

if TYPE_CHECKING:
    from .generic_gateway_parameter import GenericGatewayParameter


class GenericHttpGatewayConfig(_BaseModel):
    """OpenAPI schema `GenericHttpGatewayConfig`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    configurationTemplate: str | None = None
    contentType: ContentType | None = None
    id: str | None = None
    isDefault: bool | None = None
    maxSmsLength: str | None = None
    name: str | None = None
    parameters: list[GenericGatewayParameter] | None = None
    password: str | None = None
    sendUrlParameters: bool | None = None
    uid: str | None = None
    urlTemplate: str | None = None
    useGet: bool | None = None
    username: str | None = None
