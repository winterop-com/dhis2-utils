"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class UserInviteParams(_BaseModel):
    """OpenAPI schema `UserInviteParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    email: str | None = None
    firstName: str | None = None
    g_recaptcha_response: str | None = _Field(default=None, alias="g-recaptcha-response")
    password: str | None = None
    surname: str | None = None
    token: str | None = None
    username: str | None = None
