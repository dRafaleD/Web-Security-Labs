#!/usr/bin/env python3
"""Single-process teaching model for pending and committed idempotency entries."""
from hashlib import sha256
from json import dumps

RESOURCE = {"owner": "alice", "version": 2, "value": "initial"}
LEDGER = {}

def digest(version: int, value: str) -> str:
    raw = dumps([version, value], separators=(",", ":"), ensure_ascii=True)
    return sha256(raw.encode("utf-8")).hexdigest()

def begin(actor: str, key: str, expected_version: int, value: str) -> str:
    if actor != RESOURCE["owner"]:
        return "UNAUTHORIZED"
    if not isinstance(key, str) or len(key) < 8:
        return "BAD_KEY"
    if type(expected_version) is not int or not isinstance(value, str) or not value:
        return "BAD_REQUEST"
    fp = digest(expected_version, value)
    scope = (actor, key)
    previous = LEDGER.get(scope)
    if previous:
        if previous["fingerprint"] != fp:
            return "KEY_CONFLICT"
        return "IN_PROGRESS" if previous["status"] == "PENDING" else "REPLAY"
    if RESOURCE["version"] != expected_version:
        return "STALE_VERSION"
    LEDGER[scope] = {
        "status": "PENDING", "fingerprint": fp,
        "version": expected_version, "value": value,
    }
    return "PENDING"

def finish(actor: str, key: str) -> str:
    entry = LEDGER.get((actor, key))
    if not entry or entry["status"] != "PENDING":
        return "NO_PENDING"
    if RESOURCE["version"] != entry["version"]:
        del LEDGER[(actor, key)]
        return "STALE_CANCELLED"
    # One indivisible action only inside this deterministic local model.
    RESOURCE["value"] = entry["value"]
    RESOURCE["version"] += 1
    entry["status"] = "COMMITTED"
    return "COMMITTED"

def abort(actor: str, key: str) -> str:
    entry = LEDGER.get((actor, key))
    if not entry or entry["status"] != "PENDING":
        return "NO_PENDING"
    del LEDGER[(actor, key)]
    return "ABORTED"

def main():
    cases = [
        ("initial", lambda: begin("alice", "request-001", 2, "first"), "PENDING"),
        ("parallel retry", lambda: begin("alice", "request-001", 2, "first"), "IN_PROGRESS"),
        ("changed body", lambda: begin("alice", "request-001", 2, "changed"), "KEY_CONFLICT"),
        ("commit", lambda: finish("alice", "request-001"), "COMMITTED"),
        ("replay", lambda: begin("alice", "request-001", 2, "first"), "REPLAY"),
        ("old version", lambda: begin("alice", "request-002", 2, "second"), "STALE_VERSION"),
        ("new pending", lambda: begin("alice", "request-002", 3, "second"), "PENDING"),
        ("aborted", lambda: abort("alice", "request-002"), "ABORTED"),
        ("retry after abort", lambda: begin("alice", "request-002", 3, "second"), "PENDING"),
        ("second commit", lambda: finish("alice", "request-002"), "COMMITTED"),
        ("other owner", lambda: begin("bob", "request-003", 4, "bad"), "UNAUTHORIZED"),
    ]
    for label, action, expected in cases:
        actual = action()
        assert actual == expected, (label, actual)
        print(f"{label:22} {actual}")
    assert RESOURCE == {"owner": "alice", "version": 4, "value": "second"}
    print("12/12 deterministic state assertions passed; no real concurrency")

if __name__ == "__main__":
    main()
