#!/usr/bin/env python3
"""Offline JSON parsing and scoped idempotency; reject ambiguous duplicate keys."""
import hashlib
import json

DOC = {"owner": "alice", "version": 1, "name": "Old", "active": False}
LEDGER = {}

def unique_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result

def reject_constant(value: str):
    raise ValueError(f"non-finite JSON value: {value}")

def handle(actor: str, resource: str, raw: str) -> str:
    if actor != DOC["owner"] or resource != "doc-a":
        return "DENY_SCOPE"
    if not isinstance(raw, str) or len(raw) > 2048:
        return "INVALID_JSON"
    try:
        request = json.loads(raw, object_pairs_hook=unique_object,
                             parse_constant=reject_constant)
    except (ValueError, TypeError, json.JSONDecodeError):
        return "INVALID_JSON"
    if not isinstance(request, dict) or set(request) != {"version", "key", "patch"}:
        return "INVALID_REQUEST"
    version, key, patch = request["version"], request["key"], request["patch"]
    if type(version) is not int or not isinstance(key, str) or not 8 <= len(key) <= 64:
        return "INVALID_REQUEST"
    if not isinstance(patch, dict) or not patch or not set(patch) <= {"name", "active"}:
        return "INVALID_REQUEST"
    if "name" in patch and (not isinstance(patch["name"], str)
                             or not 1 <= len(patch["name"]) <= 40):
        return "INVALID_REQUEST"
    if "active" in patch and type(patch["active"]) is not bool:
        return "INVALID_REQUEST"
    # Canonicalize a VALIDATED object. Raw JSON field order is irrelevant.
    canonical = json.dumps([actor, resource, version, patch], sort_keys=True,
                           ensure_ascii=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    ledger_key = (actor, resource, key)
    if ledger_key in LEDGER:
        return "REPLAY" if LEDGER[ledger_key] == digest else "KEY_CONFLICT"
    if DOC["version"] != version:
        return "STALE_VERSION"
    DOC.update(patch)
    DOC["version"] += 1
    LEDGER[ledger_key] = digest
    return "APPLIED"

def main():
    cases = [
        ("original", '{"version":1,"key":"request-01","patch":{"name":"New","active":true}}', "APPLIED"),
        ("reordered fields", '{"patch":{"active":true,"name":"New"},"key":"request-01","version":1}', "REPLAY"),
        ("different key same old version", '{"version":1,"key":"request-02","patch":{"name":"Other"}}', "STALE_VERSION"),
        ("conflicting key reuse", '{"version":1,"key":"request-01","patch":{"name":"Other"}}', "KEY_CONFLICT"),
        ("duplicate top-level key", '{"version":1,"version":2,"key":"request-03","patch":{"name":"N"}}', "INVALID_JSON"),
        ("duplicate nested key", '{"version":2,"key":"request-03","patch":{"name":"N","name":"X"}}', "INVALID_JSON"),
        ("nonfinite", '{"version":2,"key":"request-03","patch":{"active":NaN}}', "INVALID_JSON"),
        ("booleans are not versions", '{"version":true,"key":"request-03","patch":{"name":"N"}}', "INVALID_REQUEST"),
        ("mass assignment", '{"version":2,"key":"request-03","patch":{"role":"admin"}}', "INVALID_REQUEST"),
        ("valid second update", '{"version":2,"key":"request-03","patch":{"active":false}}', "APPLIED"),
    ]
    for label, raw, expected in cases:
        got = handle("alice", "doc-a", raw)
        assert got == expected, (label, got)
        print(f"{label:30} {got}")
    assert DOC == {"owner": "alice", "version": 3, "name": "New", "active": False}
    assert len(LEDGER) == 2
    print(f"{len(cases)+2}/{len(cases)+2} toy JSON and request checks passed")

if __name__ == "__main__":
    main()
