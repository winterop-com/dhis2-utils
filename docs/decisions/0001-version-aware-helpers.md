# 0001 — Version-aware client helpers

**Status:** Proposed (sketch).
**Target release:** v0.7.0 — public-API-shape change; minor bump under pre-1.0 SemVer.

## Context

`Dhis2Client.connect()` already discovers the live DHIS2 version and loads the matching `dhis2w_client.generated.v{42|43}` module into `self._generated`. The generated tree's `Resources` accessor is constructed from that, so `client.resources.organisation_units.get(uid)` already returns a v43 model when talking to v43.

But the **hand-written helper modules** (`dhis2w_client/{system,dashboards,maps,programs,...}.py`) all import their model classes statically from a single version:

```python
from dhis2w_client.generated.v42.oas import SystemInfo, Grid
from dhis2w_client.generated.v42.schemas import OrganisationUnit
```

73 such imports, all pinned to v42. So `client.system.info()` against a v43 instance parses with the v42 `SystemInfo` class. Most of the time this is fine — most fields are stable across versions — but it has real costs once v43 specifics matter.

## Why now

The v42 → v43 schema diff (run with `dhis2 dev codegen diff v42 v43`) shows three kinds of change. The first two are pure metadata noise. The third is the problem:

| Kind | Examples | Impact on v42-pinned helpers |
| --- | --- | --- |
| Metadata bound shifts | `description.max: 2_147_483_647 → 255`, `href.propertyType: URL → TEXT` | None — pydantic doesn't enforce these. |
| Pure additions | `Program.enableChangeLog`, `Program.enrollmentsLabel`, `TrackedEntityAttribute.blockedSearchOperators` (~20 new fields total) | Field invisible at typed-access time; lands in `model_extra` if `extra="allow"` is set. |
| Type-shape changes | `DashboardItem.user: Reference → list[User]` (rename to `users` on the wire); `TrackedEntityAttribute.favorite: bool → list[str]` (renamed `favorites`); `Section.user` removed; `Program.favorite` removed | **Pydantic refuses to parse v43 wire data with the v42 model**. Same field name, incompatible type, no graceful path. |

The third row is what forces a decision: pinning to v42 isn't free, it actively breaks for ~6 schemas the moment a caller hits a v43 instance.

## Decision

Adopt **runtime model resolution** for hand-written helpers. Helpers ask `client.generated.<Name>` instead of `from dhis2w_client.generated.v42 import Name`. The class returned is the v42 class on a v42 instance, the v43 class on a v43 instance.

This is **Option C4** from the original review's three credible designs:

- **A** (pin to v42, document) — rejected; doesn't gracefully degrade for the type-shape changes.
- **B** (separate `Dhis2Client42` / `Dhis2Client43`) — rejected; doubles the user-facing surface.
- **C4** (runtime resolution against the existing `_generated` module) — adopted. Single client, single helper module per resource, model class resolved per-instance.

### What stays the same

