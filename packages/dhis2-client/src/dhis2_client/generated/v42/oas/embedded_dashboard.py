"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import EmbeddedProvider

if TYPE_CHECKING:
    from .embedded_options import EmbeddedOptions
    from .embedded_security import EmbeddedSecurity


class EmbeddedDashboard(_BaseModel):
    """OpenAPI schema `EmbeddedDashboard`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None
    options: EmbeddedOptions | None = None
    provider: EmbeddedProvider | None = None
    security: EmbeddedSecurity | None = None
