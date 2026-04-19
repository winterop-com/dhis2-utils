"""Unit tests for the client-side DHIS2 UID generator."""

from __future__ import annotations

import re

import pytest
from dhis2_client import UID_ALPHABET, UID_LENGTH, UID_LETTERS, UID_RE, generate_uid, generate_uids, is_valid_uid


def test_constants_match_upstream_dhis2_core_codegenerator() -> None:
    """Alphabet + length + first-char constraint match dhis2-core/CodeGenerator.java."""
    assert UID_LENGTH == 11
    assert UID_LETTERS == "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    assert len(UID_LETTERS) == 52
    assert UID_ALPHABET == "0123456789" + UID_LETTERS
    assert len(UID_ALPHABET) == 62


def test_regex_is_canonical() -> None:
    """The regex is the exact form DHIS2 validates against on the server."""
    assert UID_RE.pattern == r"^[A-Za-z][A-Za-z0-9]{10}$"


def test_generate_uid_structure() -> None:
    """One generated UID is 11 chars, starts with a letter, every char is in the alphabet."""
    uid = generate_uid()
    assert len(uid) == UID_LENGTH
    assert uid[0] in UID_LETTERS
    assert all(char in UID_ALPHABET for char in uid)
    assert UID_RE.match(uid) is not None


def test_generate_uid_is_not_constant() -> None:
    """Successive calls produce different UIDs (collision is vanishingly rare)."""
    assert generate_uid() != generate_uid()


def test_generate_uids_returns_list_of_length_count() -> None:
    uids = generate_uids(100)
    assert len(uids) == 100
    assert all(UID_RE.match(uid) for uid in uids)
    # No collisions in a sample of 100 (62^10 * 52 keyspace — effectively impossible).
    assert len(set(uids)) == 100


def test_generate_uids_zero_returns_empty_list() -> None:
    assert generate_uids(0) == []


def test_generate_uids_negative_raises() -> None:
    with pytest.raises(ValueError, match="count must be >= 0"):
        generate_uids(-1)


def test_is_valid_uid_accepts_real_uids() -> None:
    """Real-looking DHIS2 UIDs validate."""
    assert is_valid_uid("DEancVisit1")
    assert is_valid_uid("NORNorway01")
    assert is_valid_uid("abc12345678")
    assert is_valid_uid("Aa1Bb2Cc3Dd")


def test_is_valid_uid_rejects_bad_candidates() -> None:
    """Length violations, leading digits, and stray punctuation all fail."""
    assert not is_valid_uid("")
    assert not is_valid_uid("short")
    assert not is_valid_uid("way-too-long-uid-value")
    assert not is_valid_uid("0ancVisit11")  # leading digit
    assert not is_valid_uid("ancVisit-11")  # hyphen
    assert not is_valid_uid("ancVisit 11")  # space


def test_distribution_is_reasonable() -> None:
    """Over 1000 UIDs, every alphabet character should appear somewhere.

    Smoke test for `secrets.choice` feeding the generator — if we accidentally
    seeded with a low-entropy RNG we'd see visibly skewed character counts.
    """
    sample = "".join(generate_uids(1000))
    # Every char in the 62-alphabet should appear at least once in ~11000 draws.
    missing = {char for char in UID_ALPHABET if char not in sample}
    assert not missing, f"alphabet characters never appeared in 11000 draws: {missing}"


def test_uids_exported_from_top_level() -> None:
    """Top-level `from dhis2_client import generate_uid` stays stable."""
    import dhis2_client

    assert dhis2_client.generate_uid is generate_uid
    assert dhis2_client.is_valid_uid is is_valid_uid
    assert dhis2_client.UID_LENGTH == 11


def test_generated_sample_matches_regex_repeatedly() -> None:
    """Stress test — 500 generated UIDs all match the canonical regex."""
    pattern = re.compile(UID_RE.pattern)
    for uid in generate_uids(500):
        assert pattern.match(uid), f"generated UID {uid!r} failed the regex"
