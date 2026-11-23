# Day 50 — Idempotency Key Expiry and Reuse Tombstones

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](expiry_tombstone_demo.py)

## After Day 49
The previous lab versioned Unicode canonicalization policies so old idempotency keys retained their original meaning. Day 50 explores **expiration**: if a server deletes all record of an expired key, a delayed client retry could accidentally reapply the original business operation.

## Toy policy
The endpoint validates actor, resource, fields and optimistic document version, then creates a fingerprint using NFC-normalized text. An accepted key has a **10-unit TTL**. Within that window an identical request returns `REPLAY`, while a changed request returns `KEY_CONFLICT`.

After expiry the key becomes an **EXPIRED_KEY tombstone**, and is never accepted as a fresh key during this exercise. A new key can perform a *new* authorized operation at the current document version. The tombstone prevents a previously successful request from being mistaken for a new operation after its original response window ends.

## Run
```bash
python3 labs/50-idempotency-key-expiry-and-reuse-tombstones/expiry_tombstone_demo.py
```

## Questions
Why can deleting an expired key cause duplicate business effects? Why does a server need an explicit key-retention contract? When can tombstones safely be purged? Why are durable transactions, monotonically understood time and unique constraints necessary in production?

## Limits
No HTTP, real database, distributed retries or durable storage. An indefinite tombstone ledger is only a model; real systems need bounded retention and a clearly documented reuse policy.
