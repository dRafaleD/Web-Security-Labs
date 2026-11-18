#!/usr/bin/env python3
"""Offline canonical fingerprints and scoped idempotency keys."""
from hashlib import sha256
import json

DB = {
    "doc-a": {"owner": "alice", "version": 1, "name": "Original", "active": False},
    "doc-b": {"owner": "bob", "version": 5, "name": "Other", "active": True},
}
LEDGER = {}  # (actor, resource, key) -> (request_fingerprint, outcome)

def fingerprint(actor: str, resource: str, version: int, patch: dict) -> str:
    envelope = [actor, resource, version, patch]
    raw = json.dumps(envelope, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False)
    return sha256(raw.encode("utf-8")).hexdigest()

def apply(actor: str, resource: str, version: int, patch: dict, key: str) -> str:
    record = DB.get(resource)
    if not record or record["owner"] != actor:
        return "DENY_SCOPE"
    if type(version) is not int or not isinstance(key, str) or len(key) < 8:
        return "INVALID_REQUEST"
    if not isinstance(patch, dict) or not patch or not set(patch).issubset({"name", "active"}):
        return "INVALID_REQUEST"
    if "name" in patch and (not isinstance(patch["name"], str) or
                            not 1 <= len(patch["name"]) <= 40):
        return "INVALID_REQUEST"
    if "active" in patch and type(patch["active"]) is not bool:
        return "INVALID_REQUEST"
    fp = fingerprint(actor, resource, version, patch)
    ledger_key = (actor, resource, key)
    if ledger_key in LEDGER:
        old_fp, outcome = LEDGER[ledger_key]
        return "REPLAY" if old_fp == fp else "KEY_CONFLICT"
    if record["version"] != version:
        return "STALE_VERSION"
    record.update(patch)
    record["version"] += 1
    LEDGER[ledger_key] = (fp, record["version"])
    return "APPLIED"

def main():
    cases = [
        ("first", ("alice", "doc-a", 1, {"name": "Review", "active": True}, "request-01"), "APPLIED"),
        ("same body reordered", ("alice", "doc-a", 1, {"active": True, "name": "Review"}, "request-01"), "REPLAY"),
        ("changed value", ("alice", "doc-a", 1, {"name": "Changed", "active": True}, "request-01"), "KEY_CONFLICT"),
        ("wrong owner", ("bob", "doc-a", 1, {"name": "Review"}, "request-01"), "DENY_SCOPE"),
        ("cross resource", ("alice", "doc-b", 5, {"active": True}, "request-01"), "DENY_SCOPE"),
        ("unknown field", ("alice", "doc-a", 2, {"role": "admin"}, "request-02"), "INVALID_REQUEST"),
        ("bool as version", ("alice", "doc-a", True, {"active": False}, "request-02"), "INVALID_REQUEST"),
        ("stale with new key", ("alice", "doc-a", 1, {"active": False}, "request-02"), "STALE_VERSION"),
        ("new operation", ("alice", "doc-a", 2, {"active": False}, "request-02"), "APPLIED"),
    ]
    for name, args, expected in cases:
        got = apply(*args)
        assert got == expected, (name, got)
        print(f"{name:24} {got}")
    assert DB["doc-a"] == {"owner": "alice", "version": 3, "name": "Review", "active": False}
    assert len(LEDGER) == 2
    print("11/11 canonical request and scope assertions passed")

if __name__ == "__main__":
    main()
