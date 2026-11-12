#!/usr/bin/env python3
"""Offline idempotency-key binding for a synthetic PATCH-like operation."""
from copy import deepcopy
from hashlib import sha256
import json

SEED = {"doc-1": {"owner": "alice", "version": 2, "title": "Initial"}}

def fingerprint(actor, resource, expected_version, patch):
    payload = [actor, resource, expected_version, patch]
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(canonical.encode("utf-8")).hexdigest()

def patch_with_key(db, ledger, actor, resource, expected_version, patch, key):
    record = db.get(resource)
    if record is None or record["owner"] != actor:
        return False, "DENY_OWNER"
    if not isinstance(key, str) or not (8 <= len(key) <= 64) or not key.isascii():
        return False, "DENY_KEY"
    if type(expected_version) is not int or not isinstance(patch, dict):
        return False, "DENY_SHAPE"
    if set(patch) != {"title"} or not isinstance(patch["title"], str):
        return False, "DENY_FIELD"
    if not (1 <= len(patch["title"].strip()) <= 40):
        return False, "DENY_VALUE"
    binding = fingerprint(actor, resource, expected_version, patch)
    if key in ledger:
        old_binding, prior_version = ledger[key]
        if binding != old_binding:
            return False, "DENY_KEY_REUSE"
        return True, f"REPLAY_VERSION_{prior_version}"
    if record["version"] != expected_version:
        return False, "DENY_STALE"
    record["title"] = patch["title"].strip()
    record["version"] += 1
    ledger[key] = (binding, record["version"])
    return True, f"APPLIED_VERSION_{record['version']}"

def main():
    db, ledger = deepcopy(SEED), {}
    cases = [
        ("first", "alice", "doc-1", 2, {"title": "Review"}, "request-001", (True, "APPLIED_VERSION_3")),
        ("same replay", "alice", "doc-1", 2, {"title": "Review"}, "request-001", (True, "REPLAY_VERSION_3")),
        ("same key different body", "alice", "doc-1", 2, {"title": "Other"}, "request-001", (False, "DENY_KEY_REUSE")),
        ("other owner", "bob", "doc-1", 2, {"title": "Review"}, "request-001", (False, "DENY_OWNER")),
        ("stale new key", "alice", "doc-1", 2, {"title": "Late"}, "request-002", (False, "DENY_STALE")),
        ("second valid", "alice", "doc-1", 3, {"title": "Next"}, "request-002", (True, "APPLIED_VERSION_4")),
        ("second replay", "alice", "doc-1", 3, {"title": "Next"}, "request-002", (True, "REPLAY_VERSION_4")),
    ]
    for label, actor, rid, ver, body, key, expected in cases:
        actual = patch_with_key(db, ledger, actor, rid, ver, body, key)
        assert actual == expected, (label, actual)
        print(f"{label:23} {actual[1]}")
    assert db["doc-1"] == {"owner": "alice", "version": 4, "title": "Next"}
    assert len(ledger) == 2
    print("7/7 replay checks passed; atomic storage is not modeled.")

if __name__ == "__main__":
    main()
