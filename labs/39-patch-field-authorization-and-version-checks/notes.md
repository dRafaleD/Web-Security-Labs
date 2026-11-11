# Day 39 — PATCH Field Authorization and Version Checks

[English](notes.md) · [Türkçe](notes.tr.md) · [Offline Python exercise](patch_guard_demo.py)

## Why partial updates need their own rules
Day 38 demonstrated how a valid JSON object can still attempt **mass assignment**, such as setting is_admin or owner. A PATCH request is even easier to misread: it intends to update *only selected fields*, and an application may accidentally copy them directly into a database object.

This lesson models a narrow **partial-update policy**. The client can update only display_name or notifications_enabled. The server retains trusted owner, object ID, version and any privilege metadata. Object-level authorization is checked first.

## Decisions a safe update layer makes
1. **Who is acting?** The principal is a trusted function argument, never a field from the patch body.
2. **Which object?** Resolve the object; do not let a syntactically valid ID bypass ownership checks (BOLA/IDOR).
3. **Which fields?** Use a per-operation allowlist; reject owner, role, version and unknown keys. Prefer rejecting the entire patch to silently discarding protected fields.
4. **Which values?** Apply strict field-specific validation. In Python, booleans must not pass an integer check by accident.
5. **Which version?** Require an expected version to reject stale edits. This models optimistic concurrency; an actual database must perform the version check and update **atomically**.
6. **What is recorded?** Log outcome and reason without copying secrets or full untrusted payloads into public logs.

## Hands-on (no server, database or network)
~~~bash
python3 patch_guard_demo.py
~~~

The program begins with two fictional users' documents, accepts a valid update, rejects a protected role field, rejects another user's object, rejects a stale version, rejects a malformed value and then accepts an authorized boolean update. Assertions verify both decisions and stored state.

## Exercises
1. Why is rejecting protected keys safer than simply ignoring them?
2. Explain why field-level validation cannot replace object-level authorization.
3. Add a writable theme field with a finite allowlist.
4. What can go wrong when two workers both check version 3 and then write version 4 without a transaction?
5. Compare HTTP PATCH (partial changes) with PUT (usually full representation); why does neither method guarantee authorization by itself?
6. How would you design audit logs without exposing sensitive request fields?

## Limits
This deterministic script is a policy demonstration, not an HTTP implementation, JSON Patch RFC implementation, authentication system, or production database transaction. Real services need atomic conditional writes, appropriate authentication and consistent validation.
