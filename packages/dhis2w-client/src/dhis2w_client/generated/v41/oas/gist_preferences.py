"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class GistPreferences(_BaseModel):
    """OpenAPI schema `GistPreferences`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    included: Literal["FALSE", "TRUE", "AUTO"] | None = None
    transformation: (
        Literal[
            "AUTO",
            "NONE",
            "IS_EMPTY",
            "IS_NOT_EMPTY",
            "SIZE",
            "MEMBER",
            "NOT_MEMBER",
            "IDS",
            "ID_OBJECTS",
            "PLUCK",
            "FROM",
        ]
        | None
    ) = None
