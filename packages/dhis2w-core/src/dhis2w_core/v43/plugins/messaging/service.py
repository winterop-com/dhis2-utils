"""Service layer for the `messaging` plugin — thin orchestration over `client.messaging`."""

from __future__ import annotations

from collections.abc import Sequence

from dhis2w_client import MessageConversation, WebMessageResponse

from dhis2w_core.client_context import open_client
from dhis2w_core.profile import Profile


async def list_conversations(
    profile: Profile,
    *,
    filter: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> list[MessageConversation]:
    """List conversations the authenticated user is part of."""
    async with open_client(profile) as client:
        return await client.messaging.list_conversations(filter=filter, page=page, page_size=page_size)


async def get_conversation(profile: Profile, uid: str) -> MessageConversation:
    """Fetch one conversation with its full thread."""
    async with open_client(profile) as client:
        return await client.messaging.get_conversation(uid)


async def send(
    profile: Profile,
    *,
    subject: str,
    text: str,
    users: Sequence[str] | None = None,
    user_groups: Sequence[str] | None = None,
    organisation_units: Sequence[str] | None = None,
    attachments: Sequence[str] | None = None,
) -> MessageConversation:
    """Create a new conversation with an initial message; returns the typed conversation."""
    async with open_client(profile) as client:
        return await client.messaging.send(
            subject=subject,
            text=text,
            users=users,
            user_groups=user_groups,
            organisation_units=organisation_units,
            attachments=attachments,
        )


async def reply(profile: Profile, uid: str, *, text: str) -> WebMessageResponse:
    """Reply to an existing conversation.

    DHIS2 stores the plain-text body as the message on v42 — attachments +
    internal-note flag are only usable on the initial `send()`.
    """
    async with open_client(profile) as client:
        return await client.messaging.reply(uid, text=text)


async def mark_read(profile: Profile, uids: str | Sequence[str]) -> WebMessageResponse:
    """Flip one or many conversations to read."""
    async with open_client(profile) as client:
        return await client.messaging.mark_read(uids)


async def mark_unread(profile: Profile, uids: str | Sequence[str]) -> WebMessageResponse:
    """Flip one or many conversations to unread."""
    async with open_client(profile) as client:
        return await client.messaging.mark_unread(uids)


async def delete_conversation(profile: Profile, uid: str) -> None:
    """Delete a conversation (soft-deletes for the calling user only)."""
    async with open_client(profile) as client:
        await client.messaging.delete_conversation(uid)


async def set_priority(profile: Profile, uid: str, priority: str) -> None:
    """Set the ticket-workflow priority (`NONE` / `LOW` / `MEDIUM` / `HIGH`)."""
    async with open_client(profile) as client:
        await client.messaging.set_priority(uid, priority)  # type: ignore[arg-type]


async def set_status(profile: Profile, uid: str, status: str) -> None:
    """Set the ticket-workflow status (`NONE` / `OPEN` / `PENDING` / `INVALID` / `SOLVED`)."""
    async with open_client(profile) as client:
        await client.messaging.set_status(uid, status)  # type: ignore[arg-type]


async def assign(profile: Profile, uid: str, user_uid: str) -> None:
    """Assign a conversation to a user (ticket workflows)."""
    async with open_client(profile) as client:
        await client.messaging.assign(uid, user_uid)


async def unassign(profile: Profile, uid: str) -> None:
    """Remove the assignee from a conversation."""
    async with open_client(profile) as client:
        await client.messaging.unassign(uid)
