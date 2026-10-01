# Day 6 — Authorization and Access Control Foundations

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand what authorization means after authentication has identified a user, and learn why access-control decisions must be enforced by the server for every protected resource and action.

This lab focuses on:

- authentication vs authorization
- subjects, objects and actions
- object-level authorization
- function-level authorization
- roles and ownership
- 401 vs 403
- deny-by-default thinking
- server-side enforcement
- IDOR/BOLA concepts
- safe local access-control testing

The included Flask application is intentionally small and defensive. It demonstrates correct checks rather than teaching how to attack a real service.

## 1. Authentication is not authorization

From Day 5:

```text
Authentication -> Who are you?
Authorization  -> What may you do?
```

A user can be correctly authenticated and still be forbidden from accessing a resource.

Example:

```text
Alice logs in
    ↓
identity known
    ↓
Alice requests Bob's private profile
    ↓
server checks ownership/permission
    ↓
deny
```

The login being valid does not make the later request authorized.

## 2. Subject, object and action

A useful access-control model asks three questions:

```text
Subject -> who is making the request?
Object  -> which resource is targeted?
Action  -> what operation is requested?
```

Example:

```text
Subject: user 1
Object:  profile 1
Action:  read
```

The authorization decision is about the combination, not just the URL.

## 3. Object-level authorization

Suppose an application has:

```text
/profiles/1
/profiles/2
```

The fact that user 1 knows that profile 2 exists must not automatically grant access to it.

The server should check something like:

```text
is requester owner?
        OR
does requester have an allowed privileged role?
```

This is object-level authorization.

## 4. IDOR / BOLA concept

**IDOR** is commonly used for insecure direct object reference problems. In API security, **BOLA** means Broken Object Level Authorization.

The core defensive lesson is simple:

> Never assume that an object identifier is an authorization control.

Changing an ID, UUID, filename or path should not bypass a server-side permission check.

Identifiers locate resources. Authorization decides whether the requester may access them.

## 5. Function-level authorization

Access control also applies to operations.

For example:

```text
/profile        -> normal user function
/admin/report   -> administrator function
```

Hiding an admin button in the browser is not enough. A client can send HTTP requests without using the visible UI.

Therefore the server must enforce:

```text
request -> identify subject -> check permission -> perform action
```

This is the key idea behind function-level authorization.

## 6. Client-side checks are not security boundaries

JavaScript may hide or disable controls for user experience:

```text
if not admin:
    hide admin button
```

But client-side state is controlled by the client.

Security-sensitive authorization belongs on the trusted server side.

A useful rule:

```text
client-side check -> UX
server-side check -> security decision
```

Client-side controls can complement security but must not be the only enforcement.

## 7. 401 vs 403

A useful beginner distinction:

### 401 Unauthorized
Despite the historical name, it generally means authentication credentials are missing, invalid or insufficient to establish the required identity.

Think:

```text
"I do not have a valid authenticated identity for this request."
```

### 403 Forbidden
The server understands the request/identity but refuses the operation.

Think:

```text
"I know who you are, but you cannot do this."
```

Real applications can intentionally vary error behavior to avoid leaking information, so do not treat status codes as the entire security model.

## 8. Role-based access control

A simple RBAC model assigns roles:

```text
student -> normal features
analyst -> analysis features
admin   -> administrative features
```

Then permissions are associated with roles.

RBAC can simplify policy management, but role checks alone do not solve every problem. Object ownership may still matter.

For example, two users can have the same role while still being allowed to access only their own private records.

## 9. Ownership checks

A common policy:

```text
allow if:
    requester owns object
    OR requester has explicit administrative permission
otherwise:
    deny
```

The exact policy depends on the application.

The important point is that ownership must come from trusted server-side data, not from a client claim such as:

```text
owner=true
```

## 10. Deny by default

A strong mental model is:

```text
no matching permission
        ↓
       deny
```

Instead of granting access unless something blocks it, define what is allowed and reject requests that do not meet the policy.

This reduces accidental exposure when new routes or resources are added.

## 11. Local Flask lab

Install Flask if needed:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

Run:

```bash
python safe_app.py
```

The application listens only on:

```text
127.0.0.1:5000
```

