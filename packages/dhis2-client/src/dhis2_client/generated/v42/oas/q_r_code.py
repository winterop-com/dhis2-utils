"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class QRCode(_BaseModel):
    """OpenAPI schema `QRCode`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    base32Secret: str | None = None
    base64QRImage: str | None = None
