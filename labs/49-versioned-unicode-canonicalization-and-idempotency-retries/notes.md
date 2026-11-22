# Day 49 — Versioned Unicode Canonicalization and Idempotency Retries

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](policy_migration_demo.py)

## From Day 48
The application defined equivalence of composed and decomposed Unicode text using **NFC**. But how should an idempotency service behave if that rule changes **while old retry keys remain valid**?

## Safe migration idea
The host controls a canonicalization policy version. An accepted idempotency entry stores **which policy produced its fingerprint**:
- **raw-v1:** literal Unicode code-point sequence.
- **nfc-v2:** text normalized to NFC.

After migration, **new keys** use v2. Existing keys always recompute retry fingerprints using **their stored policy**, so an old raw key cannot silently acquire a different meaning. A composed string using an old key conflicts even though newly issued v2 keys consider composed and decomposed text equivalent.

All keys remain tied to the authenticated actor, resource and original expected document version. The same key with different request semantics is rejected.

## Run
```bash
python3 labs/49-versioned-unicode-canonicalization-and-idempotency-retries/policy_migration_demo.py
```

## Questions
Why must canonicalization rules be versioned when requests may be retried? Could changing case folding or NFKC alter business identity? How should very old keys expire? Why does this model still need transactional key reservation and document updates?

## Limits
In-memory Python fixture, no HTTP, database, distributed concurrency or complete Unicode security policy.
