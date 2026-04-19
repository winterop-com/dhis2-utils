"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import Include, Transform


class GistPreferences(_BaseModel):
    """OpenAPI schema `GistPreferences`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    included: Include | None = None
    transformation: Transform | None = None
