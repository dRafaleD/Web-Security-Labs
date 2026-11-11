#!/usr/bin/env python3
"""Synthetic field-level PATCH authorization, no network or DB."""
from copy import deepcopy

ORIGINAL = {
    "doc-1": {
        "owner": "alice", "version": 2,
        "display_name": "Original", "notifications_enabled": False,
    },
    "doc-2": {
        "owner": "bob", "version": 5,
        "display_name": "Other", "notifications_enabled": True,
    },
}
ALLOWED = {"display_name", "notifications_enabled"}


def apply_patch(db, principal, resource_id, expected_version, patch):
    record = db.get(resource_id)
    if record is None or record["owner"] != principal:
        return False, "resource unavailable or unauthorized"
    if type(expected_version) is not int:
        return False, "invalid version type"
    if record["version"] != expected_version:
        return False, "stale version"
    if not isinstance(patch, dict) or not patch:
        return False, "patch must be a nonempty object"
    if not set(patch).issubset(ALLOWED):
        return False, "protected or unknown field"

    changes = {}
    for field, value in patch.items():
        if field == "display_name":
            if not isinstance(value, str):
                return False, "display_name must be text"
            value = value.strip()
            if not 1 <= len(value) <= 40:
                return False, "display_name length invalid"
        elif field == "notifications_enabled" and type(value) is not bool:
            return False, "notifications_enabled must be boolean"
        changes[field] = value

    # Educational in-memory write. A database needs atomic compare-and-swap.
    record.update(changes)
    record["version"] += 1
    return True, "updated"


def main():
    db = deepcopy(ORIGINAL)
    cases = [
        ("valid name", "alice", "doc-1", 2,
         {"display_name": "  Research Notes  "}, True),
        ("role injection", "alice", "doc-1", 3,
         {"role": "admin"}, False),
        ("other owner", "alice", "doc-2", 5,
         {"display_name": "Nope"}, False),
        ("stale update", "alice", "doc-1", 2,
         {"display_name": "Overwritten"}, False),
        ("wrong type", "alice", "doc-1", 3,
         {"notifications_enabled": "yes"}, False),
        ("valid boolean", "alice", "doc-1", 3,
         {"notifications_enabled": True}, True),
    ]
    for label, actor, resource, version, patch, expected in cases:
        accepted, reason = apply_patch(db, actor, resource, version, patch)
        print(f"{label:16} {'ALLOW' if accepted else 'DENY':5} {reason}")
        assert accepted is expected, label
    assert db["doc-1"]["display_name"] == "Research Notes"
    assert db["doc-1"]["notifications_enabled"] is True
    assert db["doc-1"]["version"] == 4
    assert db["doc-1"]["owner"] == "alice" and db["doc-2"] == ORIGINAL["doc-2"]
    print("Synthetic field and version checks passed.")


if __name__ == "__main__":
    main()
