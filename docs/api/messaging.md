# Messaging

`MessagingAccessor` on `Dhis2Client.messaging` — DHIS2 internal messaging via `/api/messageConversations` with the full ticket-workflow fields (status, priority, assignee). Pairs with the [Files](files.md) accessor for `MESSAGE_ATTACHMENT` `FileResource`s.

## When to reach for it

- Notify a user / group / role from a script ("audit found 7 conflicts on dataset X — please review").
- Implement a ticket workflow on top of DHIS2 (status, priority, assignee transitions are first-party on `/api/messageConversations`).
- Send a file along with the message — upload first via the files accessor, reference the resource UID on `send`.

## Worked example — send + iterate the inbox

```python
from dhis2w_core.client_context import open_client
from dhis2w_core.profile import profile_from_env

async with open_client(profile_from_env()) as client:
    # 1. Send a new conversation. Recipients are typed `Recipient` refs;
    #    pass any combination of user / userGroup / userRole.
    conversation = await client.messaging.send(
        subject="Audit ping",
        text="Please confirm dataset X has been reviewed for May 2026.",
        users=["abcdefghij"],          # user UIDs
        user_groups=["GROUPxxxxxx"],   # optional
    )
    print(f"created  {conversation.id}  subject={conversation.subject!r}")

    # 2. Iterate the inbox; filter by ticket-workflow status.
    open_threads = await client.messaging.list(status="OPEN", page_size=20)
    for c in open_threads:
        print(f"  {c.id}  status={c.status}  subject={c.subject!r}")

    # 3. Reply to one (plain text — DHIS2's reply endpoint is text-only).
    await client.messaging.reply(conversation.id, text="Confirmed.")

    # 4. Close the ticket.
    await client.messaging.set_status(conversation.id, status="SOLVED")
```

## Worked example — message with attachment

```python
async with open_client(profile_from_env()) as client:
    # 1. Upload the file as a MESSAGE_ATTACHMENT-domain FileResource.
    resource = await client.files.upload_file_resource(
        path="./audit-results.pdf",
        domain="MESSAGE_ATTACHMENT",
    )
    # 2. Send the message, referencing the resource UID. DHIS2 accepts a list
    #    of `{id: <resource-uid>}` refs on the initial send (not on reply).
    await client.messaging.send(
        subject="Audit results",
        text="Attached: PDF report for dataset X.",
        users=["abcdefghij"],
        attachments=[resource.id],
    )
```

Worked end-to-end demo: [`examples/v42/client/messaging_with_attachment.py`](https://github.com/winterop-com/dhis2w-utils/blob/main/examples/v42/client/messaging_with_attachment.py) (covers send + reply + mark-read + delete).

::: dhis2w_client.v42.messaging
