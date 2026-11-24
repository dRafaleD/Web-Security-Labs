# Day 51 — Idempotent Operation Receipts and Reconciliation

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](receipt_demo.py)

Day 50 prevented expired idempotency keys from silently applying an old operation again. Day 51 adds a separate **read-only receipt lookup** for clients unsure whether an earlier operation committed. A receipt is scoped to the authenticated actor, resource and operation key. Historical committed versions remain historical; they are not proof of current resource state. If the current version predates a recorded commit, the result requests reconciliation instead of applying another write.

**Questions:** Why is reading a receipt distinct from retrying a mutation? Why must receipt access check current authorization? What durable transaction would bind an actual receipt to a committed mutation?

The authorization boolean and version come from an imagined trusted server. This fixture has no HTTP endpoints, database, concurrency or real state changes.

## Run
```bash
python3 labs/51-idempotent-operation-receipts-and-reconciliation/receipt_demo.py
```
