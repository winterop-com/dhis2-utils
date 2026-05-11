"""Typed helpers for DHIS2's sharing API.

DHIS2 models access to every persistable object as a `sharing` block: a
public-access string, an owning user, and two lists of per-user / per-user-group
grants. The wire shape has two flavours:

- `SharingObject` — what `/api/sharing?type=<t>&id=<uid>` returns inside
  `SharingInfo.object`. Carries `publicAccess`, `userAccesses`, `userGroupAccesses`.
- `Sharing` — what metadata resources carry on their `sharing` field. Same
  information but `userAccesses[]` becomes a keyed map `users: {uid: {...}}`
  (same for groups), matching how DHIS2 stores it internally.

This module ships three utilities:

- `access_string(metadata="rw", data="rw")` — compose the 8-char access string
  DHIS2 uses (`"rwrw----"`, `"r-------"`, etc.). Constants for the common forms.
- `get_sharing(client, resource_type, uid)` — fetch the current block via
  `GET /api/sharing`.
- `apply_sharing(client, resource_type, uid, sharing)` — replace it via
  `POST /api/sharing`. Returns a `WebMessageResponse`.
- A `SharingBuilder` convenience for building up `SharingObject` without
  typing the map-vs-list details by hand.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict

from dhis2w_client.generated.v42.oas import (
    Sharing,
    SharingInfo,
    SharingObject,
    SharingUser,
    SharingUserAccess,
    SharingUserGroupAccess,
)
from dhis2w_client.v42.envelopes import WebMessageResponse

if TYPE_CHECKING:
    from dhis2w_client.v42.client import Dhis2Client

# Access string literals. DHIS2's access grammar packs four capabilities
# into an 8-char string: metadata r/w, data r/w, reserved (hyphens).
#
#   positions 0-1: metadata read ('r') / write ('w'). '--' means no access.
#   positions 2-3: data read / write. '--' means no data-level access.
#   positions 4-7: reserved; must be '----'.
#
# Each position is either the letter or '-'. See BUGS.md and
# docs/architecture/user-plugin.md for the full mapping.
AccessPattern = Literal["rw", "r-", "--"]

ACCESS_NONE = "--------"
ACCESS_READ_METADATA = "r-------"
ACCESS_READ_WRITE_METADATA = "rw------"
ACCESS_READ_DATA = "r-r-----"
ACCESS_READ_WRITE_DATA = "rwrw----"


def access_string(*, metadata: AccessPattern = "--", data: AccessPattern = "--") -> str:
    """Compose an 8-char DHIS2 access string from metadata + data r/w pairs.

    Examples:
        >>> access_string(metadata="rw")  # metadata-only read/write
        'rw------'
        >>> access_string(metadata="r-", data="r-")  # read-everything
        'r-r-----'
        >>> access_string(metadata="rw", data="rw")  # full access
        'rwrw----'
    """
    metadata_part = metadata.ljust(2, "-")
    data_part = data.ljust(2, "-")
    return f"{metadata_part}{data_part}----"


class SharingBuilder(BaseModel):
    """Fluent-ish builder for `SharingObject` so callers don't hand-assemble maps.

    Callers that want to attach fresh sharing to an object work in terms of
    "grant user X read+write", not "build a `SharingUserAccess` and append it
    to the list". The builder hides that boilerplate while producing the exact
    wire shape `POST /api/sharing` wants.
    """

    model_config = ConfigDict(extra="allow")

    public_access: str = ACCESS_READ_METADATA
    external_access: bool = False
    owner_user_id: str | None = None
    user_accesses: dict[str, str] = {}
    user_group_accesses: dict[str, str] = {}

    def grant_user(self, user_id: str, access: str) -> SharingBuilder:
        """Grant `access` to one user (overwrites any existing grant)."""
        return self.model_copy(update={"user_accesses": {**self.user_accesses, user_id: access}})

    def grant_user_group(self, group_id: str, access: str) -> SharingBuilder:
        """Grant `access` to one user group (overwrites any existing grant)."""
        return self.model_copy(
            update={"user_group_accesses": {**self.user_group_accesses, group_id: access}},
        )

    def to_sharing_object(self) -> SharingObject:
        """Materialise the builder into the `SharingObject` wire shape."""
        return SharingObject(
            publicAccess=self.public_access,
            externalAccess=self.external_access,
            user=SharingUser(id=self.owner_user_id) if self.owner_user_id else None,
            userAccesses=[SharingUserAccess(id=uid, access=access) for uid, access in self.user_accesses.items()],
            userGroupAccesses=[
                SharingUserGroupAccess(id=gid, access=access) for gid, access in self.user_group_accesses.items()
            ],
        )


async def get_sharing(client: Dhis2Client, resource_type: str, uid: str) -> SharingObject:
    """Fetch `GET /api/sharing?type=<resource_type>&id=<uid>` → SharingObject.

    `resource_type` is the DHIS2 singular metadata-resource name as it appears
    in filter syntax and in the sharing API's `?type=` param — e.g.
    `"dataSet"`, `"dataElement"`, `"program"`, `"user"`. DHIS2 returns a
    `{meta, object}` envelope; callers almost always want just `.object`.
    """
    raw = await client.get_raw("/api/sharing", params={"type": resource_type, "id": uid})
    info = SharingInfo.model_validate(raw)
    if info.object is None:
        raise ValueError(f"/api/sharing returned no `object` for {resource_type}/{uid}")
    return info.object


async def apply_sharing(
    client: Dhis2Client,
    resource_type: str,
    uid: str,
    sharing: SharingObject | SharingBuilder,
) -> WebMessageResponse:
    """Replace the sharing block via `POST /api/sharing?type=<t>&id=<uid>`.

    DHIS2 ignores unknown fields and preserves the owner user when the payload
    omits it. Accepts either a `SharingObject` (raw wire shape) or a
    `SharingBuilder` (convenience form).
    """
    payload_obj = sharing.to_sharing_object() if isinstance(sharing, SharingBuilder) else sharing
    payload = {"object": payload_obj.model_dump(by_alias=True, exclude_none=True, mode="json")}
    return await client.post(
        "/api/sharing",
        payload,
        params={"type": resource_type, "id": uid},
        model=WebMessageResponse,
    )


__all__ = [
    "ACCESS_NONE",
    "ACCESS_READ_DATA",
    "ACCESS_READ_METADATA",
    "ACCESS_READ_WRITE_DATA",
    "ACCESS_READ_WRITE_METADATA",
    "AccessPattern",
    "Sharing",
    "SharingBuilder",
    "SharingObject",
    "access_string",
    "apply_sharing",
    "get_sharing",
]
