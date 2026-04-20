# Messaging

`MessagingAccessor` on `Dhis2Client.messaging` — DHIS2 internal messaging via `/api/messageConversations`. Pairs with the files plugin for `MESSAGE_ATTACHMENT` fileResources: upload via `client.files.upload_file_resource(..., domain="MESSAGE_ATTACHMENT")`, then reference the UID in `send` / `reply`.

::: dhis2_client.messaging
