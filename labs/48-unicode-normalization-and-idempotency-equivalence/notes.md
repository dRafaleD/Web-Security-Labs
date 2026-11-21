# Day 48 — Unicode Normalization and Idempotency Equivalence

[English](notes.md) · [Türkçe](notes.tr.md) · [Python exercise](unicode_idempotency_demo.py)

## From Day 47
Day 47 limited JSON size, nesting and accepted fields before computing a request fingerprint. A subtle question remains: **which Unicode text values are logically the same request?**

## Contract-defined equivalence
This toy endpoint accepts a user-visible `label` and explicitly normalizes it to **NFC** *after strict request validation*. Thus composed `é` and decomposed `e + combining acute` have the same fingerprint and replay as one request.

The example **does not** apply case folding or **NFKC** compatibility normalization: `①` is not silently merged with `1`, nor `Café` with `café`. It rejects control/format characters including bidi overrides and malformed/duplicate JSON members before reserving an idempotency key.

The chosen equivalence is an **application contract**, not a universal Unicode security rule. Different APIs (e.g. passwords or identifiers) may require preserving exact bytes.

## Run
```bash
python3 labs/48-unicode-normalization-and-idempotency-equivalence/unicode_idempotency_demo.py
```

## Questions
1. What is the difference between NFC and NFKC?
2. Why can case folding change an identifier's meaning?
3. Why must request normalization be defined before computing idempotency hashes?
4. How can different client/server canonicalization rules cause replay-key conflicts?
5. What additional concerns arise for filenames and account identifiers?

## Limits
Single-process toy validation, not a full Unicode identifier policy, HTTP server or atomic DB ledger.
