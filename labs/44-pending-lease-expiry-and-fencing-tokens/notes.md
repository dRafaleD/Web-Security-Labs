# Day 44 — Pending Lease Expiry and Fencing Tokens

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](lease_fencing_demo.py)

## From Day 43
Day 43 introduced `PENDING`, `IN_PROGRESS` and `REPLAY` statuses for idempotent requests. But what happens if a worker crashes while a request is **PENDING**? A never-ending pending entry can block every retry.

## Lease and fencing concept
A **lease** grants a worker a bounded period to process a request. Once that period expires, another worker can reserve the same logical operation. The new worker receives a **larger fencing token**.

The model demonstrates:
1. First reservation gets token 1 and expires at time 110.
2. A retry before expiry returns `IN_PROGRESS`.
3. At expiry a new reservation gets token 2.
4. The old worker with token 1 is rejected, even if it tries to finish later.
5. Only the current worker may commit the version-checked update.
6. Subsequent identical retries return `REPLAY`.

## Reproduce
~~~bash
python3 labs/44-pending-lease-expiry-and-fencing-tokens/lease_fencing_demo.py
~~~

## Production caveat
This deterministic function only **models** a transaction. In production, fencing checks and resource mutation must be enforced atomically by durable storage; otherwise a late worker can still race with a new worker. Key ownership must be scoped to authenticated actor, resource and canonical request fingerprint. Crash recovery, lease clocks and retention require additional design.

## Questions
1. Why is a timeout insufficient to prevent a stale worker's write?
2. What distinguishes a lease ID from a monotonically increasing fencing token?
3. What happens if the first worker commits before the retry but loses its response?
4. Why must resource write and ledger state transition be in one transaction?
5. Why is `IN_PROGRESS` not a success response?

## Scope
No real HTTP, DB, threads, network or locks. All times are fictional integers.
