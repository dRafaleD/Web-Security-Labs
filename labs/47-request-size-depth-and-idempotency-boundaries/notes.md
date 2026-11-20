# Day 47 — Request Size, Nesting Depth and Idempotency Boundaries

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](request_limits_demo.py)

## Day 46 follow-up
Day 46 rejected duplicate JSON keys and non-standard numeric values. Day 47 emphasizes **resource limits**: before generating an idempotency fingerprint, a backend needs limits on bytes, nesting and accepted schema.

## Pipeline
1. Verify actor scope from the server-side identity.
2. Enforce the raw UTF-8 byte limit before JSON parsing.
3. Parse with duplicate-key and non-finite number rejection.
4. Reject excessive nesting; validate field names, types and lengths.
5. Canonicalize the validated request for a scoped idempotency fingerprint.
6. Check replay and optimistic version before updating the toy document.

An invalid request must **not reserve an idempotency key** or modify state. The demonstration uses a 160-byte limit and max nesting depth 3, both intentionally tiny for testing.

## Run
```bash
python3 labs/47-request-size-depth-and-idempotency-boundaries/request_limits_demo.py
```

## Questions
Why measure bytes rather than characters? Why should a parser reject duplicate keys before canonicalization? How does excessive nesting exhaust processing resources? Why should a denied request not claim a key? What protections would actual HTTP body streaming and DB concurrency require?

## Limitations
Standard-library in-memory fixture; not a full streaming parser, server, transaction implementation or denial-of-service guarantee.
