"""FastMCP tool registration for the `user-role` plugin."""

from __future__ import annotations

from typing import Any

from dhis2_client.envelopes import WebMessageResponse
from dhis2_client.generated.v42.oas import UserRole

from dhis2_core.plugins.user_role import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register user-role tools — read + membership edits."""

    @mcp.tool()
    async def user_role_list(
        fields: str = "id,name,displayName,authorities,users",
        filters: list[str] | None = None,
        order: list[str] | None = None,
        page_size: int | None = None,
        paging: bool | None = None,
        profile: str | None = None,
    ) -> list[UserRole]:
        """List DHIS2 user roles with the metadata query surface."""
        return await service.list_user_roles(
            resolve_profile(profile),
            fields=fields,
            filters=filters,
            order=order,
            page_size=page_size,
            paging=paging,
        )

    @mcp.tool()
    async def user_role_get(uid: str, fields: str | None = None, profile: str | None = None) -> UserRole:
        """Fetch one user role by UID."""
        return await service.get_user_role(resolve_profile(profile), uid, fields=fields)

    @mcp.tool()
    async def user_role_authority_list(uid: str, profile: str | None = None) -> list[str]:
        """Return the sorted authorities carried by one role."""
        return await service.list_authorities(resolve_profile(profile), uid)

    @mcp.tool()
    async def user_role_add_user(
        role_uid: str,
        user_uid: str,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Grant a user a role."""
        return await service.add_user(resolve_profile(profile), role_uid, user_uid)

    @mcp.tool()
    async def user_role_remove_user(
        role_uid: str,
        user_uid: str,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Revoke a user's role."""
        return await service.remove_user(resolve_profile(profile), role_uid, user_uid)
