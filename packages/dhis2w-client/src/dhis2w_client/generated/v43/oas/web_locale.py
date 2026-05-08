"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class WebLocale(_BaseModel):
    """OpenAPI schema `WebLocale`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    displayName: str | None = None
    languageTag: str | None = None
    locale: str | None = None
    name: str | None = None
