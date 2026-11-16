# Day 43 — Idempotency Pending States and Retry Decisions

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](pending_demo.py)

## After Day 42
Day 42 showed how optimistic versions prevent a second client from overwriting a newer update. But what should happen when an identical request arrives **while the first one is still processing**?

## Toy state machine
A fictional server keeps an entry for `(authenticated actor, idempotency key)` containing a fingerprint, expected resource version and status:
- **No entry:** validate request and version, create `PENDING`.
- **PENDING + identical parameters:** return `IN_PROGRESS`; do **not** execute again.
- **COMMITTED + identical parameters:** return `REPLAY`; do not write again.
- **Same key + different parameters:** return `KEY_CONFLICT`.
- **Abort before commit:** remove the pending entry so an authorized retry can start again.
- **Stale version:** reject before reserving a fresh key.

## Reproduce
~~~bash
python3 labs/43-idempotency-pending-states-and-retry-decisions/pending_demo.py
~~~

## Real-world boundaries
The `finish()` function models an indivisible change of the resource and ledger status only within a deterministic Python process. A real deployment needs a **transaction or equivalent atomic primitive**, locks/constraints for concurrent workers, crash recovery, pending-entry expiry, bounded key retention and re-authorization. Never treat `IN_PROGRESS` as proof that a request will eventually succeed.

## Questions
1. Why should a concurrent retry not create a second work item?
2. How should a client handle `IN_PROGRESS` versus `REPLAY`?
3. What can happen if a worker crashes between the resource update and the ledger commit?
4. When can a pending entry be safely retried or discarded?
5. Why must idempotency-key lookup be scoped to the authenticated user?

## Safety
No network, HTTP server, database or threads. The state trace is a learning aid, not production-ready concurrency logic.
