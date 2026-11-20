#!/usr/bin/env python3
"""Offline request validation: reject oversized/deep JSON before idempotency state."""
from hashlib import sha256
import json

MAX_BYTES = 160
MAX_DEPTH = 3
LEDGER = {}
DOCUMENT = {"owner": "alice", "version": 1, "label": "old"}

def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError("duplicate key")
        result[k] = v
    return result

def depth(value):
    if isinstance(value, dict):
        return 1 + max((depth(x) for x in value.values()), default=0)
    if isinstance(value, list):
        return 1 + max((depth(x) for x in value), default=0)
    return 0

def handle(actor, body):
    if actor != DOCUMENT["owner"]:
        return "DENY_SCOPE"
    if not isinstance(body, str) or len(body.encode("utf-8")) > MAX_BYTES:
        return "TOO_LARGE"
    try:
        request = json.loads(body, object_pairs_hook=unique_pairs,
                             parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    except (ValueError, TypeError):
        return "INVALID_JSON"
    if depth(request) > MAX_DEPTH:
        return "TOO_DEEP"
    if not isinstance(request, dict) or set(request) != {"key", "version", "patch"}:
        return "INVALID_REQUEST"
    key, version, patch = request["key"], request["version"], request["patch"]
    if not isinstance(key, str) or not 8 <= len(key) <= 40 or type(version) is not int:
        return "INVALID_REQUEST"
    if not isinstance(patch, dict) or set(patch) != {"label"}:
        return "INVALID_REQUEST"
    if not isinstance(patch["label"], str) or not 1 <= len(patch["label"]) <= 30:
        return "INVALID_REQUEST"
    canonical = json.dumps([actor, version, patch], sort_keys=True,
                           separators=(",", ":")).encode()
    fingerprint = sha256(canonical).hexdigest()
    if key in LEDGER:
        return "REPLAY" if LEDGER[key] == fingerprint else "KEY_CONFLICT"
    if version != DOCUMENT["version"]:
        return "STALE"
    DOCUMENT["label"] = patch["label"]
    DOCUMENT["version"] += 1
    LEDGER[key] = fingerprint
    return "APPLIED"

def request(key, version, patch):
    return json.dumps({"key": key, "version": version, "patch": patch})

def main():
    cases = [
        ("valid", request("request-1", 1, {"label":"fresh"}), "APPLIED"),
        ("reordered identical", '{"patch":{"label":"fresh"},"version":1,"key":"request-1"}', "REPLAY"),
        ("conflict", request("request-1", 1, {"label":"wrong"}), "KEY_CONFLICT"),
        ("duplicate JSON key", '{"key":"request-2","key":"request-3","version":2,"patch":{"label":"x"}}', "INVALID_JSON"),
        ("large body", request("request-2",2,{"label":"x"})+" "*200, "TOO_LARGE"),
        ("nested excess", request("request-2",2,{"label":{"deep":{"deeper":"x"}}}), "TOO_DEEP"),
        ("unknown field", request("request-2",2,{"role":"admin"}), "INVALID_REQUEST"),
        ("stale", request("request-2",1,{"label":"x"}), "STALE"),
        ("valid new", request("request-2",2,{"label":"updated"}), "APPLIED"),
    ]
    for name, body, expected in cases:
        outcome = handle("alice", body)
        assert outcome == expected, (name, outcome)
        print(f"{name:23} {outcome}")
    assert handle("bob", request("request-3",3,{"label":"no"})) == "DENY_SCOPE"
    assert DOCUMENT == {"owner":"alice","version":3,"label":"updated"}
    assert len(LEDGER) == 2
    print("12/12 toy request-boundary checks passed")

if __name__ == "__main__":
    main()
