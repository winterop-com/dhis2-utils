"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class BulkSmsGatewayConfig(_BaseModel):
    """OpenAPI schema `BulkSmsGatewayConfig`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None
    isDefault: bool | None = None
    maxSmsLength: str | None = None
    name: str | None = None
    password: str | None = None
    sendUrlParameters: bool | None = None
    uid: str | None = None
    urlTemplate: str | None = None
    username: str | None = None
