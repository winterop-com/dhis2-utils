"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .base_identifiable_object import BaseIdentifiableObject
    from .file_resource import FileResource


class Message(_BaseModel):
    """OpenAPI schema `Message`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attachments: list[FileResource] | None = None
    href: str | None = None
    internal: bool | None = None
    lastUpdated: datetime | None = None
    metaData: str | None = None
    sender: BaseIdentifiableObject | None = None
    text: str | None = None
