# Day 5 — Cookies, Sessions and Authentication Security

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand how browser cookies and server-side sessions maintain login state, how authentication differs from authorization, and which cookie attributes help reduce common session risks.

This lab uses only a small local Flask application.

## 1. Why sessions exist

HTTP is stateless at the protocol level. A server does not automatically remember that two requests belong to the same logged-in user.

A common pattern is:

```text
login request
    ↓
server verifies identity
    ↓
server creates session state
    ↓
browser receives session cookie
    ↓
future requests send cookie
    ↓
server links request to session
```

## 2. Cookie anatomy

A response may contain:

```http
Set-Cookie: session=example; Path=/; HttpOnly; SameSite=Lax
```

Important attributes include:

- **Name / Value** — cookie identifier and stored value.
- **Domain** — which hosts are eligible to receive it.
- **Path** — path scope.
- **Expires / Max-Age** — lifetime.
- **Secure** — send over HTTPS according to browser rules.
- **HttpOnly** — blocks normal JavaScript access.
- **SameSite** — influences cross-site sending behavior.

## 3. HttpOnly

```http
HttpOnly
```

This tells the browser not to expose the cookie through normal client-side JavaScript APIs.

It is especially useful as defense in depth against session theft in some XSS scenarios.

It does **not** fix XSS itself.

## 4. Secure

```http
Secure
```

The browser should send the cookie only over secure HTTPS transport.

Important:

> Secure does not encrypt the cookie value by itself.

TLS protects the transport.

For our localhost HTTP lab, we intentionally do not enable Secure because the demo runs over plain HTTP.

## 5. SameSite

Common values:

```text
SameSite=Strict
SameSite=Lax
SameSite=None
```

SameSite controls some cross-site cookie behavior and can help reduce CSRF risk.

It should be understood as one part of a broader CSRF/session defense strategy.

## 6. Authentication vs authorization

Authentication:

```text
Who are you?
```

Authorization:

```text
What are you allowed to do?
```

Example:

```text
user logs in successfully
        ↓
authenticated
        ↓
user requests /admin
        ↓
server checks role
        ↓
403 if not authorized
```

A successful login should never automatically imply permission to every resource.

## 7. Session lifecycle

A healthy mental model:

```text
create
  ↓
use
  ↓
rotate when appropriate
  ↓
expire / logout
  ↓
invalidate
```

Security bugs often appear when sessions live too long, are not invalidated correctly, or authorization decisions depend on weak assumptions.

## 8. Local Flask lab

Install Flask in a virtual environment if needed:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000/
```

This application uses only a dummy local login and contains no real credentials.

## 9. Inspect the session cookie

Login using the training form.

In Developer Tools:

```text
Application / Storage -> Cookies
```

Inspect:

- cookie name
- Path
- HttpOnly
- SameSite
- Secure

Do not publish real cookies from real services into this repository.

## 10. Observe with curl

Request the home page:

```bash
curl -i http://127.0.0.1:5000/
```

Submit the dummy login and save cookies:

```bash
curl -i -c cookies.txt   -X POST   -d "username=student"   http://127.0.0.1:5000/login
```

Then reuse the local training cookie:

```bash
curl -i -b cookies.txt http://127.0.0.1:5000/profile
```

This demonstrates how a client persists state between requests.

## 11. Logout

Call:

```text
/logout
```

Then request `/profile` again.

Expected behavior: the session no longer identifies you as logged in.

This illustrates why session invalidation is part of authentication security.

## 12. Session fixation concept

Session fixation is a class of weakness where an application improperly allows an attacker-known session identifier to remain valid across authentication.

Defensive principle:

> Authentication should not simply promote an untrusted pre-authentication session into a privileged authenticated session without appropriate session handling.

Modern frameworks often provide safer session mechanisms, but developers must still understand the lifecycle.

## 13. Session ID secrecy

If a session identifier functions as a bearer credential, possession of it may be enough to act as that session.

Therefore:

- do not log sensitive session IDs unnecessarily,
- do not commit them to GitHub,
- protect them in transit,
- expire/invalidate them correctly,
- scope cookies appropriately.

## 14. Password handling note

Our demo intentionally avoids implementing real password storage.

Real applications should not store plaintext passwords. Password storage requires well-established password-hashing schemes and secure authentication design, which will be a separate topic.

## 15. Mini exercises

1. Login to the local app.
2. Find the session cookie in DevTools.
3. Verify HttpOnly and SameSite.
4. Explain why Secure is disabled in this HTTP localhost demo.
5. Use curl with a cookie jar to access `/profile`.
6. Logout and verify the authenticated state disappears.
7. Explain the difference between authentication and authorization.
8. Explain why copying real session values into notes would be dangerous.

## Questions

1. Why does a web application need session state?
2. What does HttpOnly protect against?
3. What does Secure actually require?
4. Does SameSite replace all CSRF defenses?
5. What is the difference between authentication and authorization?
6. Why should a session be invalidated on logout?
7. What is the basic idea behind session fixation?
8. Why can a session ID be security-sensitive?
9. Why should real passwords not be stored in plaintext?
10. Why is session lifecycle more important than only checking the login page?

## Main takeaway

Authentication security is a lifecycle, not a single login request:

```text
identity verification
      ↓
session creation
      ↓
safe cookie attributes
      ↓
authorization checks
      ↓
rotation / expiry
      ↓
logout / invalidation
```
