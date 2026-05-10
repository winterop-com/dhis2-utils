"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class EmailRecipients(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class EmailSender(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Email(_BaseModel):
    """OpenAPI schema `Email`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    recipients: list[EmailRecipients] | None = None
    sender: EmailSender | None = _Field(default=None, description="A UID reference to a User  ")
    subject: str | None = None
    text: str | None = None
