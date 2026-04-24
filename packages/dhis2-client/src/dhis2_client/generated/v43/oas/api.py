"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class Api(_BaseModel):
    """OpenAPI schema `Api`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    accessToken: str | None = None
    password: str | None = None
    url: str | None = None
    username: str | None = None
