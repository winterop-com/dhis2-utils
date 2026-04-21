"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .app_shortcut import AppShortcut


class WebModule(_BaseModel):
    """OpenAPI schema `WebModule`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    defaultAction: str | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayName: str | None = None
    icon: str | None = None
    name: str | None = None
    namespace: str | None = None
    shortcuts: list[AppShortcut] | None = None
    version: str | None = None
