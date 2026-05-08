"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class ApiQueryParamsAuthScheme(_BaseModel):
    """OpenAPI schema `ApiQueryParamsAuthScheme`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    queryParams: dict[str, str] | None = None
    type: Literal["api-query-params"] = "api-query-params"
