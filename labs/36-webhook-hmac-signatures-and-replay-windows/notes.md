# Day 36 — Webhook HMAC Signatures and Replay Windows

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python lab](webhook_demo.py)

## Problem: a webhook is not automatically trusted
A backend may accept callbacks from a payment provider or a CI system. A request that *claims* to be from the provider is still an untrusted HTTP request. Check the **raw message bytes** with the sender's documented verification procedure before modifying application state.

## HMAC signing
HMAC-SHA256 combines a shared secret key with bytes from a request. Unlike hashing the payload by itself, forging a valid MAC without the secret should be computationally infeasible under proper key handling. Use `hmac.compare_digest` for comparing expected and received values. Never put the secret in the URL, public logs or repository.

**Critical detail:** Signing parsed JSON and then reserializing it may change whitespace and byte order. Verify the **original received bytes**, exactly as the provider's specification requires.

## Replay defense
A real signature remains valid when the **same signed request** is delivered again. A timestamp tolerance rejects very old or too-far-future events, but alone cannot stop a replay inside that window. Use a durable event-ID / nonce store with an appropriate retention window and atomic deduplication. Your application should also be idempotent.

## Hands-on (no network, no real credentials)
```bash
python3 webhook_demo.py
```
The program signs synthetic bytes with a hardcoded **demo-only** secret, then tests valid, tampered, stale and duplicate messages. It does not implement a specific provider's header format; use their current documentation for production.

## Challenge
1. Predict why changing one byte invalidates the signature.
2. Which check prevents a previously accepted event from running twice?
3. Explain the tradeoff between network clock skew and a replay window.
4. Why must signature verification occur before parsing and processing?
5. What could go wrong if the deduplication store exists only in one worker's RAM?

## Evidence and limitations
Record event ID, validation result and timing metadata without raw secrets. The in-memory set here is not distributed-safe, and verification does not authorize an arbitrary business action.
