#!/usr/bin/env python3
"""Offline API idempotency: NFC equivalence without casefold/NFKC surprises."""
from hashlib import sha256
import json
import unicodedata

OWNER = "alice"
DOC = {"version": 1, "label": "initial"}
LEDGER: dict[tuple[str, str], str] = {}
MAX_BYTES = 256

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result

def handle(actor: str, raw: str) -> str:
    if actor != OWNER:
        return "DENY_SCOPE"
    if not isinstance(raw, str) or len(raw.encode("utf-8")) > MAX_BYTES:
        return "TOO_LARGE"
    try:
        request = json.loads(raw, object_pairs_hook=unique_pairs)
    except (TypeError, ValueError):
        return "INVALID_JSON"
    if not isinstance(request, dict) or set(request) != {"key", "version", "label"}:
        return "INVALID_REQUEST"
    key, version, label = request["key"], request["version"], request["label"]
    if not isinstance(key, str) or not 8 <= len(key) <= 40:
        return "INVALID_REQUEST"
    if type(version) is not int or not isinstance(label, str):
        return "INVALID_REQUEST"
    normalized = unicodedata.normalize("NFC", label)
    if not 1 <= len(normalized) <= 40:
        return "INVALID_TEXT"
    # Toy API rejects control/format code points, including bidi overrides.
    if any(unicodedata.category(ch) in ("Cc", "Cf") for ch in normalized):
        return "INVALID_TEXT"
    # Deliberately avoid casefold/NFKC: they could merge distinct user values.
    canonical = json.dumps([actor, version, normalized], ensure_ascii=True,
                           separators=(",", ":"))
    digest = sha256(canonical.encode()).hexdigest()
    ledger_key = (actor, key)
    if ledger_key in LEDGER:
        return "REPLAY" if LEDGER[ledger_key] == digest else "KEY_CONFLICT"
    if version != DOC["version"]:
        return "STALE_VERSION"
    DOC["label"] = normalized
    DOC["version"] += 1
    LEDGER[ledger_key] = digest
    return "APPLIED"

def request(key: str, version: int, label: str) -> str:
    return json.dumps({"key": key, "version": version, "label": label},
                      ensure_ascii=False)

def main():
    cases = [
        ("composed accent", "alice", request("request-1", 1, "Café"), "APPLIED"),
        ("decomposed equivalent", "alice", request("request-1", 1, "Cafe\u0301"), "REPLAY"),
        ("case is distinct", "alice", request("request-1", 1, "café"), "KEY_CONFLICT"),
        ("bidi control rejected", "alice", request("request-2", 2, "abc\u202e"), "INVALID_TEXT"),
        ("duplicate member", "alice", '{"key":"request-2","key":"request-3","version":2,"label":"x"}', "INVALID_JSON"),
        ("raw body too large", "alice", " " * 257, "TOO_LARGE"),
        ("stale new key", "alice", request("request-3", 1, "old"), "STALE_VERSION"),
        ("compatibility char accepted", "alice", request("request-2", 2, "①"), "APPLIED"),
        ("NFKC not assumed", "alice", request("request-2", 2, "1"), "KEY_CONFLICT"),
        ("same record replay", "alice", request("request-2", 2, "①"), "REPLAY"),
        ("wrong user", "bob", request("request-4", 3, "x"), "DENY_SCOPE"),
        ("valid next update", "alice", request("request-4", 3, "final"), "APPLIED"),
    ]
    for title, actor, raw, expected in cases:
        actual = handle(actor, raw)
        assert actual == expected, (title, actual)
        print(f"{title:29} {actual}")
    assert DOC == {"version": 4, "label": "final"}
    assert len(LEDGER) == 3
    print(f"{len(cases)+2}/{len(cases)+2} Unicode/idempotency checks passed")

if __name__ == "__main__":
    main()
