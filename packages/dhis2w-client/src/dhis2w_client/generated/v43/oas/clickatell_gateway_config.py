"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ClickatellGatewayConfig(_BaseModel):
    """OpenAPI schema `ClickatellGatewayConfig`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    authToken: str | None = None
    id: str | None = None
    isDefault: bool | None = None
    maxSmsLength: str | None = None
    name: str | None = None
    password: str | None = None
    sendUrlParameters: bool | None = None
    uid: str | None = None
    urlTemplate: str | None = None
    username: str | None = None
