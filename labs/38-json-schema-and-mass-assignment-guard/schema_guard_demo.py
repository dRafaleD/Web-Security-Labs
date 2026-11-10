#!/usr/bin/env python3
"""Safe, offline JSON schema and object-authorization teaching fixture."""
import json

OWNERS = {7: "alice", 8: "bob"}
FIELDS = {"id", "action"}
ACTIONS = {"read", "list"}


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_):
    raise ValueError("nonstandard JSON number")


def authorize(principal: str, raw_json: str) -> tuple[bool, str]:
    try:
        data = json.loads(raw_json,
                          object_pairs_hook=reject_duplicate_keys,
                          parse_constant=reject_constant)
    except ValueError:
        return False, "invalid JSON"
    if not isinstance(data, dict):
        return False, "expected a JSON object"
    if set(data) != FIELDS:
        return False, "missing or unexpected input fields"
    # bool is a subclass of int; exact type check is intentional.
    if type(data["id"]) is not int or data["id"] < 0:
        return False, "id must be a nonnegative integer"
    if type(data["action"]) is not str or data["action"] not in ACTIONS:
        return False, "action not permitted"
    if OWNERS.get(data["id"]) != principal:
        return False, "resource not found or not accessible"
    return True, "schema and owner checks passed (no action executed)"


def main():
    cases = [
        ("valid read", "alice", '{"id":7,"action":"read"}', True),
        ("admin injection", "alice",
         '{"id":7,"action":"read","is_admin":true}', False),
        ("owner spoof", "bob",
         '{"id":7,"action":"read","owner":"bob"}', False),
        ("string id", "alice", '{"id":"7","action":"read"}', False),
        ("boolean id", "alice", '{"id":true,"action":"read"}', False),
        ("unknown action", "alice", '{"id":7,"action":"delete"}', False),
        ("other owner", "alice", '{"id":8,"action":"read"}', False),
        ("duplicate key", "alice",
         '{"id":7,"id":8,"action":"read"}', False),
    ]
    for label, principal, body, expected in cases:
        allowed, reason = authorize(principal, body)
        print(f"{label:16} {'ALLOW' if allowed else 'DENY':5} | {reason}")
        assert allowed is expected, (label, reason)
    print("All synthetic authorization checks passed.")


if __name__ == "__main__":
    main()
