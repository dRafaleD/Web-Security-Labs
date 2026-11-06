# Day 21 — CSRF, SameSite Cookies and Origin Checks

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning goal
Learn why a user's authenticated browser can be tricked into making a state-changing request (CSRF), and how anti-CSRF tokens, Origin validation, and SameSite cookies complement one another.

## Core concepts
- Authentication cookies may be attached by the browser automatically; this is what makes cross-site requests risky.
- SameSite=Lax or Strict reduces certain cross-site cookie submissions but is not a universal substitute for CSRF defenses.
- An unpredictable token tied to a user's session is validated **server-side** before a state change.
- Origin/Referer checks can be defense in depth; missing or unusual headers require an explicit policy.
- XSS can undermine CSRF defenses. Do not treat CSRF tokens as XSS protection.

## Offline demo
`csrf_demo.py` models a request policy with entirely synthetic values; it does **not** host a web service or make requests.

```bash
python3 csrf_demo.py
```

## Tasks
1. Identify which inputs are controlled by the browser, user, and server.
2. Change the allowed origin; predict which cases fail.
3. Add a negative case for a missing Origin header.
4. Describe how synchronizer tokens differ from SameSite.
5. Name a limitation of this toy model.

## Safety
No production service, attacker page, or credential collection. This exercise demonstrates validation logic only.
