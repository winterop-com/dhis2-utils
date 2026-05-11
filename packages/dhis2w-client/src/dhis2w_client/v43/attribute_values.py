"""Cross-resource `attributeValues` helpers for DHIS2 integration workflows.

DHIS2 exposes user-defined `Attribute` objects as the extensibility point
for metadata: any resource that carries an `attributeValues` field
(DataElements, Options, OrganisationUnits, Indicators, Dashboards, …)
can attach arbitrary typed key-value pairs, keyed by the Attribute's
UID. Integrations use this for cross-system code mapping — ICD-10 on
DataElements, SNOMED on Options, external-warehouse IDs on OrgUnits.

This accessor gives one consistent surface for those workflows. Every
method dispatches on a plural `resource` string matching the DHIS2 API
endpoint (`"dataElements"`, `"options"`, `"organisationUnits"`, …), so
one helper works across every attribute-bearing resource without a
per-type sibling class.

`client.option_sets` keeps its own thin option-specific wrappers
(`get_option_attribute_value` etc.) for ergonomics — they now delegate
here so the wire-shape workarounds (BUGS.md #21's attribute-UID-as-
filter-property) live in one place.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dhis2w_client.v43.client import Dhis2Client


class AttributeValuesAccessor:
    """`Dhis2Client.attribute_values` — read / write / search AttributeValues on any resource."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client — reuses its auth + HTTP pool for every request."""
        self._client = client

    async def resolve_attribute_uid(self, attribute_code_or_uid: str) -> str:
        """Resolve an Attribute identifier to its DHIS2 UID; raise LookupError on miss.

        Integrations usually know an Attribute by its business `code`
        (e.g. `SNOMED_CODE`) but DHIS2's filter DSL for attribute values
        keys by the Attribute's UID (BUGS.md #21). This helper turns the
        code into a UID via `/api/attributes?filter=code:eq:{code}`; UIDs
        pass through unchanged.
        """
        from dhis2w_client.v43.uids import is_valid_uid  # noqa: PLC0415

        if is_valid_uid(attribute_code_or_uid):
            return attribute_code_or_uid
        raw = await self._client.get_raw(
            "/api/attributes",
            params={"filter": f"code:eq:{attribute_code_or_uid}", "fields": "id", "paging": "false"},
        )
        hits = raw.get("attributes")
        if not isinstance(hits, list) or not hits:
            raise LookupError(
                f"no Attribute with code {attribute_code_or_uid!r} (and not a valid UID). "
                "Create the Attribute first via `client.resources.attributes.create(...)`.",
            )
        first = hits[0]
        if not isinstance(first, dict):
            raise LookupError(f"attribute row for {attribute_code_or_uid!r} is not an object: {first!r}")
        attribute_id = first.get("id")
        if not isinstance(attribute_id, str):
            raise LookupError(f"attribute row for {attribute_code_or_uid!r} has no `id` field: {first!r}")
        return attribute_id

    async def get_value(
        self,
        resource: str,
        resource_uid: str,
        attribute_code_or_uid: str,
    ) -> str | None:
        """Read one attribute value off a resource; None if the attribute isn't set.

        `resource` is the plural DHIS2 API name (`"dataElements"`,
        `"options"`, `"organisationUnits"`, …). The resource must carry
        an `attributeValues` field server-side — DHIS2 returns a typed
        error otherwise, which bubbles up unchanged.
        """
        attribute_uid = await self.resolve_attribute_uid(attribute_code_or_uid)
        raw = await self._client.get_raw(
            f"/api/{resource}/{resource_uid}",
            params={"fields": "id,attributeValues[value,attribute[id]]"},
        )
        attribute_values = raw.get("attributeValues") or []
        if not isinstance(attribute_values, list):
            return None
        for entry in attribute_values:
            if not isinstance(entry, dict):
                continue
            attribute = entry.get("attribute")
            if isinstance(attribute, dict) and attribute.get("id") == attribute_uid:
                raw_value = entry.get("value")
                return str(raw_value) if raw_value is not None else None
        return None

    async def set_value(
        self,
        resource: str,
        resource_uid: str,
        attribute_code_or_uid: str,
        value: str,
    ) -> None:
        """Set / replace one attribute value on a resource (read-merge-write).

        Reads the full resource, merges the new attribute value (replaces
        any prior entry for the same attribute UID), PUTs the payload
        back. DHIS2 rejects partial PATCH on `attributeValues` on
        multiple resource types (the list is identity-keyed by attribute
        UID, not index), so the full round-trip is the only path that
        behaves consistently.
        """
        attribute_uid = await self.resolve_attribute_uid(attribute_code_or_uid)
        raw = await self._client.get_raw(f"/api/{resource}/{resource_uid}")
        attribute_values = raw.get("attributeValues") or []
        if not isinstance(attribute_values, list):
            attribute_values = []
        merged = [
            entry
            for entry in attribute_values
            if not (
                isinstance(entry, dict)
                and isinstance(entry.get("attribute"), dict)
                and entry["attribute"].get("id") == attribute_uid
            )
        ]
        merged.append({"value": value, "attribute": {"id": attribute_uid}})
        raw["attributeValues"] = merged
        await self._client.put_raw(f"/api/{resource}/{resource_uid}", raw)

    async def delete_value(
        self,
        resource: str,
        resource_uid: str,
        attribute_code_or_uid: str,
    ) -> bool:
        """Remove one attribute value from a resource; return True if anything was removed.

        Same read-merge-write pattern as `set_value`; when the attribute
        isn't present on the resource the call is a no-op and returns
        `False` (no HTTP PUT fires — avoids gratuitous churn on
        `lastUpdated` fields).
        """
        attribute_uid = await self.resolve_attribute_uid(attribute_code_or_uid)
        raw = await self._client.get_raw(f"/api/{resource}/{resource_uid}")
        attribute_values = raw.get("attributeValues") or []
        if not isinstance(attribute_values, list):
            return False
        filtered = [
            entry
            for entry in attribute_values
            if not (
                isinstance(entry, dict)
                and isinstance(entry.get("attribute"), dict)
                and entry["attribute"].get("id") == attribute_uid
            )
        ]
        if len(filtered) == len(attribute_values):
            return False
        raw["attributeValues"] = filtered
        await self._client.put_raw(f"/api/{resource}/{resource_uid}", raw)
        return True

    async def find_uids_by_value(
        self,
        resource: str,
        attribute_code_or_uid: str,
        value: str,
        *,
        extra_filters: Sequence[str] | None = None,
    ) -> list[str]:
        """Reverse lookup — every resource UID whose attribute value matches.

        DHIS2's filter DSL for attribute values is the quirky
        `<attributeUid>:eq:<value>` form (see BUGS.md #21). This helper
        resolves the business code to UID then emits the quirky-but-
        working filter. Additional constraints pass through as
        `extra_filters` — e.g. scope an Option lookup to one OptionSet
        via `extra_filters=["optionSet.id:eq:OsVaccType1"]`, or narrow a
        DataElement lookup via `extra_filters=["domainType:eq:AGGREGATE"]`.

        Callers wanting the full typed model should round-trip the
        returned UIDs through `client.resources.<resource>.get(uid)` —
        this accessor stays generic over resource types by returning
        UIDs only.
        """
        attribute_uid = await self.resolve_attribute_uid(attribute_code_or_uid)
        filters: list[str] = [f"{attribute_uid}:eq:{value}"]
        if extra_filters:
            filters.extend(extra_filters)
        raw = await self._client.get_raw(
            f"/api/{resource}",
            params={
                "filter": filters,
                "fields": "id",
                "paging": "false",
            },
        )
        rows = raw.get(resource)
        if not isinstance(rows, list):
            return []
        return [row["id"] for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)]

    async def find_one_uid_by_value(
        self,
        resource: str,
        attribute_code_or_uid: str,
        value: str,
        *,
        extra_filters: Sequence[str] | None = None,
    ) -> str | None:
        """Reverse lookup helper — return the first matching UID, or None on miss."""
        uids = await self.find_uids_by_value(
            resource,
            attribute_code_or_uid,
            value,
            extra_filters=extra_filters,
        )
        return uids[0] if uids else None


def _attribute_value_entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract a typed-ish `attributeValues` list from a raw resource payload."""
    entries = payload.get("attributeValues") or []
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


__all__ = ["AttributeValuesAccessor"]
