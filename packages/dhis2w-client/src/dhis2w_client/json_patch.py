"""Typed RFC 6902 JSON Patch operations — reusable across every DHIS2 PATCH endpoint.

DHIS2 accepts JSON Patch bodies on `PATCH /api/<resource>/{id}` across most
metadata types (routes, users, data elements, ...). Each op is a distinct
pydantic class tagged by the `op` field; the discriminated Union makes
pydantic route incoming dicts to the right variant and reject wrong-shape
bodies at construction time.

Variant shapes (per RFC 6902):

    add      {op, path, value}           insert / overlay at path
    remove   {op, path}                  delete at path
    replace  {op, path, value}           overwrite at path with value
    test     {op, path, value}           assert equality; aborts on mismatch
    move     {op, path, from}            move value from -> path
    copy     {op, path, from}            copy value from -> path

`from` is a Python reserved word, so it's aliased to the `from_` attribute.
`JsonPatchOpAdapter.validate_python(raw)` picks the right variant from a
dict; `op.model_dump(by_alias=True)` serialises back to the wire shape.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class _JsonPatchBase(BaseModel):
    """Shared config for every RFC 6902 op — `extra="forbid"` so typos fail fast."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    path: str


class AddOp(_JsonPatchBase):
    """RFC 6902 `add` — insert `value` at `path` (or replace existing on overlap)."""

    op: Literal["add"] = "add"
    value: Any


class RemoveOp(_JsonPatchBase):
    """RFC 6902 `remove` — delete the value at `path`."""

    op: Literal["remove"] = "remove"


class ReplaceOp(_JsonPatchBase):
    """RFC 6902 `replace` — overwrite the value at `path` with `value`."""

    op: Literal["replace"] = "replace"
    value: Any


class TestOp(_JsonPatchBase):
    """RFC 6902 `test` — assert the value at `path` equals `value` (aborts the patch on mismatch)."""

    # Tell pytest this isn't a test class (naming collision with the Test* convention).
    __test__ = False

    op: Literal["test"] = "test"
    value: Any


class MoveOp(_JsonPatchBase):
    """RFC 6902 `move` — move the value at `from_` to `path`. Serialises `from_` as `from` on the wire."""

    op: Literal["move"] = "move"
    from_: str = Field(alias="from")


class CopyOp(_JsonPatchBase):
    """RFC 6902 `copy` — copy the value at `from_` to `path`. Serialises `from_` as `from` on the wire."""

    op: Literal["copy"] = "copy"
    from_: str = Field(alias="from")


JsonPatchOp = Annotated[
    AddOp | RemoveOp | ReplaceOp | TestOp | MoveOp | CopyOp,
    Field(discriminator="op"),
]
"""Discriminated union over the six RFC 6902 ops. Validates `{op, path, value?, from?}` per op shape."""


JsonPatchOpAdapter: TypeAdapter[JsonPatchOp] = TypeAdapter(JsonPatchOp)
"""Helper: `JsonPatchOpAdapter.validate_python(dict)` picks the right op subclass by `op`."""


__all__ = [
    "AddOp",
    "CopyOp",
    "JsonPatchOp",
    "JsonPatchOpAdapter",
    "MoveOp",
    "RemoveOp",
    "ReplaceOp",
    "TestOp",
]
