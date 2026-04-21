"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class SoftwareUpdateResponse(_BaseModel):
    """OpenAPI schema `SoftwareUpdateResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    responseType: str | None = None
    versionMetadata: dict[str, dict[str, str]] | None = _Field(
        default=None, description="keys are class java.lang.Object"
    )
