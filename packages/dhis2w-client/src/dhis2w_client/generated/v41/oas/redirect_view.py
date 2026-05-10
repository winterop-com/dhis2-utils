"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class RedirectView(_BaseModel):
    """OpenAPI schema `RedirectView`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    applicationContext: Any | None = None
    attributesMap: dict[str, dict[str, Any]] | None = None
    beanName: str | None = None
    contentType: str | None = None
    exposePathVariables: bool | None = None
    hosts: list[str] | None = None
    propagateQueryProperties: bool | None = None
    redirectView: bool | None = None
    requestContextAttribute: str | None = None
    staticAttributes: dict[str, dict[str, Any]] | None = None
    url: str | None = None
