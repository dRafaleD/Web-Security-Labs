# Day 37 — JSON Request Limits, Duplicate Keys and Parser Boundaries

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python lab](json_guard_demo.py)

## Why JSON is still untrusted input
APIs often accept JSON, but a request's declared `Content-Type` does not prove that its bytes are valid or safe. Excessively large bodies, deep structures, ambiguous duplicate keys and nonstandard numeric constants can lead to inconsistent interpretation or resource exhaustion. Enforce a **byte limit before parsing**, then validate format and business schema.

## Layered checks
1. Check the media type (`application/json`) instead of trusting an arbitrary label.
2. Enforce the raw body size, including UTF-8 bytes, before calling a JSON parser.
3. Decode as strict UTF-8; reject malformed JSON and `NaN` / `Infinity`, which Python's permissive defaults can otherwise accept.
4. Reject **duplicate object keys**, for example `{"role":"reader","role":"admin"}`. Different consumers can interpret such data differently.
5. Check maximum nesting depth and node count **after parsing**. These do not protect the JSON decoder itself from all deep-input CPU/memory risks; production gateways need proven streaming limits and timeouts.
6. Validate expected fields, types and authorization separately. Passing this lab's syntax guards does **not** authorize an API action.

## Run (no server, network or dependencies)
```bash
python3 json_guard_demo.py
```
The script tests a valid small object, wrong media type, oversized body, duplicate key, malformed UTF-8, nonstandard number and excessive nesting. It prints allowed/denied decisions and asserts the expected result for every synthetic case.

## Exercises
1. Why is checking `len(body)` better than counting characters after decoding?
2. Explain why two parsers disagreeing about duplicate keys creates a security risk.
3. Change the maximum depth to 2: what happens to an otherwise valid nested object?
4. Add an application-level schema, such as `id` being an integer and `action` being one of two allowed words.
5. Where should request timeouts, decompression limits and rate limits be enforced?

## Limitations
This is a **post-receipt, offline validation model**. A real HTTP server must limit request transfer, chunking, decompression, buffering and parser work at the appropriate layers. No vulnerable server or exploit payload is provided.
