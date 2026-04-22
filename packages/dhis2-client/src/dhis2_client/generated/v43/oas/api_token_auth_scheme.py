"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class ApiTokenAuthScheme(_BaseModel):
    """OpenAPI schema `ApiTokenAuthScheme`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    token: str | None = None
    type: Literal["api-token"] = "api-token"
