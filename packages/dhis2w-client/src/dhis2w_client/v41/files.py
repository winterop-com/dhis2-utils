"""Document management + typed file-resource upload/download.

Two orthogonal DHIS2 file surfaces, one accessor on `Dhis2Client.files`:

- **`/api/documents`** — user-uploaded attachments tied to a CRUD metadata
  object. Types: `UPLOAD_FILE` (binary stored in DHIS2), `EXTERNAL_URL`
  (URL the DHIS2 UI links to). Appears in the DHIS2 `Data Administration`
  app.
- **`/api/fileResources`** — typed binary blobs referenced from other
  metadata: `DATA_VALUE` (file-type DataElement captures), `ICON`,
  `MESSAGE_ATTACHMENT`, etc. Create with a `domain`, get a UID back,
  then reference that UID from the owning resource.

Neither is part of the `customize` plugin — branding logos go through a
different endpoint family. This accessor is for operator-owned document
management + capture-media pipelines.
"""

from __future__ import annotations

import mimetypes
from typing import TYPE_CHECKING, Any, cast

from dhis2w_client.generated.v41.enums import FileResourceDomain
from dhis2w_client.generated.v41.oas import Document, FileResource

if TYPE_CHECKING:
    from dhis2w_client.v41.client import Dhis2Client


class FilesAccessor:
    """`Dhis2Client.files` — documents + file resources.

    All calls reuse the client's open HTTP pool + auth. Downloads buffer
    the response body into memory (DHIS2 documents + file resources are
    typically < 10 MB each); stream-download for larger payloads belongs
    on a follow-up when a real use case surfaces.
    """

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    # ---- documents --------------------------------------------------

    async def list_documents(
        self,
        *,
        filter: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> list[Document]:
        """List `/api/documents` — typed `Document` objects without the binary payload."""
        filters: list[str] | None = [filter] if filter else None
        return cast(
            list[Document],
            await self._client.resources.documents.list(
                fields=":owner",
                filters=filters,
                page=page,
                page_size=page_size,
            ),
        )

    async def get_document(self, uid: str) -> Document:
        """Return metadata for one document (`/api/documents/{uid}`)."""
        return await self._client.get(f"/api/documents/{uid}", model=Document)

    async def upload_document(
        self,
        data: bytes,
        *,
        name: str,
        filename: str | None = None,
        content_type: str | None = None,
    ) -> Document:
        """Upload a binary as a DHIS2 document and return the created `Document`.

        DHIS2 doesn't accept multipart-form POSTs on `/api/documents`
        directly (415 Unsupported Media Type — see BUGS.md #16). The
        correct workflow is a two-step:

        1. Upload the bytes as a `FileResource` with `domain=DOCUMENT` via
           `/api/fileResources`.
        2. `POST /api/documents` (JSON) with `url=<fileResourceUid>` so the
           document references the already-stored file resource.

        `contentType` is inferred from `filename` when not set. The
        returned `Document` carries the new UID.
        """
        resolved_filename = filename or name
        file_resource = await self.upload_file_resource(
            data,
            filename=resolved_filename,
            domain=FileResourceDomain.DOCUMENT,
            content_type=content_type,
        )
        raw = await self._client.post_raw(
            "/api/documents",
            body={
                "name": name,
                "url": file_resource.id,
                "external": False,
                "attachment": True,
            },
        )
        created_uid = _uid_from_web_message(raw)
        if created_uid is None:
            raise RuntimeError(f"document upload did not return a uid: {raw!r}")
        return await self.get_document(created_uid)

    async def create_external_document(
        self,
        *,
        name: str,
        url: str,
    ) -> Document:
        """Create an EXTERNAL_URL document (no binary; DHIS2 links to `url`)."""
        body = {"name": name, "url": url, "external": True, "attachment": False}
        raw = await self._client.post_raw("/api/documents", body=body)
        created_uid = _uid_from_web_message(raw)
        if created_uid is None:
            raise RuntimeError(f"external document create did not return a uid: {raw!r}")
        return await self.get_document(created_uid)

    async def download_document(self, uid: str) -> bytes:
        """Fetch the binary payload at `/api/documents/{uid}/data`."""
        response = await self._client._request(  # noqa: SLF001
            "GET",
            f"/api/documents/{uid}/data",
        )
        return response.content

    async def delete_document(self, uid: str) -> None:
        """Delete `/api/documents/{uid}`."""
        await self._client.resources.documents.delete(uid)

    # ---- file resources --------------------------------------------

    async def upload_file_resource(
        self,
        data: bytes,
        *,
        filename: str,
        domain: FileResourceDomain | str = FileResourceDomain.DATA_VALUE,
        content_type: str | None = None,
    ) -> FileResource:
        """Upload a file resource and return the created `FileResource`.

        `domain` picks the storage family (`DATA_VALUE` for file-type DE
        captures, `ICON` for custom icons, `MESSAGE_ATTACHMENT`, etc.).
        DHIS2 returns a `WebMessage` envelope with the created UID under
        `response.fileResource.id` (NOT `response.uid` like `/api/documents`).
        The returned `FileResource` is then the UID you reference from
        the owning resource.
        """
        resolved_content_type = content_type or _guess_content_type(filename)
        domain_value = domain.value if isinstance(domain, FileResourceDomain) else str(domain)
        response = await self._client._request(  # noqa: SLF001
            "POST",
            "/api/fileResources",
            files={"file": (filename, data, resolved_content_type)},
            params={"domain": domain_value},
        )
        body = response.json() if response.content else {}
        created_uid = _uid_from_file_resource_response(body)
        if created_uid is None:
            raise RuntimeError(f"fileResource upload did not return a uid: {body!r}")
        return await self.get_file_resource(created_uid)

    async def get_file_resource(self, uid: str) -> FileResource:
        """Return metadata for one file resource (`/api/fileResources/{uid}`)."""
        return await self._client.get(f"/api/fileResources/{uid}", model=FileResource)

    async def download_file_resource(self, uid: str) -> bytes:
        """Fetch the binary payload at `/api/fileResources/{uid}/data`."""
        response = await self._client._request(  # noqa: SLF001
            "GET",
            f"/api/fileResources/{uid}/data",
        )
        return response.content


def _guess_content_type(filename: str) -> str:
    """Return a sensible Content-Type for `filename`; falls back to `application/octet-stream`."""
    guessed, _ = mimetypes.guess_type(filename)
    return guessed or "application/octet-stream"


def _uid_from_web_message(body: Any) -> str | None:
    """Pull `response.uid` from a DHIS2 WebMessage envelope; returns `None` when absent."""
    if not isinstance(body, dict):
        return None
    response = body.get("response")
    if isinstance(response, dict):
        uid = response.get("uid")
        if isinstance(uid, str) and uid:
            return uid
    # Fallback: some paths embed the created object directly.
    direct = body.get("id")
    if isinstance(direct, str) and direct:
        return direct
    return None


def _uid_from_file_resource_response(body: Any) -> str | None:
    """Pull the created fileResource UID from DHIS2's nested response envelope.

    `POST /api/fileResources` returns `{ response: { fileResource: { id: ... } } }`,
    not the flat `response.uid` shape the generic metadata endpoints use.
    """
    if not isinstance(body, dict):
        return None
    response = body.get("response")
    if isinstance(response, dict):
        file_resource = response.get("fileResource")
        if isinstance(file_resource, dict):
            uid = file_resource.get("id")
            if isinstance(uid, str) and uid:
                return uid
    return _uid_from_web_message(body)


__all__ = ["Document", "FileResource", "FileResourceDomain", "FilesAccessor"]
