"""FastMCP tool registration for the `messaging` plugin."""

from __future__ import annotations

from typing import Any

from dhis2w_client import MessageConversation, WebMessageResponse

from dhis2w_core.plugins.messaging import service
from dhis2w_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register messaging tools on the MCP server."""

    @mcp.tool()
    async def messaging_list(
        filter: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        profile: str | None = None,
    ) -> list[MessageConversation]:
        """List conversations the authenticated user is part of.

        `filter` accepts DHIS2's standard DSL (`read:eq:false` for unread
        only). `page` is 1-indexed; DHIS2 defaults `page_size` to 50.
        """
        return await service.list_conversations(
            resolve_profile(profile),
            filter=filter,
            page=page,
            page_size=page_size,
        )

    @mcp.tool()
    async def messaging_get(uid: str, profile: str | None = None) -> MessageConversation:
        """Fetch one conversation with its full message thread."""
        return await service.get_conversation(resolve_profile(profile), uid)

    @mcp.tool()
    async def messaging_send(
        subject: str,
        text: str,
        users: list[str] | None = None,
        user_groups: list[str] | None = None,
        organisation_units: list[str] | None = None,
        attachments: list[str] | None = None,
        profile: str | None = None,
    ) -> MessageConversation:
        """Create a new conversation with an initial message; returns the typed conversation.

        At least one recipient list (`users` / `user_groups` /
        `organisation_units`) must be non-empty. `attachments` is a list of
        fileResource UIDs previously uploaded with `domain=MESSAGE_ATTACHMENT`
        (see the `files` plugin). The `MessageConversation.id` is the new
        conversation UID (DHIS2 returns it on the Location header — see
        BUGS.md #17 — the accessor looks it up for you).
        """
        return await service.send(
            resolve_profile(profile),
            subject=subject,
            text=text,
            users=users,
            user_groups=user_groups,
            organisation_units=organisation_units,
            attachments=attachments,
        )

    @mcp.tool()
    async def messaging_reply(
        uid: str,
        text: str,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Reply to an existing conversation with a plain-text message.

        DHIS2's reply endpoint takes text/plain body on v42 — attachments
        + the internal-note flag only work on the initial `messaging_send`
        call.
        """
        return await service.reply(resolve_profile(profile), uid, text=text)

    @mcp.tool()
    async def messaging_mark_read(uids: list[str], profile: str | None = None) -> WebMessageResponse:
        """Mark one or more conversations as read."""
        return await service.mark_read(resolve_profile(profile), uids)

    @mcp.tool()
    async def messaging_mark_unread(uids: list[str], profile: str | None = None) -> WebMessageResponse:
        """Mark one or more conversations as unread."""
        return await service.mark_unread(resolve_profile(profile), uids)

    @mcp.tool()
    async def messaging_delete(uid: str, profile: str | None = None) -> dict[str, str]:
        """Delete a conversation (soft-delete for the calling user)."""
        await service.delete_conversation(resolve_profile(profile), uid)
        return {"status": "deleted", "uid": uid}

    @mcp.tool()
    async def messaging_set_priority(uid: str, priority: str, profile: str | None = None) -> dict[str, str]:
        """Set a conversation's ticket-workflow priority: NONE / LOW / MEDIUM / HIGH."""
        await service.set_priority(resolve_profile(profile), uid, priority.upper())
        return {"uid": uid, "priority": priority.upper()}

    @mcp.tool()
    async def messaging_set_status(uid: str, status: str, profile: str | None = None) -> dict[str, str]:
        """Set a conversation's ticket-workflow status: NONE / OPEN / PENDING / INVALID / SOLVED."""
        await service.set_status(resolve_profile(profile), uid, status.upper())
        return {"uid": uid, "status": status.upper()}

    @mcp.tool()
    async def messaging_assign(uid: str, user_uid: str, profile: str | None = None) -> dict[str, str]:
        """Assign a conversation to a user (ticket workflows)."""
        await service.assign(resolve_profile(profile), uid, user_uid)
        return {"uid": uid, "assignee": user_uid}

    @mcp.tool()
    async def messaging_unassign(uid: str, profile: str | None = None) -> dict[str, str]:
        """Remove the assignee from a conversation."""
        await service.unassign(resolve_profile(profile), uid)
        return {"uid": uid, "assignee": ""}
