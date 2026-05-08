"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .datastore_namespace import DatastoreNamespace


class AppDhis(_BaseModel):
    """OpenAPI schema `AppDhis`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    additionalNamespaces: list[DatastoreNamespace] | None = None
    href: str | None = None
    namespace: str | None = None
