#!/usr/bin/env python3
"""Deterministic two-request race; models an atomic commit but does not implement a DB."""
from hashlib import sha256

DOC = {"owner": "alice", "version": 2, "value": "before"}
LEDGER = {}  # (actor, key) -> (fingerprint, applied_version)

def fingerprint(value: str, expected_version: int) -> str:
    return sha256(f"{expected_version}:{len(value)}:{value}".encode()).hexdigest()

def commit(actor: str, key: str, expected_version: int, value: str) -> str:
    if actor != DOC["owner"]:
        return "UNAUTHORIZED"
    if not isinstance(key, str) or len(key) < 8:
        return "INVALID_KEY"
    if type(expected_version) is not int or not isinstance(value, str) or not value:
        return "INVALID"
    fp = fingerprint(value, expected_version)
    ledger_key = (actor, key)
    if ledger_key in LEDGER:
        old_fp, _ = LEDGER[ledger_key]
        return "REPLAY" if old_fp == fp else "KEY_CONFLICT"
    # Model a single, indivisible DB transaction: compare-and-swap + ledger insert.
    if DOC["version"] != expected_version:
        return "STALE"
    DOC["value"] = value
    DOC["version"] += 1
    LEDGER[ledger_key] = (fp, DOC["version"])
    return "APPLIED"

def main() -> None:
    passed = 0
    def check(actual: str, expected: str):
        nonlocal passed
        assert actual == expected, (actual, expected)
        passed += 1

    # Clients A and B both read version 2 before either submits.
    snapshot_a = snapshot_b = DOC["version"]
    check(commit("alice", "operation-a", snapshot_a, "first"), "APPLIED")
    check(commit("alice", "operation-b", snapshot_b, "second"), "STALE")
    check(commit("alice", "operation-a", snapshot_a, "first"), "REPLAY")
    check(commit("alice", "operation-a", snapshot_a, "modified"), "KEY_CONFLICT")
    check(commit("bob", "operation-a", snapshot_a, "first"), "UNAUTHORIZED")
    check(commit("alice", "operation-c", 3, "third"), "APPLIED")
    check(commit("alice", "operation-c", 3, "third"), "REPLAY")
    assert DOC == {"owner": "alice", "version": 4, "value": "third"}
    assert len(LEDGER) == 2
    passed += 2
    print(f"{passed}/{passed} deterministic race assertions passed")

if __name__ == "__main__":
    main()
