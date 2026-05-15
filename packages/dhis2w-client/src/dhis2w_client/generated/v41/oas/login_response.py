"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class LoginResponse(_BaseModel):
    """OpenAPI schema `LoginResponse`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    loginStatus: (
        Literal[
            "SUCCESS",
            "ACCOUNT_DISABLED",
            "ACCOUNT_LOCKED",
            "ACCOUNT_EXPIRED",
            "PASSWORD_EXPIRED",
            "INCORRECT_TWO_FACTOR_CODE",
            "REQUIRES_TWO_FACTOR_ENROLMENT",
        ]
        | None
    ) = None
    redirectUrl: str | None = None
