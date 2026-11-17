#!/usr/bin/env python3
"""Offline idempotency lease/fencing model; no real concurrency or database."""
from dataclasses import dataclass

@dataclass
class Job:
    fingerprint: str
    status: str
    lease_until: int
    token: int

LEDGER: dict[str, Job] = {}
DOC = {"version": 2, "text": "initial"}
NEXT_TOKEN = 0
LEASE_SECONDS = 10

def reserve(key: str, fingerprint: str, now: int) -> tuple[str, int | None]:
    global NEXT_TOKEN
    if not key or not fingerprint:
        return "INVALID", None
    current = LEDGER.get(key)
    if current:
        if current.fingerprint != fingerprint:
            return "KEY_CONFLICT", None
        if current.status == "COMMITTED":
            return "REPLAY", None
        if now < current.lease_until:
            return "IN_PROGRESS", None
    # Lease takeover increments fencing token; older workers lose authority.
    NEXT_TOKEN += 1
    LEDGER[key] = Job(fingerprint, "PENDING", now + LEASE_SECONDS, NEXT_TOKEN)
    return "RESERVED", NEXT_TOKEN

def finish(key: str, token: int, now: int, expected_version: int, text: str) -> str:
    job = LEDGER.get(key)
    if not job or job.status != "PENDING" or job.token != token:
        return "STALE_WORKER"
    if now >= job.lease_until:
        return "LEASE_EXPIRED"
    if DOC["version"] != expected_version:
        return "STALE_VERSION"
    # Illustrative atomic transition only: DB must commit document+ledger together.
    DOC["text"] = text
    DOC["version"] += 1
    job.status = "COMMITTED"
    return "COMMITTED"

def main() -> None:
    result, token1 = reserve("req-001", "body-v1", 100)
    assert result == "RESERVED" and token1 == 1
    assert reserve("req-001", "body-v1", 102)[0] == "IN_PROGRESS"
    assert reserve("req-001", "changed", 102)[0] == "KEY_CONFLICT"
    assert finish("req-001", token1, 110, 2, "old") == "LEASE_EXPIRED"
    result, token2 = reserve("req-001", "body-v1", 110)
    assert result == "RESERVED" and token2 == 2
    assert finish("req-001", token1, 111, 2, "old") == "STALE_WORKER"
    assert finish("req-001", token2, 112, 2, "new") == "COMMITTED"
    assert reserve("req-001", "body-v1", 115)[0] == "REPLAY"
    assert DOC == {"version": 3, "text": "new"}
    assert finish("req-001", token2, 116, 2, "duplicate") == "STALE_WORKER"
    print("10/10 lease and fencing scenarios passed; transactions not implemented")

if __name__ == "__main__":
    main()
