"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .components_object import ComponentsObject
    from .info_object import InfoObject
    from .server_object import ServerObject
    from .tag_object import TagObject


class OpenApiObject(_BaseModel):
    """OpenAPI schema `OpenApiObject`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    components: ComponentsObject | None = None
    info: InfoObject | None = None
    openapi: str | None = None
    paths: dict[str, Any] | None = None
    servers: list[ServerObject] | None = None
    tags: list[TagObject] | None = None
