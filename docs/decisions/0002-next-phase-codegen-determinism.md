# 0002 — Next phase: codegen determinism + golden-snapshot lock

**Status:** Proposed.
**Target release:** v0.8.0 (or a v0.7.x patch series followed by the bump on the snapshot test going green in CI).

## Context

After v0.7.0 the workspace is in a settled state:

- v42 + v43 are the only supported majors; the generated tree is two trees, not five.
- Both versions seed cleanly under `make refresh-and-verify`; the v42 verify-examples score is 161/0/11 and v43 is 154/7/11 (the 7 fails are deferred non-wire-shape items).
- The multi-version e2e CI matrix runs nightly.
- The `categorys → categories` and `rawPeriods` wire-shape fixes mean callers writing maps / visualizations / category combos work on both versions.

What hasn't been fixed yet, and shows up every time we run codegen:

- **Codegen emitter is non-deterministic.** Running `dhis2 dev codegen rebuild` against a committed manifest produces a tree that diffs against itself on the next rebuild. The diffs are pure noise (field reordering, whitespace, ordering of dict / set iteration). Memory note `project_codegen_flaky.md` records: *"oas-rebuild produces ~1100-file noisy drift on every rerun; safe to revert if user did not run codegen on purpose."*
- This noise pollutes every contributor's working tree the moment they run `make refresh-and-verify` (which calls `dev_codegen.sh` which calls `rebuild`). It makes diffs unreviewable, hides real codegen drift, and means the only way to verify "did I actually change anything" is to revert + redo + diff manually.
- It also blocks the testing-roadmap A5 entry — *"load committed `schemas_manifest.json`; run `emit()` into a tmp dir; diff against committed `generated/v{N}/`; fail on any diff"* — because the diff is never empty.

## Decision

Two-PR sequence, in order:

1. **Determinize the codegen emitter.** Find every source of non-determinism and lock the iteration order. After this PR, `dhis2 dev codegen rebuild` from a clean tree should produce zero diffs; running it twice in a row should produce zero diffs.

2. **Add A5 (codegen golden-snapshot test).** A pytest module under `packages/dhis2w-codegen/tests/test_snapshots.py` that loads each committed manifest, runs `emit()` into a `tmp_path`, walks both trees, and asserts byte-for-byte equality. CI fails when the codegen output drifts from the committed tree; intentional codegen changes need to update the snapshot in the same PR.

The order matters: A5 is only useful once the emitter is deterministic. A deterministic emitter without A5 is worth shipping on its own — it stops the working-tree pollution today.

## Phase 1 — determinism (1 PR)

### Where to look

The emitter lives in `packages/dhis2w-codegen/src/dhis2w_codegen/`. Suspected sources of non-determinism:

- **`dict` and `set` iteration.** Python's dict insertion order is stable since 3.7, but `set` iteration is hash-randomised across processes. Any place the emitter iterates a `set` produces different output across runs.
- **JSON-loading the manifest.** `json.load` returns dicts; iteration order matches insertion order which matches the file. Should be deterministic if the manifest itself is sorted.
- **Schema → class name mapping.** If the emitter walks `manifest["schemas"]` and produces output keyed by class name, the output ordering is whatever the manifest is.
- **Cross-class references.** When emitting `class Foo` that references `Bar`, the emitter might collect `Bar` into a set of imports — that set iteration is non-deterministic.
- **Jinja templates.** Templates iterate their inputs; if the input is a `set`, the output is non-deterministic.
- **OAS-side emitter.** `oas_emit.py` does the same kind of work for `/api/openapi.json`. Memory note specifically calls out OAS-side; both probably share the bug.

### Strategy

1. Reproduce the bug deterministically: `dhis2 dev codegen rebuild`, save the tree, `dhis2 dev codegen rebuild` again, diff. Run in two fresh Python processes (different `PYTHONHASHSEED` => different `set` iteration).
2. Use `git diff --stat` to identify which files diff. For each diffing file, scan the emitter logic that produces it.
3. Replace every `set(...)` literal in emit paths with `sorted(...)` or a `list` constructed in deterministic order. Replace `frozenset` similarly. `dict()` should already be insertion-ordered — but `dict.update(other_dict)` from a non-deterministic source spreads the bug.
4. After each change, re-run the rebuild-twice-and-diff loop until it's empty.
5. Add a simple regression test in `packages/dhis2w-codegen/tests/test_determinism.py`: emit twice, assert equal.

