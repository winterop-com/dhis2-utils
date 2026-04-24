"""ValidationRuleGroup authoring — `Dhis2Client.validation_rule_groups`.

`ValidationRuleGroup`s collect ValidationRules into named runs so
`dhis2 maintenance validation run --group <uid>` exercises a coherent
subset (BCG-dose rules, ANC rules, …). Follows the same CRUD +
per-item membership pattern as IndicatorGroupsAccessor.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.generated.v42.schemas import ValidationRule, ValidationRuleGroup

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client
from dhis2_client.envelopes import WebMessageResponse

_GROUP_FIELDS: str = "id,name,shortName,code,description,validationRules[id,name,code]"
_MEMBER_FIELDS: str = "id,name,shortName,code,periodType,importance,operator"


class ValidationRuleGroupsAccessor:
    """`Dhis2Client.validation_rule_groups` — CRUD + membership over `/api/validationRuleGroups`."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def list_all(self) -> list[ValidationRuleGroup]:
        """Return every ValidationRuleGroup."""
        raw = await self._client.get_raw(
            "/api/validationRuleGroups",
            params={"fields": _GROUP_FIELDS, "paging": "false"},
        )
        rows = raw.get("validationRuleGroups") or []
        return [ValidationRuleGroup.model_validate(row) for row in rows if isinstance(row, dict)]

    async def get(self, uid: str) -> ValidationRuleGroup:
        """Fetch one group by UID with its `validationRules` refs populated."""
        return await self._client.get(
            f"/api/validationRuleGroups/{uid}", model=ValidationRuleGroup, params={"fields": _GROUP_FIELDS}
        )

    async def list_members(
        self,
        uid: str,
        *,
        page: int = 1,
        page_size: int = 50,
    ) -> list[ValidationRule]:
        """Page through ValidationRules belonging to one group."""
        raw = await self._client.get_raw(
            "/api/validationRules",
            params={
                "filter": f"validationRuleGroups.id:eq:{uid}",
                "fields": _MEMBER_FIELDS,
                "page": str(page),
                "pageSize": str(page_size),
                "order": "name:asc",
            },
        )
        rows = raw.get("validationRules") or []
        return [ValidationRule.model_validate(row) for row in rows if isinstance(row, dict)]

    async def create(
        self,
        *,
        name: str,
        short_name: str | None = None,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
    ) -> ValidationRuleGroup:
        """Create an empty ValidationRuleGroup; add members afterwards via `add_members`."""
        payload: dict[str, Any] = {"name": name}
        if short_name:
            payload["shortName"] = short_name
        if uid:
            payload["id"] = uid
        if code:
            payload["code"] = code
        if description:
            payload["description"] = description
        envelope = await self._client.post("/api/validationRuleGroups", payload, model=WebMessageResponse)
        created_uid = envelope.created_uid or uid
        if not created_uid:
            raise RuntimeError("validation-rule-group create did not return a uid")
        return await self.get(created_uid)

    async def update(self, group: ValidationRuleGroup) -> ValidationRuleGroup:
        """PUT an edited ValidationRuleGroup back. `group.id` must be set."""
        if not group.id:
            raise ValueError("update requires group.id to be set")
        body = group.model_dump(by_alias=True, exclude_none=True, mode="json")
        await self._client.put_raw(f"/api/validationRuleGroups/{group.id}", body=body)
        return await self.get(group.id)

    async def add_members(self, uid: str, *, validation_rule_uids: list[str]) -> ValidationRuleGroup:
        """Add ValidationRules to the group via the per-item POST shortcut."""
        for rule_uid in validation_rule_uids:
            await self._client.resources.validation_rule_groups.add_collection_item(uid, "validationRules", rule_uid)
        return await self.get(uid)

    async def remove_members(self, uid: str, *, validation_rule_uids: list[str]) -> ValidationRuleGroup:
        """Drop ValidationRules from the group via the per-item DELETE shortcut."""
        for rule_uid in validation_rule_uids:
            await self._client.resources.validation_rule_groups.remove_collection_item(uid, "validationRules", rule_uid)
        return await self.get(uid)

    async def delete(self, uid: str) -> None:
        """Delete the grouping row — member rules stay."""
        if not uid:
            raise ValueError("delete requires a non-empty uid")
        await self._client.resources.validation_rule_groups.delete(uid)


__all__ = [
    "ValidationRuleGroup",
    "ValidationRuleGroupsAccessor",
]