- Generated trees keep their per-version layout. `dhis2w_client.generated.v42.OrganisationUnit` and `dhis2w_client.generated.v43.OrganisationUnit` are still importable.
- `client.resources.X` accessors remain typed-as-v42 at the static type-check level (they're constructed by the generator off whichever tree was loaded). No change to those.
- The `extra="allow"` ConfigDict on every generated model still catches pure-addition fields silently.

### What changes

1. **`Dhis2Client.generated` becomes a public read-only property.** The underscore module attribute already exists (`self._generated: ModuleType`); just expose it. Callers — and helpers — read model classes off it.

2. **Hand-written helpers swap the static import for a runtime lookup.** The pattern flips from:

   ```python
   from dhis2w_client.generated.v42.oas import SystemInfo

   class SystemModule:
       async def info(self) -> SystemInfo:
           raw = await self._client.get_raw("/api/system/info")
           return SystemInfo.model_validate(raw)
   ```

   to:

   ```python
   from typing import TYPE_CHECKING

   if TYPE_CHECKING:
       # Static type-check sees the v42 shape — most fields are stable.
       # The v43 version is structurally compatible for everything except
       # the breaking-shape schemas listed at the bottom of this doc.
       from dhis2w_client.generated.v42.oas import SystemInfo

   class SystemModule:
       async def info(self) -> "SystemInfo":
           raw = await self._client.get_raw("/api/system/info")
           cls = self._client.generated.oas.SystemInfo  # resolved per instance
           return cls.model_validate(raw)
   ```

   At runtime: parses with the version-matching class, so `DashboardItem.user` shape mismatch goes away. At type-check time: the v42 shape remains the documented contract. We're explicit in this decision doc that **the static type lies for ~6 schemas under v43** — see the table below.

3. **A small `parse_with_generated` helper** in `dhis2w_client/_collection.py` covers the common "parse one or many of a generated class" pattern so helpers don't all open-code the `client.generated.X` lookup.

   ```python
   # _collection.py addition
   def parse_one_with(client: "Dhis2Client", path: str, raw: dict) -> Any:
       """Resolve `<class>` off the live-version `client.generated` module and validate `raw` against it.

       `path` is a dotted lookup like 'oas.SystemInfo' or 'OrganisationUnit'.
       """
       module = client.generated
       for part in path.split("."):
           module = getattr(module, part)
       return module.model_validate(raw)
   ```

4. **The breaking-shape schemas get explicit per-version branches** in the helper that touches them. Six schemas listed below; each gets a small `if client.version_key == "v43":` branch (or a typed-handler dispatch) on the divergent field. Estimated: ~4 places need this.

## Migration plan

### Phase 1 — primitive (this PR)

- `Dhis2Client.generated` public property + docstring.
- Decision doc landed (this file).
- No helper changes yet.
- v0.6.x stays SemVer-compatible.

### Phase 2 — helper sweep (separate PR per logical group)

Touch helpers in topical batches so a regression is bounded:

1. **System + System info** — single helper, low risk, tests exist. Validates the pattern.
2. **Dashboards** — has the `DashboardItem.user` breaking shape. Real test of the "branch for v43" approach.
3. **Tracker / event helpers** — touches the new `TrackerSingleEvent` / `TrackerTrackerEvent` split.
4. **TrackedEntityAttribute** — six new search-tuning fields + the breaking `favorite → favorites` rename.
5. **Program / ProgramStage / TrackedEntityType** — labels + `enableChangeLog` + `enrollmentCategoryCombo`.
6. **Map / MapView / EventChart / EventReport / EventVisualization** — pinning fields.
7. The remaining ~50 helpers — each is `s/from dhis2w_client.generated.v42/.../` + a `TYPE_CHECKING` guard.

### Phase 3 — release as v0.7.0

- Lockstep version bump 0.6.x → 0.7.0.
- Tag, publish.
- `docs/architecture/typed-schemas.md` updated to describe the runtime-resolution pattern.
- Migration note in the v0.7.0 release notes pointing at this doc.

## What this doesn't fix

- **Static type-check still shows the v42 shape on every helper return type.** Callers who write `dashboard_item.users` (the v43 wire name) will be flagged as accessing an unknown attribute. They can `cast` or use `getattr` — explicit but ugly. Documented limitation.
- **Pure-addition v43 fields stay invisible at the typed level.** `program.enableChangeLog` reads through `model_extra` until / unless we re-pin the helper return types to v43 (which we'd do at v0.8.0 if v43 becomes the typed default).

## Schemas with breaking-shape changes (the per-version branch list)

These are the ~6 places where a v42-typed model can't parse v43 wire data. Each will get an explicit branch in its helper module:

| Schema | Field | v42 type | v43 type | Helper that touches it |
| --- | --- | --- | --- | --- |
| `DashboardItem` | `user` / `users` | `Reference \| None` | `list[User]` (renamed `users` on wire) | `dashboards.py` |
| `TrackedEntityAttribute` | `favorite` / `favorites` | `bool` | `list[str]` (renamed `favorites`) | `tracked_entity_attributes.py` |
| `Program` | `favorite` / `favorites` | `list[str]` | removed entirely | `programs.py` (if it touches the field) |
| `Section` | `user` | `Reference \| None` | removed entirely | `sections.py` (if it touches the field) |
| `DashboardItem` | `code` / `id` | `IDENTIFIER` typed | `TEXT` typed | dashboards.py — same call site as above |
| `Map` | `basemaps` | absent | `list[Basemap]` | `maps.py` |

Anything else that's purely additive is invisible to v42-pinned typed access but doesn't break parsing — those callers see the field via `model_extra` or upgrade to direct `dhis2w_client.generated.v43.*` imports if they need typed access.

## Open questions

- **Do we want a `client.model_for("DashboardItem") -> type[BaseModel]` shortcut?** Would replace `client.generated.schemas.dashboard_item.DashboardItem` with a flat lookup. Nice-to-have; not required.
- **Should `_collection.parse_collection` accept a string class name and resolve through `client.generated`?** Saves the `cls = client.generated.X` step in every helper. Probably yes; folded into the Phase 2 sweep.
- **Is the `TYPE_CHECKING` import the right way to lie to the type checker?** Alternative: `# type: ignore[assignment]` on the resolved class; less clean but more honest. Open for review.
