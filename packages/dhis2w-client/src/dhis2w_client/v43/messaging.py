"""DHIS2 internal messaging — `/api/messageConversations`.

Natural pairing with the files plugin: a `MESSAGE_ATTACHMENT`-domain
fileResource uploaded via `client.files.upload_file_resource(...)` returns
a UID that references directly from a message. The same fileResource can
be read back via `client.files.download_file_resource(uid)` once the
conversation recipient has access.

Covers:

- Inbox reads (`list_conversations` / `get_conversation`)
- Conversation creation + reply (`send` / `reply`)
- Read-state toggle (`mark_read` / `mark_unread`) + delete
- Ticket-workflow fields (`set_priority` / `set_status` / `assign` /
  `unassign`). These work on PRIVATE conversations too — DHIS2 stores
  the fields regardless of `messageType`; they're most meaningful when
  `messageType=TICKET`.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel, ConfigDict

from dhis2w_client.generated.v43.oas import MessageConversation
from dhis2w_client.generated.v43.oas._enums import (
    MessageConversationPriority,
    MessageConversationStatus,
)
from dhis2w_client.v43._collection import parse_collection
from dhis2w_client.v43.envelopes import WebMessageResponse

if TYPE_CHECKING:
    from dhis2w_client.v43.client import Dhis2Client

MessagePriority = Literal["NONE", "LOW", "MEDIUM", "HIGH"]
MessageStatus = Literal["NONE", "OPEN", "PENDING", "INVALID", "SOLVED"]


class Recipient(BaseModel):
    """One addressee of an outgoing message — reference to a user, user group, or organisation unit.

    Messages accept three overlapping recipient lists (`users`, `userGroups`,
    `organisationUnits`); every kind is an `{id}` reference on the wire.
    `Recipient` is a thin domain name over that — `kind` names where DHIS2
    delivers the message, `uid` is the referenced entity.
    """

    model_config = ConfigDict(frozen=True)

    uid: str
    kind: str  # "user" | "userGroup" | "organisationUnit"


class MessagingAccessor:
    """`Dhis2Client.messaging` — conversation list + send + reply + mark-read.

    Returns typed `MessageConversation` from the OAS schema. For attachments,
    upload via `client.files.upload_file_resource(..., domain='MESSAGE_ATTACHMENT')`
    first, then pass the returned UID to `send` / `reply` via `attachments`.
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_conversations(
        self,
        *,
        filter: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[MessageConversation]:
        """List conversations the authenticated user is part of.

        `filter` accepts DHIS2's standard `property:operator:value` DSL
        (e.g. `"read:eq:false"` for unread-only). `page` is 1-indexed;
        DHIS2 defaults `pageSize` to 50.
        """
        params: dict[str, Any] = {"fields": "id,subject,read,messageType,lastMessage,lastSender,messageCount"}
        if filter is not None:
            params["filter"] = filter
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size
        raw = await self._client.get_raw("/api/messageConversations", params=params)
        return parse_collection(raw, "messageConversations", MessageConversation)

    async def get_conversation(self, uid: str) -> MessageConversation:
        """Fetch one conversation with its full message thread (`/api/messageConversations/{uid}`).

        Explicit `fields=` selector — DHIS2's default selector returns only
        `messages[id]`, so the text + sender + created timestamp have to be
        asked for. This fetches enough to render a readable thread without
        bringing down translations / sharing / attribute values.
        """
        fields = (
            "id,subject,read,messageType,status,priority,messageCount,"
            "lastUpdated,lastSender[id,displayName,name],lastMessage,"
            "userMessages[user[id,displayName],read,followUp],"
            "messages[id,text,created,sender[id,displayName,name],internal,attachments[id,name,contentType]]"
        )
        return await self._client.get(
            f"/api/messageConversations/{uid}",
            model=MessageConversation,
            params={"fields": fields},
        )

    async def send(
        self,
        *,
        subject: str,
        text: str,
        users: Sequence[str] | None = None,
        user_groups: Sequence[str] | None = None,
        organisation_units: Sequence[str] | None = None,
        attachments: Sequence[str] | None = None,
    ) -> MessageConversation:
        """Create a new conversation + first message; returns the new conversation.

        At least one of `users` / `user_groups` / `organisation_units` must
        be non-empty — DHIS2 silently drops messages with no recipients.
        Each value is a UID. `attachments` is a list of fileResource UIDs
        previously uploaded with `domain=MESSAGE_ATTACHMENT`.

        The returned `MessageConversation` is freshly fetched — the
        create endpoint returns just the status envelope, not the new
        UID (see BUGS.md #17). The UID is extracted from the 201
        `Location` header; this method GETs the conversation back so the
        caller receives a typed object instead of parsing a URL.
        """
        if not (users or user_groups or organisation_units):
            raise ValueError(
                "messaging.send requires at least one recipient — "
                "pass `users=[...]`, `user_groups=[...]`, or `organisation_units=[...]`",
            )
        body: dict[str, Any] = {"subject": subject, "text": text}
        if users:
            body["users"] = [{"id": uid} for uid in users]
        if user_groups:
            body["userGroups"] = [{"id": uid} for uid in user_groups]
        if organisation_units:
            body["organisationUnits"] = [{"id": uid} for uid in organisation_units]
        if attachments:
            body["attachments"] = [{"id": uid} for uid in attachments]
        response = await self._client._request(  # noqa: SLF001 — accessor is tight with the client
            "POST",
            "/api/messageConversations",
            json=body,
        )
        location = response.headers.get("location")
        if not location:
            raise RuntimeError(
                "DHIS2 accepted the message but returned no Location header — "
                "can't look up the created conversation UID.",
            )
        # `Location` is an absolute URL on DHIS2's canonical host; the last
        # path segment is the new UID.
        created_uid = location.rstrip("/").rsplit("/", 1)[-1]
        return await self.get_conversation(created_uid)

    async def reply(
        self,
        uid: str,
        *,
        text: str,
    ) -> WebMessageResponse:
        """Reply to an existing conversation (`POST /api/messageConversations/{uid}`).

        DHIS2's reply endpoint takes `text/plain` body — not JSON — and
        stores the raw bytes as the message text. JSON objects get
        stringified verbatim. Attachments + the internal-note flag only
        work on the initial `send()`; to attach a file after a conversation
        already exists, start a new conversation (or use
        `/api/messageConversations/{uid}/attachments` via `post_raw`
        directly if your DHIS2 build supports it — not wired here).
        """
        response = await self._client._request(  # noqa: SLF001 — accessor is tight with the client
            "POST",
            f"/api/messageConversations/{uid}",
            content=text.encode("utf-8"),
            extra_headers={"Content-Type": "text/plain"},
        )
        # DHIS2 returns its standard status envelope on 201; parse it for
        # caller-visible status + message.
        body: dict[str, Any] = {}
        if response.content:
            try:
                body = response.json()
            except ValueError:
                body = {"status": "OK", "httpStatus": response.reason_phrase}
        return WebMessageResponse.model_validate(body or {"status": "OK"})

    async def mark_read(self, uids: str | Sequence[str]) -> WebMessageResponse:
        """Flip one or many conversations to read (`POST /api/messageConversations/read`).

        DHIS2's bulk endpoint takes an array body of UIDs. A single string
        input is wrapped for convenience.
        """
        return await self._mark(uids, path="/api/messageConversations/read")

    async def mark_unread(self, uids: str | Sequence[str]) -> WebMessageResponse:
        """Flip one or many conversations to unread (`POST /api/messageConversations/unread`)."""
        return await self._mark(uids, path="/api/messageConversations/unread")

    async def delete_conversation(self, uid: str) -> None:
        """Delete a conversation. DHIS2 soft-deletes for the calling user — other participants still see it."""
        await self._client.delete_raw(f"/api/messageConversations/{uid}")

    async def set_priority(
        self,
        uid: str,
        priority: MessagePriority | MessageConversationPriority,
    ) -> None:
        """Set the ticket-workflow priority on a conversation.

        Accepts `"NONE"` / `"LOW"` / `"MEDIUM"` / `"HIGH"` (matching the
        `MessageConversationPriority` OAS enum). DHIS2 accepts this call on
        any message type — most useful on `TICKET`-type conversations but
        stores on PRIVATE threads too.
        """
        await self._client._request(  # noqa: SLF001 — accessor is tight with the client
            "POST",
            f"/api/messageConversations/{uid}/priority",
            params={"messageConversationPriority": str(priority)},
        )

    async def set_status(
        self,
        uid: str,
        status: MessageStatus | MessageConversationStatus,
    ) -> None:
        """Set the ticket-workflow status on a conversation.

        Accepts `"NONE"` / `"OPEN"` / `"PENDING"` / `"INVALID"` / `"SOLVED"`
        (matching the `MessageConversationStatus` OAS enum).
        """
        await self._client._request(  # noqa: SLF001
            "POST",
            f"/api/messageConversations/{uid}/status",
            params={"messageConversationStatus": str(status)},
        )

    async def assign(self, uid: str, user_uid: str) -> None:
        """Assign a conversation to a user (ticket workflows)."""
        await self._client._request(  # noqa: SLF001
            "POST",
            f"/api/messageConversations/{uid}/assign",
            params={"userId": user_uid},
        )

    async def unassign(self, uid: str) -> None:
        """Remove the assignee from a conversation."""
        await self._client._request(  # noqa: SLF001
            "DELETE",
            f"/api/messageConversations/{uid}/assign",
        )

    async def _mark(self, uids: str | Sequence[str], *, path: str) -> WebMessageResponse:
        """POST a list of conversation UIDs to a bulk read/unread endpoint."""
        payload = [uids] if isinstance(uids, str) else list(uids)
        raw = await self._client.post_raw(path, body=payload)
        return WebMessageResponse.model_validate(raw)


__all__ = [
    "MessageConversation",
    "MessagePriority",
    "MessageStatus",
    "MessagingAccessor",
    "Recipient",
]
