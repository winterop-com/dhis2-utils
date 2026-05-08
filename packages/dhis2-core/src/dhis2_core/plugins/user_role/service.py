"""Service layer for the `user-role` plugin — role membership + authorities.

Authorities aren't granted on the User directly; they're granted by adding a
user to a role that carries the authority. This service wraps the canonical
paths: `/api/userRoles` for CRUD, `/api/userRoles/{rid}/users/{uid}` for
single-user role assignment.
"""

from __future__ import annotations

from typing import cast

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.oas import UserRole

from dhis2_core.client_context import open_client
from dhis2_core.profile import Profile


async def list_user_roles(
    profile: Profile,
    *,
    fields: str | None = None,
    filters: list[str] | None = None,
    order: list[str] | None = None,
    page: int | None = None,
    page_size: int | None = None,
    paging: bool | None = None,
) -> list[UserRole]:
    """List user roles (forwards metadata query knobs)."""
    async with open_client(profile) as client:
        roles = await client.resources.user_roles.list(
            fields=fields,
            filters=filters,
            order=order,
            page=page,
            page_size=page_size,
            paging=paging,
        )
    return cast(list[UserRole], roles)


async def get_user_role(profile: Profile, uid: str, *, fields: str | None = None) -> UserRole:
    """Fetch one user role by UID."""
    async with open_client(profile) as client:
        role = await client.resources.user_roles.get(uid, fields=fields)
    return cast(UserRole, role)


async def list_authorities(profile: Profile, uid: str) -> list[str]:
    """Return the sorted list of authorities carried by one user role.

    DHIS2's full authority inventory is at `/api/authorities`, but for a given
    role the interesting slice is the role's own `authorities[]`. `UserRole`
    models that directly — this helper just unwraps + sorts it.
    """
    role = await get_user_role(profile, uid, fields="id,name,authorities")
    return sorted(role.authorities or [])


async def add_user(profile: Profile, role_uid: str, user_uid: str) -> WebMessageResponse:
    """Grant a user a role via `POST /api/userRoles/{role}/users/{user}`."""
    async with open_client(profile) as client:
        return await client.post(
            f"/api/userRoles/{role_uid}/users/{user_uid}",
            {},
            model=WebMessageResponse,
        )


async def remove_user(profile: Profile, role_uid: str, user_uid: str) -> WebMessageResponse:
    """Revoke a user's role via `DELETE /api/userRoles/{role}/users/{user}`."""
    async with open_client(profile) as client:
        return await client.delete(
            f"/api/userRoles/{role_uid}/users/{user_uid}",
            model=WebMessageResponse,
        )
