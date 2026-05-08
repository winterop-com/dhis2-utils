"""One-pass builder for the full Category dimension stack.

`build_category_combo(client, spec)` walks a declarative
`CategoryComboBuildSpec` and ensures the requested
`CategoryOption` -> `Category` -> `CategoryCombo` chain exists on the
target instance, creating only what's missing. Idempotent — re-running
the same spec is a no-op (modulo new options getting wired into
existing categories).

Lookup is by `name` (DHIS2 enforces unique names on each of the three
resource types). For each spec entry:

1. Each `CategoryOptionSpec` resolves to an existing CategoryOption
   (by name) or a fresh create.
2. Each `CategorySpec` resolves to an existing Category (by name) — if
   present, missing option UIDs are appended via `add_option`. If
   absent, the Category is created with all option UIDs wired in one
   POST.
3. The top-level `CategoryComboBuildSpec.name` resolves to an existing
   CategoryCombo (by name) — if present, missing category UIDs are
   appended via `add_category`. If absent, the combo is created with
   all category UIDs in order.
4. The helper polls the COC matrix until the expected count
   (the cross-product of option counts) lands.

Returns a typed `CategoryComboBuildResult` carrying every UID and a
created-vs-reused breakdown so callers can render a "what changed"
summary.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field

from dhis2w_client.generated.v42.schemas import Category, CategoryCombo, CategoryOption

if TYPE_CHECKING:
    from dhis2w_client.client import Dhis2Client


class CategoryOptionSpec(BaseModel):
    """One CategoryOption inside a CategorySpec.

    Resolved by `name` against the target instance. `short_name` defaults
    to `name` when omitted; DHIS2 caps shortName at 50 characters so
    longer names are truncated.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=230)
    short_name: str | None = Field(default=None, max_length=50)
    code: str | None = None
    description: str | None = None


class CategorySpec(BaseModel):
    """One Category axis of a CategoryComboBuildSpec.

    `options` order is preserved on creation and shapes the COC matrix
    layout. Existing categories are amended with any missing options
    appended in spec order.
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=230)
    short_name: str | None = Field(default=None, max_length=50)
    code: str | None = None
    description: str | None = None
    options: list[CategoryOptionSpec] = Field(..., min_length=1)


class CategoryComboBuildSpec(BaseModel):
    """Declarative spec for `build_category_combo`."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., min_length=1, max_length=230)
    categories: list[CategorySpec] = Field(..., min_length=1)
    code: str | None = None
    data_dimension_type: str = "DISAGGREGATION"
    skip_total: bool = False


class CategoryBuildEntry(BaseModel):
    """Per-category outcome of a build run."""

    model_config = ConfigDict(frozen=True)

    name: str
    uid: str
    created: bool
    option_uids: list[str]
    created_option_uids: list[str] = Field(default_factory=list)
    appended_option_uids: list[str] = Field(default_factory=list)


class CategoryComboBuildResult(BaseModel):
    """Outcome of `build_category_combo` — every UID + a created-vs-reused breakdown."""

    model_config = ConfigDict(frozen=True)

    combo_uid: str
    combo_created: bool
    combo_appended_category_uids: list[str] = Field(default_factory=list)
    categories: list[CategoryBuildEntry]
    expected_coc_count: int
    coc_count: int

    @property
    def category_uids(self) -> list[str]:
        """Ordered Category UIDs the combo references — useful for downstream wiring."""
        return [entry.uid for entry in self.categories]


async def build_category_combo(
    client: Dhis2Client,
    spec: CategoryComboBuildSpec,
    *,
    timeout_seconds: float = 120.0,
    poll_interval_seconds: float = 1.0,
) -> CategoryComboBuildResult:
    """Ensure `spec` exists end-to-end on the target instance, creating only what's missing.

    See module docstring for the resolution algorithm. The default
    `timeout_seconds=120` doubles the per-combo default on
    `wait_for_coc_generation` because rebuild on a fresh instance can
    take longer than steady-state regen.
    """
    expected_coc_count = 1
    for category_spec in spec.categories:
        expected_coc_count *= len(category_spec.options)

    # Step 1 + 2: resolve each category (and its options) into a UID.
    category_entries: list[CategoryBuildEntry] = []
    for category_spec in spec.categories:
        entry = await _resolve_category(client, category_spec)
        category_entries.append(entry)

    # Step 3: resolve the combo itself.
    combo_uids = [entry.uid for entry in category_entries]
    existing_combo = await _find_combo_by_name(client, spec.name)
    appended_category_uids: list[str] = []
    if existing_combo is not None and existing_combo.id:
        combo_uid = existing_combo.id
        existing_category_uids = {ref.get("id") for ref in (existing_combo.categories or []) if isinstance(ref, dict)}
        for cat_uid in combo_uids:
            if cat_uid not in existing_category_uids:
                await client.category_combos.add_category(combo_uid, cat_uid)
                appended_category_uids.append(cat_uid)
        combo_created = False
    else:
        created = await client.category_combos.create(
            name=spec.name,
            categories=combo_uids,
            code=spec.code,
            data_dimension_type=spec.data_dimension_type,
            skip_total=spec.skip_total,
        )
        if not created.id:
            raise RuntimeError("CategoryCombo create returned no id")
        combo_uid = created.id
        combo_created = True

    # Step 4: wait for the COC matrix to settle at the expected cross-product size.
    coc_count = await client.category_combos.wait_for_coc_generation(
        combo_uid,
        expected_count=expected_coc_count,
        timeout_seconds=timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )

    return CategoryComboBuildResult(
        combo_uid=combo_uid,
        combo_created=combo_created,
        combo_appended_category_uids=appended_category_uids,
        categories=category_entries,
        expected_coc_count=expected_coc_count,
        coc_count=coc_count,
    )


