# Day 41 — Idempotency Expiry and Replay Boundaries

[English](notes.md) · [Türkçe](notes.tr.md) · [Python practice](expiry_demo.py)

## Day 40 follow-up
An idempotency key prevents duplicate application **while its ledger entry is retained**. Real services have retention/expiry limits. What happens when the entry expires?

## Toy model
A key is scoped to an actor and bound to the request body and expected version. Before expiry, identical requests replay the recorded result and changed bodies fail with `KEY_CONFLICT`. At or after expiry the key may be treated as new, **but the optimistic version check rejects an already-applied stale update**. This illustrates defense in depth, not complete replay protection.

## Run
```bash
python3 labs/41-idempotency-expiry-and-replay-boundaries/expiry_demo.py
```

## Questions
1. Why can't a key be assumed unique forever?
2. Why does expiry not make an old request safe to apply again?
3. What if a mutation succeeds but the ledger write fails?
4. Why must real storage atomically commit the resource and ledger?

## Limits
In-memory, single-process simulation with fake time; no HTTP server or persistence. Real implementations require transactional storage, concurrency control, bounded retention and secure key generation.
