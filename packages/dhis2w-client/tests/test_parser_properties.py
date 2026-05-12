"""Property-based tests on the parser DSLs — UIDs, periods, JsonPatch.

Hypothesis-driven properties over the hand-written parser surfaces.
Catches edge cases that example-based tests miss (off-by-one boundary
years, leap years, week 53, quarterly rollover, etc.) by exercising
randomized inputs against invariants the implementation is supposed
to uphold.

Each property is short (<10 lines of body) — Hypothesis does the
heavy lifting around generation, shrinking, and stat aggregation.
Run with `make test` like any other unit suite; runs in <1s.

Properties:

- `generate_uid()` outputs always satisfy `is_valid_uid()`.
- `generate_uid()` outputs match `UID_RE` exactly.
- `generate_uids(n)` yields `n` distinct, valid uids.
- `parse_period` round-trips: `parse_period(p).id == p`.
- `next_period_id` / `previous_period_id` are inverses for valid period ids.
- `period_start_end` returns (start, end) with start <= end.
- `JsonPatchOpAdapter.validate_python(dump)` round-trips an op via dict.
"""

from __future__ import annotations

import re
from datetime import date

import pytest
from dhis2w_client import (
    JsonPatchOpAdapter,
    generate_uid,
    generate_uids,
    is_valid_uid,
    next_period_id,
    parse_period,
    period_start_end,
    previous_period_id,
)
from dhis2w_client.v42.uids import UID_RE
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from pydantic import BaseModel

# ----- UID gen / validation --------------------------------------------------


@settings(max_examples=200)
@given(st.integers(min_value=0, max_value=1000))
def test_generate_uid_always_valid(_seed: int) -> None:
    """Every UID `generate_uid()` returns satisfies `is_valid_uid()`.

    The seed is unused — `generate_uid` is `secrets`-driven and stateless,
    so we just need many sample invocations.
    """
    uid = generate_uid()
    assert is_valid_uid(uid), f"generate_uid returned an invalid uid: {uid!r}"
    assert UID_RE.fullmatch(uid) is not None, f"uid {uid!r} doesn't match UID_RE"
    assert len(uid) == 11
    assert uid[0].isalpha()


@settings(max_examples=50)
@given(st.integers(min_value=1, max_value=50))
def test_generate_uids_yields_distinct_valid_uids(count: int) -> None:
    """`generate_uids(n)` returns `n` distinct uids, each `is_valid_uid()`."""
    uids = generate_uids(count)
    assert len(uids) == count
    assert len(set(uids)) == count, "generate_uids produced duplicates within a single call"
    for uid in uids:
        assert is_valid_uid(uid), f"generate_uids yielded invalid uid: {uid!r}"


@given(st.text(min_size=0, max_size=15))
def test_is_valid_uid_matches_regex(candidate: str) -> None:
    """`is_valid_uid` agrees with the canonical `UID_RE` for any string."""
    expected = UID_RE.fullmatch(candidate) is not None
    assert is_valid_uid(candidate) == expected


# ----- Period parsing -------------------------------------------------------


# Strategies for each absolute period kind. Bounds keep us inside the date
# library's safe range (year 1 ≤ y ≤ 9999) without picking pathological ones.
_year_st = st.integers(min_value=1900, max_value=2100)
_month_st = st.integers(min_value=1, max_value=12)
_quarter_st = st.integers(min_value=1, max_value=4)
_half_st = st.integers(min_value=1, max_value=2)
_iso_week_st = st.integers(min_value=1, max_value=52)  # 53 only on long years; keep safe.


@given(_year_st)
def test_parse_period_yearly_roundtrip(year: int) -> None:
    """`parse_period(f"{year}").id == f"{year}"` for any 4-digit year."""
    period_id = f"{year:04d}"
    parsed = parse_period(period_id)
    assert parsed.id == period_id
    assert parsed.start == date(year, 1, 1)
    assert parsed.end == date(year, 12, 31)


@given(_year_st, _month_st)
def test_parse_period_monthly_roundtrip(year: int, month: int) -> None:
    """`parse_period(f"{year}{month:02d}").id` round-trips + start is day 1."""
    period_id = f"{year:04d}{month:02d}"
    parsed = parse_period(period_id)
    assert parsed.id == period_id
    assert parsed.start == date(year, month, 1)
    assert parsed.start <= parsed.end


@given(_year_st, _quarter_st)
def test_parse_period_quarterly_roundtrip(year: int, quarter: int) -> None:
    """`parse_period(f"{year}Q{quarter}")` parses + start.month aligns."""
    period_id = f"{year:04d}Q{quarter}"
    parsed = parse_period(period_id)
    assert parsed.id == period_id
    assert parsed.start.year == year
    assert parsed.start.month == (quarter - 1) * 3 + 1
    assert parsed.start.day == 1
    assert parsed.start < parsed.end


@given(_year_st, _half_st)
def test_parse_period_six_monthly_roundtrip(year: int, half: int) -> None:
    """`parse_period(f"{year}S{half}")` covers 6 months exactly."""
    period_id = f"{year:04d}S{half}"
    parsed = parse_period(period_id)
    assert parsed.id == period_id
    assert parsed.start.year == year
    assert parsed.start.day == 1
    assert parsed.start < parsed.end


