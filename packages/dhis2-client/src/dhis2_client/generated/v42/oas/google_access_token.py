"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class GoogleAccessToken(_BaseModel):
    """OpenAPI schema `GoogleAccessToken`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access_token: str | None = None
    client_id: str | None = None
    expires_in: int | None = None
