"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .property import Property


class Node(_BaseModel):
    """OpenAPI schema `Node`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    children: list[Node] | None = None
    collection: bool | None = None
    comment: str | None = None
    complex: bool | None = None
    metadata: bool | None = None
    name: str | None = None
    namespace: str | None = None
    order: int | None = None
    parent: Node | None = None
    property: Property | None = None
    simple: bool | None = None
    type: str | None = None
    unorderedChildren: list[Node] | None = None
