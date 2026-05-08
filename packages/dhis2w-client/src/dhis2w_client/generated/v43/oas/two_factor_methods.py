"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class TwoFactorMethods(_BaseModel):
    """OpenAPI schema `TwoFactorMethods`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    email2faEnabled: bool | None = None
    totp2faEnabled: bool | None = None
