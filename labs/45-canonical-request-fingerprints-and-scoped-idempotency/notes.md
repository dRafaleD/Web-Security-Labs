# Day 45 — Canonical Request Fingerprints and Scoped Idempotency

[English](notes.md) · [Türkçe](notes.tr.md) · [Python practice](canonical_idempotency_demo.py)

## From Day 44
Day 44 modeled a **lease** and **fencing token** for competing workers. A separate issue arises earlier: the server needs to recognize the *same logical request* even when clients serialize object fields in a different order.

## Deterministic fingerprints
The toy application binds the request to the authenticated actor, resource, expected version and validated PATCH fields. It serializes an in-memory JSON object using a stable key order and separators before computing SHA-256.

- Same key + same logical JSON object (regardless of insertion order): **REPLAY**.
- Same key + different validated request: **KEY_CONFLICT**.
- New key with stale document version: **STALE_VERSION**.
- Unauthorized actor/resource or protected field: rejected before changing state.

This protects only the modeled single-process behavior. A request fingerprint is **not** a signature and does not grant authorization. Real systems must define canonical representations carefully, reject ambiguous JSON such as duplicate keys before normalization, scope key storage to identities/resources, and use atomic transactions with the fencing controls introduced previously.

## Run
~~~bash
python3 labs/45-canonical-request-fingerprints-and-scoped-idempotency/canonical_idempotency_demo.py
~~~

## Questions
1. Why should swapping JSON object field order preserve request identity?
2. Could normalizing whitespace or Unicode change a request's meaning?
3. Why must input validation happen before creating a fingerprint?
4. Why does an idempotency cache still need transactional storage?
5. What makes two requests equivalent for a particular API contract?

## Limit
No actual HTTP, database, race simulation or remote system. Synthetic in-memory examples only.
