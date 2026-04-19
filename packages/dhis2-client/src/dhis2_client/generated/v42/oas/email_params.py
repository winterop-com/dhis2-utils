"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .user_params import UserParams


class EmailParamsRecipients(_BaseModel):
    """OpenAPI schema `EmailParamsRecipients`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EmailParams(_BaseModel):
    """OpenAPI schema `EmailParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    recipients: list[EmailParamsRecipients] | None = None
    sender: UserParams | None = None
    subject: str | None = None
    text: str | None = None
