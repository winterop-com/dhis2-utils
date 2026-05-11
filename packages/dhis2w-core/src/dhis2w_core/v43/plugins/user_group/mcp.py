"""FastMCP tool registration for the `user-group` plugin."""

from __future__ import annotations

from typing import Any

from dhis2w_client.generated.v43.oas import UserGroup
from dhis2w_client.v43 import SharingObject
from dhis2w_client.v43.envelopes import WebMessageResponse

from dhis2w_core.profile import resolve_profile
from dhis2w_core.v43.plugins.user_group import service


def register(mcp: Any) -> None:
    """Register user-group tools — read + membership + sharing."""

    @mcp.tool()
    async def user_group_list(
        fields: str = "id,name,displayName,users",
        filters: list[str] | None = None,
        order: list[str] | None = None,
        page_size: int | None = None,
        paging: bool | None = None,
        profile: str | None = None,
    ) -> list[UserGroup]:
        """List DHIS2 user groups with the metadata query surface."""
        return await service.list_user_groups(
            resolve_profile(profile),
            fields=fields,
            filters=filters,
            order=order,
            page_size=page_size,
            paging=paging,
        )

    @mcp.tool()
    async def user_group_get(uid: str, fields: str | None = None, profile: str | None = None) -> UserGroup:
        """Fetch one user group by UID."""
        return await service.get_user_group(resolve_profile(profile), uid, fields=fields)

    @mcp.tool()
    async def user_group_add_member(
        group_uid: str,
        user_uid: str,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Add a user to a user group."""
        return await service.add_member(resolve_profile(profile), group_uid, user_uid)

    @mcp.tool()
    async def user_group_remove_member(
        group_uid: str,
        user_uid: str,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Remove a user from a user group."""
        return await service.remove_member(resolve_profile(profile), group_uid, user_uid)

    @mcp.tool()
    async def user_group_sharing_get(uid: str, profile: str | None = None) -> SharingObject:
        """Return the current sharing block for one user group."""
        return await service.get_group_sharing(resolve_profile(profile), uid)
