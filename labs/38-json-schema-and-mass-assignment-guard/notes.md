# Day 38 — JSON Schema Boundaries and Mass Assignment Defense

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python demo](schema_guard_demo.py)

## From valid JSON to safe API behavior
Day 37 rejected oversized, ambiguous or malformed JSON. However, **syntactically valid JSON can still ask an application to change a protected property**. This lab studies *mass assignment*: binding every client-provided field directly onto a server-side object.

A user might send `{"id":7,"action":"read","is_admin":true}`. The `is_admin` key is valid JSON, but clients must not control their own privilege level. The application should **allowlist permitted input keys**, reject unexpected fields, and populate owner/role from trusted server-side identity.

## Four separate defenses
1. **Parsing:** Reject malformed UTF-8/JSON, duplicate keys and unsupported constants (the previous day's topic).
2. **Schema:** Require exactly `id` (integer, not boolean) and `action` (one of `read`, `list`). Reject extra fields such as `owner`, `role` or `is_admin`.
3. **Object-level authorization:** Resolve the requested object and compare its trusted owner with the authenticated principal. A valid `id` does not establish permission.
4. **Business logic:** The demo **makes decisions only**; real state-changing requests also need transaction boundaries, audit logs and appropriate validation of each mutation.

The Python fixture models a tiny repository of objects owned by `alice` and `bob`. The caller identity comes from an explicit trusted function argument, never from the untrusted JSON body.

## Run locally
```bash
python3 schema_guard_demo.py
```
The script tests a valid request, unexpected privilege field, spoofed owner, invalid type, boolean-as-integer confusion, unknown action, and another owner's object. Each expectation is asserted; there is no HTTP server or data modification.

## Exercises
1. Why is `bool` a special case when validating integers in Python?
2. What goes wrong if an ORM model blindly receives `**request.json`?
3. Why can a schema-valid `id` still cause an IDOR/BOLA failure?
4. Add a `write` action that is **denied by default**, then design an explicit authorization policy for it.
5. Where should authentication context be established in a real application?
6. Why should validation errors avoid reflecting secrets or internal object metadata?

## Limits
This educational code does not authenticate users or implement a production API. The resource ownership list is synthetic; there is no database and no network activity. Schema validation and object-level authorization are both necessary, but neither alone guarantees application security.