async def _resolve_category(client: Dhis2Client, spec: CategorySpec) -> CategoryBuildEntry:
    """Find-or-create one Category, ensuring every option in `spec.options` is wired."""
    option_uids: list[str] = []
    created_option_uids: list[str] = []
    for option_spec in spec.options:
        existing = await _find_option_by_name(client, option_spec.name)
        if existing is not None and existing.id:
            option_uids.append(existing.id)
            continue
        created = await client.category_options.create(
            name=option_spec.name,
            short_name=option_spec.short_name or option_spec.name[:50],
            code=option_spec.code,
            description=option_spec.description,
        )
        if not created.id:
            raise RuntimeError(f"CategoryOption create returned no id for {option_spec.name!r}")
        option_uids.append(created.id)
        created_option_uids.append(created.id)

    existing_category = await _find_category_by_name(client, spec.name)
    if existing_category is not None and existing_category.id:
        cat_uid = existing_category.id
        existing_option_uids = {
            ref.get("id") for ref in (existing_category.categoryOptions or []) if isinstance(ref, dict)
        }
        appended: list[str] = []
        for option_uid in option_uids:
            if option_uid not in existing_option_uids:
                await client.categories.add_option(cat_uid, option_uid)
                appended.append(option_uid)
        return CategoryBuildEntry(
            name=spec.name,
            uid=cat_uid,
            created=False,
            option_uids=option_uids,
            created_option_uids=created_option_uids,
            appended_option_uids=appended,
        )

    created_category = await client.categories.create(
        name=spec.name,
        short_name=spec.short_name or spec.name[:50],
        code=spec.code,
        description=spec.description,
        options=option_uids,
    )
    if not created_category.id:
        raise RuntimeError(f"Category create returned no id for {spec.name!r}")
    return CategoryBuildEntry(
        name=spec.name,
        uid=created_category.id,
        created=True,
        option_uids=option_uids,
        created_option_uids=created_option_uids,
    )


async def _find_option_by_name(client: Dhis2Client, name: str) -> CategoryOption | None:
    """Look up a CategoryOption by exact name; None when missing."""
    raw = await client.get_raw(
        "/api/categoryOptions",
        params={"fields": "id,name,categoryOptionGroups[id],categorys[id]", "filter": f"name:eq:{name}"},
    )
    rows = _hits(raw, "categoryOptions")
    return CategoryOption.model_validate(rows[0]) if rows else None


async def _find_category_by_name(client: Dhis2Client, name: str) -> Category | None:
    """Look up a Category by exact name; None when missing."""
    raw = await client.get_raw(
        "/api/categories",
        params={"fields": "id,name,categoryOptions[id]", "filter": f"name:eq:{name}"},
    )
    rows = _hits(raw, "categories")
    return Category.model_validate(rows[0]) if rows else None


async def _find_combo_by_name(client: Dhis2Client, name: str) -> CategoryCombo | None:
    """Look up a CategoryCombo by exact name; None when missing."""
    raw = await client.get_raw(
        "/api/categoryCombos",
        params={"fields": "id,name,categorys[id]", "filter": f"name:eq:{name}"},
    )
    rows = _hits(raw, "categoryCombos")
    return CategoryCombo.model_validate(rows[0]) if rows else None


def _hits(raw: dict[str, Any], collection_name: str) -> list[dict[str, Any]]:
    rows = raw.get(collection_name) or []
    return [row for row in rows if isinstance(row, dict)]


__all__ = [
    "CategoryBuildEntry",
    "CategoryComboBuildResult",
    "CategoryComboBuildSpec",
    "CategoryOptionSpec",
    "CategorySpec",
    "build_category_combo",
]