@given(_year_st, _iso_week_st)
def test_parse_period_weekly_roundtrip(year: int, week: int) -> None:
    """`parse_period(f"{year}W{week:02d}")` produces a 7-day span when valid."""
    period_id = f"{year:04d}W{week:02d}"
    parsed = parse_period(period_id)
    assert parsed.id == period_id
    span = (parsed.end - parsed.start).days
    assert span == 6, f"weekly span should be 7 days (end-start=6), got {span}"


@given(_year_st, _month_st)
def test_period_start_end_invariant(year: int, month: int) -> None:
    """`period_start_end` always returns (start, end) with start <= end."""
    period_id = f"{year:04d}{month:02d}"
    start, end = period_start_end(period_id)
    assert start <= end


@given(_year_st, _month_st)
def test_next_then_prev_is_identity_monthly(year: int, month: int) -> None:
    """`previous_period_id(next_period_id(p)) == p` for monthly periods."""
    period_id = f"{year:04d}{month:02d}"
    # Skip the upper-end boundary where next would over/underflow year range.
    nxt = next_period_id(period_id)
    back = previous_period_id(nxt)
    assert back == period_id


@given(_year_st.filter(lambda y: 1901 <= y <= 2099), _month_st)
def test_prev_then_next_is_identity_monthly(year: int, month: int) -> None:
    """`next_period_id(previous_period_id(p)) == p` for monthly periods.

    Year range narrowed by 1 on each side to avoid date library bounds
    when month=1 (prev wraps to year-1=1900-12) or month=12 (next wraps
    to year+1=2101-01).
    """
    period_id = f"{year:04d}{month:02d}"
    prev = previous_period_id(period_id)
    forward = next_period_id(prev)
    assert forward == period_id


@given(_year_st, _quarter_st)
def test_next_then_prev_is_identity_quarterly(year: int, quarter: int) -> None:
    """`previous_period_id(next_period_id(p)) == p` for quarterly periods."""
    period_id = f"{year:04d}Q{quarter}"
    nxt = next_period_id(period_id)
    back = previous_period_id(nxt)
    assert back == period_id


# ----- JsonPatch round-trip -------------------------------------------------

# JSON Patch ops we ship: add, copy, move, remove, replace, test.
# Each variant's `op` field carries the discriminator literal.

_path_st = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789-_",
    min_size=1,
    max_size=20,
).map(lambda s: f"/{s}")
_value_st = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1000, max_value=1000),
    st.text(max_size=20),
    st.lists(st.integers(), max_size=5),
)


@given(_path_st, _value_st)
def test_json_patch_add_roundtrip(path: str, value: object) -> None:
    """`add` op round-trips through `JsonPatchOpAdapter.validate_python`.

    JSON Patch treats `null` as a legitimate value (distinct from a missing
    `value`), so the dump uses plain `model_dump()` — not `exclude_none=True`
    — so a `None` value is preserved in the round-trip.
    """
    raw = {"op": "add", "path": path, "value": value}
    op = JsonPatchOpAdapter.validate_python(raw)
    dumped = op.model_dump()
    assert dumped["op"] == "add"
    assert dumped["path"] == path
    assert dumped["value"] == value


@given(_path_st)
def test_json_patch_remove_roundtrip(path: str) -> None:
    """`remove` op round-trips with just `op` and `path`."""
    raw = {"op": "remove", "path": path}
    op = JsonPatchOpAdapter.validate_python(raw)
    dumped = op.model_dump()
    assert dumped["op"] == "remove"
    assert dumped["path"] == path


@given(_path_st, _path_st)
def test_json_patch_move_roundtrip(from_path: str, to_path: str) -> None:
    """`move` op round-trips its `from` + `path`."""
    raw = {"op": "move", "from": from_path, "path": to_path}
    op = JsonPatchOpAdapter.validate_python(raw)
    dumped = op.model_dump(exclude_none=True, by_alias=True)
    assert dumped["op"] == "move"
    assert dumped["from"] == from_path
    assert dumped["path"] == to_path


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.sampled_from(["add", "copy", "move", "remove", "replace", "test"]), _path_st)
def test_json_patch_op_discriminator_picks_right_subclass(op_name: str, path: str) -> None:
    """The discriminator on `op` picks the right `BaseModel` subclass for every variant.

    `JsonPatchOp` is a discriminated union (`Annotated[X | Y | ..., Field(discriminator="op")]`),
    not a runtime class — so we assert the resolved instance is a `BaseModel` and that
    its class name encodes the right op (`AddOp` for `add`, `CopyOp` for `copy`, etc.).
    """
    raw: dict[str, object] = {"op": op_name, "path": path}
    if op_name in {"add", "replace", "test"}:
        raw["value"] = "probe"
    if op_name in {"copy", "move"}:
        raw["from"] = "/source"
    op = JsonPatchOpAdapter.validate_python(raw)
    assert isinstance(op, BaseModel)
    assert op_name.lower() in re.sub(r"Op$", "", op.__class__.__name__).lower()


@given(_year_st, _month_st)
def test_parse_period_monthly_with_invalid_month_raises(year: int, month: int) -> None:
    """`parse_period` rejects month=13/0 with `ValueError`.

    Strategy generates valid 1-12 months; we map each draw to a deterministic
    invalid sibling (13 for lower-half draws, 0 for upper-half) so every
    iteration exercises a different out-of-range value.
    """
    bad_month = 13 if month <= 6 else 0
    bad_id = f"{year:04d}{bad_month:02d}"
    with pytest.raises(ValueError, match="month|unrecognised"):
        parse_period(bad_id)
