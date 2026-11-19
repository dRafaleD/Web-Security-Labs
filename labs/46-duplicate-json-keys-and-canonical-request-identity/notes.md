# Day 46 — Duplicate JSON Keys and Canonical Request Identity

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](strict_json_demo.py)

## After Day 45
Day 45 used stable JSON ordering to fingerprint **equivalent** API requests. But normalization must not silently hide **ambiguous input**. JSON with duplicate keys can be interpreted differently by proxies, application code or logging infrastructure.

## Safe order of operations
1. **Parse strictly**: reject duplicate keys at any nesting level and non-finite values such as `NaN`.
2. **Validate shape and types**: permitted fields, bounded strings, correct version type (a Python `bool` is not accepted as an integer version).
3. **Authorize actor/resource** from trusted application context, not user-supplied JSON.
4. **Canonicalize only validated fields** and compute a fingerprint.
5. **Check scoped idempotency key** and expected resource version before applying an in-memory update.

Two object-key orders replay as one request. Repeated or conflicting keys, unknown patch fields and stale versions fail. The script intentionally has no HTTP server or database.

## Run
```bash
python3 labs/46-duplicate-json-keys-and-canonical-request-identity/strict_json_demo.py
```

## Questions
Why is accepting the last duplicate JSON key unsafe? Can a proxy and backend disagree about canonical identity? Why validate type before hashing? Why does a database transaction remain necessary with concurrent workers?

## Limitations
Toy parser, single process, no resource-size streaming limits or durable atomic idempotency storage. Adapt validation to the specific API contract.
