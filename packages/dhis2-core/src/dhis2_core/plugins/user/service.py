"""Service layer for the `user` plugin — read + administer DHIS2 users.

Reads go through the generated `/api/users` resource accessor so every list /
get benefits from the typed metadata query surface (filters, order, paging,
fields selector, rootJunction, translate/locale). Mutations hit the dedicated
admin endpoints `/api/users/invite`, `/api/users/{id}/invite`, and
`/api/users/{id}/reset` that the generated CRUD accessor doesn't cover.
"""

from __future__ import annotations

from typing import Any, cast

from dhis2_client import is_valid_uid
from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.oas import User
from pydantic import BaseModel, ConfigDict, Field

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


class UserInvite(BaseModel):
    """Typed payload for `POST /api/users/invite` — create + email-invite a user.

    DHIS2 expects a User object with at minimum `username`, `email`,
    `firstName`, `surname`, plus enough role/OU linkage for the new user to
    land somewhere on sign-in. `userRoles` is a list of UID references
    (`[{"id": "uid"}]`); same for `organisationUnits`. DHIS2 dispatches the
    invitation email via its configured mailer.
    """

    model_config = ConfigDict(extra="allow")

    username: str | None = None
    email: str
    firstName: str
    surname: str
    userRoles: list[dict[str, str]] = Field(default_factory=list)
    organisationUnits: list[dict[str, str]] = Field(default_factory=list)


async def list_users(
    profile: Profile,
    *,
    fields: str | None = None,
    filters: list[str] | None = None,
    root_junction: str | None = None,
    order: list[str] | None = None,
    page: int | None = None,
    page_size: int | None = None,
    paging: bool | None = None,
) -> list[User]:
    """List users via GET /api/users (forwards every metadata query knob)."""
    async with open_client(profile) as client:
        users = await client.resources.users.list(
            fields=fields,
            filters=filters,
            root_junction=root_junction,
            order=order,
            page=page,
            page_size=page_size,
            paging=paging,
        )
    return cast(list[User], users)


async def get_user(profile: Profile, uid_or_username: str, *, fields: str | None = None) -> User:
    """Fetch one user by UID or username.

    DHIS2's `/api/users/{id}` only accepts a UID; a username path returns 405.
    When the input doesn't match the UID pattern, resolve via
    `/api/users?filter=username:eq:...` first, then fetch by the resolved UID.
    """
    async with open_client(profile) as client:
        if is_valid_uid(uid_or_username):
            user = await client.resources.users.get(uid_or_username, fields=fields)
            return cast(User, user)
        hits = await client.resources.users.list(
            filters=[f"username:eq:{uid_or_username}"],
            fields="id",
            page_size=1,
        )
        if not hits:
            raise UserNotFoundError(f"no user with username {uid_or_username!r}")
        uid = str(hits[0].id)
        user = await client.resources.users.get(uid, fields=fields)
    return cast(User, user)


class UserNotFoundError(LookupError):
    """Raised when a username→UID resolution returns no rows."""


async def invite_user(profile: Profile, invite: UserInvite) -> WebMessageResponse:
    """Create + email-invite a user via POST /api/users/invite.

    DHIS2 returns a WebMessage envelope whose `response.uid` carries the new
    user's UID. Caller drives next steps (role / OU assignment) against that.
    """
    payload = invite.model_dump(by_alias=True, exclude_none=True, mode="json")
    async with open_client(profile) as client:
        raw = await client.post_raw("/api/users/invite", payload)
    return WebMessageResponse.model_validate(raw)


async def reinvite_user(profile: Profile, uid: str) -> WebMessageResponse:
    """Re-send the invitation email for a user who hasn't accepted yet.

    Hits POST /api/users/{uid}/invite. DHIS2 rejects with 400 if the user has
    already completed registration.
    """
    async with open_client(profile) as client:
        raw = await client.post_raw(f"/api/users/{uid}/invite", {})
    return WebMessageResponse.model_validate(raw)


async def reset_password(profile: Profile, uid: str) -> WebMessageResponse:
    """Trigger DHIS2's password-reset email for a user.

    Hits POST /api/users/{uid}/reset — DHIS2 mints a reset token and mails a
    link to the user's verified email address. No password ever flows through
    the client.
    """
    async with open_client(profile) as client:
        raw = await client.post_raw(f"/api/users/{uid}/reset", {})
    return WebMessageResponse.model_validate(raw)


async def current_user(profile: Profile) -> dict[str, Any]:
    """Fetch `/api/me` — the authenticated user's profile.

    Separate from `get_user` because `/api/me` isn't an `/api/users/{id}` view;
    it returns a richer payload (authorities, settings, programs, etc.).
    """
    async with open_client(profile) as client:
        me = await client.system.me()
    return me.model_dump(by_alias=True, exclude_none=True, mode="json")
