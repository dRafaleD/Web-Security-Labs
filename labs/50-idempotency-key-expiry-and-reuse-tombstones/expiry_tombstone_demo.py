#!/usr/bin/env python3
"""Offline idempotency ledger: expired keys are tombstoned, not silently reusable."""
from hashlib import sha256
import json
import unicodedata

TTL = 10
DOC = {"owner":"alice", "version":1, "label":"Initial"}
LEDGER = {}  # (actor, resource, key) -> immutable fingerprint and expires_at

def normalize(value):
    return unicodedata.normalize("NFC",value)

def fingerprint(actor, resource, version, label):
    body = json.dumps([actor,resource,version,normalize(label)],
                      separators=(",",":"),ensure_ascii=True).encode()
    return sha256(body).hexdigest()

def handle(actor, resource, key, version, label, now):
    if actor != DOC["owner"] or resource != "doc-a":
        return "DENY_SCOPE"
    if (not isinstance(key,str) or not 8<=len(key)<=50
            or type(version) is not int or type(now) is not int
            or not isinstance(label,str) or not 1<=len(label)<=40):
        return "INVALID"
    identity = (actor,resource,key)
    fp = fingerprint(actor,resource,version,label)
    if identity in LEDGER:
        previous,deadline = LEDGER[identity]
        if now >= deadline:
            return "EXPIRED_KEY"  # Tombstone prevents reapplying old operation.
        return "REPLAY" if previous == fp else "KEY_CONFLICT"
    if version != DOC["version"]:
        return "STALE_VERSION"
    DOC["label"] = normalize(label)
    DOC["version"] += 1
    LEDGER[identity] = (fp,now+TTL)
    return "APPLIED"

def main():
    tests = [
        ("original", handle("alice","doc-a","request-01",1,"Cafe\u0301",100), "APPLIED"),
        ("NFC equivalent retry", handle("alice","doc-a","request-01",1,"Café",109), "REPLAY"),
        ("conflicting retry", handle("alice","doc-a","request-01",1,"Other",109), "KEY_CONFLICT"),
        ("expires at deadline", handle("alice","doc-a","request-01",1,"Café",110), "EXPIRED_KEY"),
        ("cannot resurrect key", handle("alice","doc-a","request-01",1,"Café",111), "EXPIRED_KEY"),
        ("fresh key with old version", handle("alice","doc-a","request-02",1,"Fresh",111), "STALE_VERSION"),
        ("fresh key new version", handle("alice","doc-a","request-02",2,"Fresh",111), "APPLIED"),
        ("fresh key replay", handle("alice","doc-a","request-02",2,"Fresh",112), "REPLAY"),
        ("cross user denied", handle("bob","doc-a","request-03",3,"Bad",112), "DENY_SCOPE"),
        ("unknown resource", handle("alice","doc-x","request-03",3,"Bad",112), "DENY_SCOPE"),
        ("boolean version invalid", handle("alice","doc-a","request-03",True,"Bad",112), "INVALID"),
    ]
    for name,actual,expected in tests:
        assert actual==expected,(name,actual)
        print(f"{name:32} {actual}")
    assert DOC == {"owner":"alice","version":3,"label":"Fresh"}
    assert len(LEDGER)==2
    print(f"{len(tests)+2}/{len(tests)+2} fictional idempotency TTL checks passed")

if __name__=="__main__":
    main()
