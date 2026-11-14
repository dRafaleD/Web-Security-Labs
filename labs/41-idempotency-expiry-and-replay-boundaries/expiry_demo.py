#!/usr/bin/env python3
"""Synthetic idempotency expiration: durable state + optimistic version check."""
from hashlib import sha256
from json import dumps

STATE = {"version": 4, "value": "old"}
LEDGER = {}
TTL = 30

def fingerprint(actor, value, expected_version):
    raw = dumps([actor, value, expected_version], separators=(",", ":"))
    return sha256(raw.encode()).hexdigest()

def update(actor, value, version, key, now):
    if actor != "alice" or not (8 <= len(key) <= 64):
        return "DENIED"
    if not isinstance(value, str) or not (1 <= len(value) <= 30):
        return "INVALID"
    if type(version) is not int or type(now) is not int:
        return "INVALID"
    signature = fingerprint(actor, value, version)
    entry = LEDGER.get((actor, key))
    if entry and now < entry["expires_at"]:
        return "REPLAY" if entry["fingerprint"] == signature else "KEY_CONFLICT"
    if entry:
        del LEDGER[(actor, key)]
    if STATE["version"] != version:
        return "STALE_VERSION"
    STATE["value"] = value
    STATE["version"] += 1
    LEDGER[(actor, key)] = {
        "fingerprint": signature, "expires_at": now + TTL
    }
    return "APPLIED"

def main():
    assert update("alice", "v1", 4, "request-01", 100) == "APPLIED"
    assert update("alice", "v1", 4, "request-01", 110) == "REPLAY"
    assert update("alice", "bad", 4, "request-01", 110) == "KEY_CONFLICT"
    assert update("bob", "v1", 4, "request-01", 110) == "DENIED"
    assert update("alice", "v1", 4, "request-01", 130) == "STALE_VERSION"
    assert update("alice", "v2", 5, "request-02", 131) == "APPLIED"
    assert update("alice", "v2", 5, "request-02", 161) == "STALE_VERSION"
    assert STATE == {"version": 6, "value": "v2"}
    print("8/8 expiry, replay and version checks passed")

if __name__ == "__main__":
    main()