The `X-Training-User` header is only a convenient local identity selector. It is **not real authentication** and must never be copied as an authentication design for production software.

## 12. Training identities

The demo contains:

```text
1  -> student    -> user
2  -> analyst    -> user
99 -> admin-demo -> admin
```

Check your selected training identity:

```bash
curl -i -H "X-Training-User: 1" http://127.0.0.1:5000/me
```

Without the header:

```bash
curl -i http://127.0.0.1:5000/me
```

Observe the status-code difference.

## 13. Object-level check

User 1 requests their own profile:

```bash
curl -i -H "X-Training-User: 1" \
  http://127.0.0.1:5000/profiles/1
```

Expected: allowed.

User 1 requests profile 2:

```bash
curl -i -H "X-Training-User: 1" \
  http://127.0.0.1:5000/profiles/2
```

Expected: `403 Forbidden`.

The important lesson is not “change an ID to attack something.” The lesson is that the server must perform the ownership/permission check even when the client supplies a valid object identifier.

## 14. Administrative function check

Normal user:

```bash
curl -i -H "X-Training-User: 1" \
  http://127.0.0.1:5000/admin/report
```

Expected: `403`.

Training admin:

```bash
curl -i -H "X-Training-User: 99" \
  http://127.0.0.1:5000/admin/report
```

Expected: allowed.

This demonstrates function-level authorization.

## 15. Why checking only the frontend fails

Imagine the frontend never displays a link to `/admin/report` for a normal user.

That is useful UI behavior, but the route still needs the server-side role check because HTTP requests can be created independently of the UI.

```text
hidden button != protected endpoint
```

## 16. Authorization should be consistent

A common engineering problem is protecting one route but forgetting another route that reaches the same resource.

Think in terms of policy:

```text
every protected read
every protected write
every protected delete
every privileged action
        ↓
authorization decision
```

Centralized framework helpers, middleware or policy layers can reduce duplicated and inconsistent checks, depending on the technology.

## 17. Do not trust client-supplied roles

Unsafe design idea:

```text
POST /report
role=admin
```

The server must not grant privileges merely because the client says it has a role.

Role and ownership information should be derived from trusted authenticated/session/server-side state.

## 18. Logging access-control decisions

Useful defensive logs may include:

- authenticated subject identifier
- requested resource/action
- allow/deny result
- timestamp
- relevant policy reason

Avoid unnecessarily logging secrets such as passwords, session tokens or sensitive personal data.

Repeated denied requests can be useful security telemetry, but context is required before calling behavior malicious.

## 19. Access-control review checklist

For a protected endpoint, ask:

```text
1. Who is the requester?
2. What resource/action is requested?
3. Where does permission data come from?
4. Is the check server-side?
5. Is object ownership checked?
6. Is role/function permission checked?
7. What happens when no rule allows access?
8. Are all equivalent routes protected consistently?
9. Is denial logged appropriately?
10. Are tests covering allowed and denied cases?
```

## Exercises

1. Start the local Flask app.
2. Request `/me` without a training identity and inspect the status.
3. Access user 1's own profile.
4. Confirm user 1 cannot access user 2's profile.
5. Confirm a normal user cannot access `/admin/report`.
6. Confirm the training admin can access the admin report.
7. Locate the object-level authorization check in the source.
8. Locate the function-level authorization check.
9. Explain why hiding an admin button is insufficient.
10. Write three test cases: allowed owner, denied non-owner, allowed admin.

## Questions

1. Authentication vs authorization?
2. What are subject, object and action?
3. Why is an object ID not an authorization mechanism?
4. What is the defensive idea behind IDOR/BOLA?
5. Why must privileged functions be protected server-side?
6. What is the practical difference between 401 and 403?
7. Why might RBAC still need ownership checks?
8. What does deny-by-default mean?
9. Why should roles not come directly from client input?
10. Why should both allowed and denied paths be tested?

## Main takeaway

```text
authenticated identity
        ↓
subject + object + action
        ↓
server-side policy check
        ↓
allow or deny
        ↓
consistent logging/testing
```

Authentication tells the application who the requester is. Authorization must still decide what that identity may do on every protected operation.