### Estimated cost

A few hours of investigation + a few `sorted()` calls. The hardest part is finding every source. If a single `set` is the culprit, this is a tiny PR. If it's pervasive, more like half a day.

## Phase 2 — A5 golden-snapshot test (1 PR)

### Shape

```python
# packages/dhis2w-codegen/tests/test_snapshots.py

from pathlib import Path
import json
import pytest
from dhis2w_codegen.emit import emit
from dhis2w_codegen.oas_emit import oas_emit

REPO_ROOT = Path(__file__).resolve().parents[3]
GENERATED_ROOT = REPO_ROOT / "packages/dhis2w-client/src/dhis2w_client/generated"


@pytest.mark.parametrize("version_key", ["v42", "v43"])
def test_schemas_emit_matches_committed_tree(version_key: str, tmp_path: Path) -> None:
    """`emit()` from the committed manifest must reproduce the committed tree byte-for-byte."""
    manifest_path = GENERATED_ROOT / version_key / "schemas_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    emit(manifest, tmp_path / version_key)
    _assert_trees_equal(tmp_path / version_key, GENERATED_ROOT / version_key, scope="schemas")


@pytest.mark.parametrize("version_key", ["v42", "v43"])
def test_oas_emit_matches_committed_tree(version_key: str, tmp_path: Path) -> None:
    """Same idea for the OAS-side tree."""
    openapi_path = GENERATED_ROOT / version_key / "openapi.json"  # or wherever it sits
    spec = json.loads(openapi_path.read_text())
    oas_emit(spec, tmp_path / version_key / "oas")
    _assert_trees_equal(tmp_path / version_key / "oas", GENERATED_ROOT / version_key / "oas")


def _assert_trees_equal(generated: Path, committed: Path, scope: str = "") -> None:
    """Walk both trees, assert every file matches byte-for-byte."""
    ...
```

### Failure mode

When CI fails the snapshot test, the diff between `tmp_path` and the committed tree pinpoints exactly which file drifted and how. The fix is either:

- Update the committed tree (intentional codegen change — `make dhis2-codegen-all` then commit).
- Fix the emitter (unintentional drift — investigate, restore determinism, no committed-tree change).

The PR that updates committed-tree contents should always run through the snapshot test; if the snapshot is updated in the same PR as the change that produced it, the test stays green.

### Estimated cost

~50 lines of test, two parameterised cases per emitter (schemas + OAS), ×2 versions = ~4 test runs. Adds maybe 5-10 seconds to `make test`. Trivial once Phase 1 is in.

## What this unlocks

- **Reviewable codegen diffs.** Running codegen no longer pollutes the tree with hundreds of bytes-only diffs.
- **CI catches accidental emitter changes.** A `dhis2w-codegen` refactor that silently changes 200 files now fails the snapshot test loudly.
- **`make refresh-and-verify` stays clean.** The `dev_codegen.sh` example currently dirties the tree on every run; that goes away.
- **Future codegen work is safer.** Anyone touching `emit.py` / `oas_emit.py` / templates sees the snapshot diff immediately, no human spot-checking.

## Out of scope

- Refactoring the codegen emitter for clarity / speed. Determinism only.
- Changing the on-disk format of generated code. The current shape is what it is; we're locking it.
- Pre-1.0 SemVer concerns. Determinism is purely an internal-quality fix; no caller-visible behavior change.
- Any v44+ work. Per the v0.7.x scope: v42 + v43 only.

## Verification

- `dhis2 dev codegen rebuild` from a clean main produces zero `git status` output.
- Running it again still produces zero output.
- Running with a different `PYTHONHASHSEED` still produces zero output.
- `pytest packages/dhis2w-codegen/tests/test_snapshots.py` passes on every committed version.
- `make refresh-and-verify` no longer leaves the working tree dirty after the run.
