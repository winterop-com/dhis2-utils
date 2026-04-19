"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class JmsTarget(_BaseModel):
    """OpenAPI schema `JmsTarget`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    address: str | None = None
    brokerUrl: str | None = None
    clientId: str | None = None
    groupId: str | None = None
    password: str | None = None
    type: str | None = None
    useQueue: bool | None = None
    username: str | None = None
