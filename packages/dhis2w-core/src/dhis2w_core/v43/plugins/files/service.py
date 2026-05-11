"""Service layer for the `files` plugin — thin orchestration over `Dhis2Client.files`."""

from __future__ import annotations

from pathlib import Path

from dhis2w_client.v43 import Document, FileResource, FileResourceDomain

from dhis2w_core.profile import Profile
from dhis2w_core.v43.client_context import open_client

# ---- documents ------------------------------------------------------


async def list_documents(
    profile: Profile,
    *,
    filter: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> list[Document]:
    """List documents; forwards `filter` / `page` / `page_size` straight to DHIS2."""
    async with open_client(profile) as client:
        return await client.files.list_documents(filter=filter, page=page, page_size=page_size)


async def get_document(profile: Profile, uid: str) -> Document:
    """Return typed metadata for one document."""
    async with open_client(profile) as client:
        return await client.files.get_document(uid)


async def upload_document(profile: Profile, path: Path, *, name: str | None = None) -> Document:
    """Upload `path` as a DHIS2 document; `name` defaults to the filename."""
    data = path.read_bytes()
    async with open_client(profile) as client:
        return await client.files.upload_document(data, name=name or path.name, filename=path.name)


async def create_external_document(profile: Profile, *, name: str, url: str) -> Document:
    """Create an EXTERNAL_URL document — DHIS2 stores no bytes; the UI links to `url`."""
    async with open_client(profile) as client:
        return await client.files.create_external_document(name=name, url=url)


async def download_document(profile: Profile, uid: str, destination: Path) -> int:
    """Download the binary payload to `destination`; returns the number of bytes written."""
    async with open_client(profile) as client:
        data = await client.files.download_document(uid)
    destination.write_bytes(data)
    return len(data)


async def delete_document(profile: Profile, uid: str) -> None:
    """Delete one document (`/api/documents/{uid}`)."""
    async with open_client(profile) as client:
        await client.files.delete_document(uid)


# ---- file resources -------------------------------------------------


async def upload_file_resource(
    profile: Profile,
    path: Path,
    *,
    domain: FileResourceDomain | str = FileResourceDomain.DATA_VALUE,
) -> FileResource:
    """Upload `path` as a fileResource in `domain` and return the created resource."""
    data = path.read_bytes()
    async with open_client(profile) as client:
        return await client.files.upload_file_resource(data, filename=path.name, domain=domain)


async def get_file_resource(profile: Profile, uid: str) -> FileResource:
    """Return typed metadata for one file resource."""
    async with open_client(profile) as client:
        return await client.files.get_file_resource(uid)


async def get_file_resources_bulk(profile: Profile, uids: list[str]) -> dict[str, FileResource]:
    """Fetch multiple fileResources concurrently; returns a `{uid: FileResource}` map.

    Used by the CLI `documents ls --details` path to enrich a documents
    table with each backing blob's contentType / size / storageStatus in a
    single round of concurrent requests.
    """
    if not uids:
        return {}

    async with open_client(profile) as client:
        import asyncio as _asyncio

        results = await _asyncio.gather(
            *(client.files.get_file_resource(uid) for uid in uids),
            return_exceptions=True,
        )
    index: dict[str, FileResource] = {}
    for uid, result in zip(uids, results, strict=True):
        if isinstance(result, FileResource):
            index[uid] = result
    return index


async def download_file_resource(profile: Profile, uid: str, destination: Path) -> int:
    """Download the file-resource payload to `destination`; returns bytes written."""
    async with open_client(profile) as client:
        data = await client.files.download_file_resource(uid)
    destination.write_bytes(data)
    return len(data)
