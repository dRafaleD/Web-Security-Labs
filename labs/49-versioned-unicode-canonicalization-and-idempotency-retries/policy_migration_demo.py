#!/usr/bin/env python3
"""Offline idempotency policy migration: preserve old keys' canonicalization rules."""
from hashlib import sha256
import json
import unicodedata

POLICY = "raw-v1"  # Application-controlled; no client-selected policy.
LEDGER = {}
DOC = {"owner": "alice", "version": 1, "label": "Initial"}

def digest(actor: str, version: int, label: str, policy: str) -> str:
    normalized = (unicodedata.normalize("NFC", label)
                  if policy == "nfc-v2" else label)
    raw = json.dumps([actor, "doc-a", version, normalized],
                     ensure_ascii=True, separators=(",", ":"))
    return sha256(raw.encode()).hexdigest()

def update(actor: str, key: str, version: int, label: str) -> str:
    if actor != DOC["owner"]:
        return "DENY_SCOPE"
    if (not isinstance(key, str) or not 8 <= len(key) <= 64
            or type(version) is not int or not isinstance(label, str)
            or not 1 <= len(label) <= 32):
        return "INVALID_REQUEST"
    # Existing retry keys MUST use the rule they were originally accepted under.
    old = LEDGER.get((actor, "doc-a", key))
    if old:
        stored_policy, old_digest = old
        return ("REPLAY" if digest(actor, version, label, stored_policy) == old_digest
                else "KEY_CONFLICT")
    if version != DOC["version"]:
        return "STALE_VERSION"
    fp = digest(actor, version, label, POLICY)
    DOC["version"] += 1
    DOC["label"] = (unicodedata.normalize("NFC", label)
                    if POLICY == "nfc-v2" else label)
    LEDGER[(actor, "doc-a", key)] = (POLICY, fp)
    return "APPLIED"

def main():
    global POLICY
    decomposed = "Cafe\u0301"
    composed = "Café"
    cases = [
        ("initial raw request", update("alice", "request-1", 1, decomposed), "APPLIED"),
        ("raw replay", update("alice", "request-1", 1, decomposed), "REPLAY"),
        ("raw composed differs", update("alice", "request-1", 1, composed), "KEY_CONFLICT"),
    ]
    POLICY = "nfc-v2"
    cases.extend([
        ("old key keeps old rule", update("alice", "request-1", 1, decomposed), "REPLAY"),
        ("old key cannot silently migrate", update("alice", "request-1", 1, composed), "KEY_CONFLICT"),
        ("new key uses NFC", update("alice", "request-2", 2, composed), "APPLIED"),
        ("new key replay equivalent", update("alice", "request-2", 2, decomposed), "REPLAY"),
        ("new key different request", update("alice", "request-2", 2, "Other"), "KEY_CONFLICT"),
        ("cross-actor denied", update("bob", "request-3", 3, "Hello"), "DENY_SCOPE"),
        ("stale new key", update("alice", "request-3", 1, "Hello"), "STALE_VERSION"),
    ])
    for name, outcome, expected in cases:
        assert outcome == expected, (name, outcome)
        print(f"{name:37} {outcome}")
    assert DOC == {"owner": "alice", "version": 3, "label": "Café"}
    assert len(LEDGER) == 2
    print(f"{len(cases)+2}/{len(cases)+2} fictional policy migration checks passed")

if __name__ == "__main__":
    main()
