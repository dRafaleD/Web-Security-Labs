# Day 40 — Idempotency Keys and Replay-Safe PATCH Requests

[English](notes.md) · [Türkçe](notes.tr.md) · [Python practice](idempotency_demo.py)

## From version guards to retries
Day 39 added field-level PATCH permission checks and optimistic versions. Day 40 asks: **what if the client times out and retries exactly the same update?** Repeating a request should not necessarily perform the mutation twice.

An **idempotency key** identifies a logical operation. A trusted server binds the key to the authenticated actor, target resource, expected version and canonicalized request body. Same key + same request → stored outcome; same key + changed request → rejection.

## Local model
The fixture has a document with owner `alice`, version 2 and a title. An in-memory ledger records the request fingerprint and resulting version.
- First authorized PATCH with `request-001`: update to version 3.
- Identical retry: return the prior result without another write.
- Reusing that key for a different body: reject.
- User `bob` cannot replay `alice`'s key to access the document.
- New key with stale version 2: reject.
- New authorized update at version 3: produce version 4; retry does not write again.

**Important:** rejecting unauthorized requests happens before serving a cached result. The fingerprint is not a substitute for authentication, authorization or an HMAC. Request keys should be high-entropy in production; these are readable training identifiers.

## Run
~~~bash
python3 labs/40-idempotency-keys-and-replay-safe-patch/idempotency_demo.py
~~~

## Production differences
A real implementation needs persistent ledger storage, atomic compare-and-swap with the resource update, scoped keys, expiry policies, collision limits and safe handling of failures between mutation and result persistence. This single-process demo does **not** solve concurrency or crash consistency.

## Questions
1. What does idempotency protect against, and what does it *not* protect against?
2. Why must the body and actor be included in the binding?
3. What is the difference between an HTTP request replay and a new authorized update?
4. How could a crash between writing the document and writing the ledger cause double application?
5. Which failures should a service retry automatically?

## Scope
All data is synthetic. No web server, external service, database or real credentials are involved.
