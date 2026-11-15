# Day 42 — Concurrent Retries, Version Checks and Idempotency

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](race_demo.py)

## Continuing Day 41
An idempotency key has an expiry window, but even unexpired keys cannot solve a **race** if two clients read the same resource version before either writes.

## Deterministic interleaving
Clients A and B both start with document version 2:
1. A commits with key `operation-a`: value changes and version becomes 3.
2. B submits a different operation based on stale version 2: rejected.
3. A retries identical parameters: returns `REPLAY` without a second write.
4. Reusing A's key for a changed payload is rejected.
5. A new valid operation at version 3 advances the record to version 4.

The function models a single **atomic compare-and-swap + idempotency-ledger insert**, but Python alone does **not** make database operations atomic. Real services must commit the resource and ledger together in a transaction and handle in-flight duplicate keys, crash recovery, authorization and persistent storage.

## Run
~~~bash
python3 labs/42-concurrent-retries-version-checks-and-idempotency/race_demo.py
~~~

## Questions
1. Why does a key lookup followed by an unlocked write still race?
2. What happens if a server crashes after the resource write but before recording the idempotency result?
3. Why must replay checks remain scoped to the authorized actor?
4. What HTTP response and retry policy would you choose for a stale version?

## Limits
No threads, sockets, HTTP server or DB. This deterministic trace illustrates **intended semantics**, not a proof of concurrency safety.
