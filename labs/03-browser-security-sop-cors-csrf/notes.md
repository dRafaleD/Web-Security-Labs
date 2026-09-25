# Day 3 — Browser Security, Same-Origin Policy, CORS and CSRF Foundations

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand how the browser separates web origins, why cross-origin access is restricted, how CORS selectively relaxes those restrictions, and why automatic credential handling matters for CSRF.

This lab builds concepts before later vulnerability-focused exercises.

## 1. What is an origin?

For browser security, an origin is based on:

```text
scheme + host + port
```

Examples:

```text
https://example.com
https://api.example.com
http://example.com
https://example.com:8443
```

These are not all the same origin.

Changing the scheme, host or effective port can produce a different origin.

## 2. Same-Origin Policy

The Same-Origin Policy (SOP) is a major browser security boundary.

In simplified terms, JavaScript running under one origin is restricted from freely reading sensitive content belonging to another origin.

Without such a boundary, a malicious page could potentially read data from other sites the user is logged into.

SOP is more nuanced than "cross-origin requests are impossible." Browsers can send many cross-origin requests in normal web behavior, but reading responses from script is restricted unless the applicable rules allow it.

## 3. Same-site vs same-origin

These terms are related but not identical.

For now remember:

```text
same-origin -> strict scheme + host + port origin comparison
same-site   -> a broader site concept used by mechanisms such as SameSite cookies
```

Later labs can go deeper into site calculation and cookie scope.

## 4. CORS

CORS stands for Cross-Origin Resource Sharing.

It is a browser-controlled mechanism that allows a server to state which origins may read certain cross-origin responses.

A response can contain:

```http
Access-Control-Allow-Origin: https://example-client.test
```

This does not "disable web security." It communicates a specific cross-origin policy to compatible browsers.

## 5. Simple conceptual example

Suppose JavaScript runs on:

```text
https://app.example
```

and requests:

```text
https://api.example
```

These are different origins.

Whether script can read the response depends on browser rules and the API's CORS response.

## 6. Preflight requests

Some cross-origin requests cause the browser to send an OPTIONS request first.

Conceptually:

```http
OPTIONS /api/profile HTTP/1.1
Origin: https://app.example
Access-Control-Request-Method: PUT
```

The server can answer with policy information such as:

```http
Access-Control-Allow-Origin: https://app.example
Access-Control-Allow-Methods: GET, PUT
```

This preliminary check is commonly called a **preflight**.

Not every cross-origin request requires one.

## 7. The Origin header

Browsers can send:

```http
Origin: https://app.example
```

The server can use it when making CORS-related decisions.

Do not confuse `Origin` with `Host`:

```text
Host   -> which server/virtual host the request targets
Origin -> security origin associated with the initiating context
```

## 8. Credentials and cookies

Browsers can automatically attach cookies to requests when cookie rules allow them.

That convenience creates an important security question:

> If a browser sends a user's credentials automatically, how does the server know an unwanted cross-site action was not triggered by another site?

This leads into CSRF.

## 9. CSRF concept

CSRF means Cross-Site Request Forgery.

The core risk appears when:

1. a user is authenticated to a site,
2. the browser automatically includes relevant credentials,
3. another site can cause a state-changing request,
4. the target application does not sufficiently verify that the action was intended.

A simplified defensive view:

```text
authenticated request
        +
state-changing action
        +
request origin/intention validation
```

Applications commonly use controls such as CSRF tokens, SameSite cookies and origin-related validation depending on their architecture.

No single mechanism should be assumed to solve every design.

## 10. CORS and CSRF are not the same thing

A common beginner mistake is treating them as the same problem.

**CORS** primarily controls whether browser JavaScript can read/use cross-origin responses under CORS rules.

**CSRF** concerns causing an authenticated user's browser to perform an unwanted action.

Therefore:

```text
CORS != CSRF protection
```

They can interact with browser behavior, but they solve different security problems.

## 11. Local origin experiment

Run two harmless local servers in separate directories:

Terminal 1:

```bash
python3 -m http.server 8000
```

Terminal 2:

```bash
python3 -m http.server 9000
```

Now compare:

```text
http://127.0.0.1:8000
http://127.0.0.1:9000
```

Same host, but different ports mean different origins.

Open Developer Tools and observe the URLs and ports. The goal is to understand origin identity, not to bypass browser controls.

## 12. Header observation lab

Open a normal site or your own local application and inspect requests in Developer Tools.

Look for these headers when present:

```text
Origin
Referer
Access-Control-Allow-Origin
Access-Control-Allow-Methods
Vary
```

Not every response will contain CORS headers. Their absence can be completely normal.

Record sanitized observations only.

## 13. Build a harmless CORS demo server

Create `cors_server.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

ALLOWED_ORIGIN = "http://127.0.0.1:8000"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.end_headers()
        self.wfile.write(b'{"message":"CORS training response"}')

HTTPServer(("127.0.0.1", 9000), Handler).serve_forever()
```

Run it:

```bash
python3 cors_server.py
```

Inspect the response:

```bash
curl -i http://127.0.0.1:9000/
```

Find:

```http
Access-Control-Allow-Origin: http://127.0.0.1:8000
```

Remember: curl displays the header, but CORS enforcement is a browser behavior.

## 14. Security headers are policy signals

Browser-facing security often relies on response headers to communicate policy.

At this stage recognize the names:

```text
Content-Security-Policy
Strict-Transport-Security
X-Content-Type-Options
Referrer-Policy
Access-Control-Allow-Origin
```

We will study their details separately rather than trying to memorize them now.

## 15. Mini exercises

### A — Origin comparison

Decide whether each pair has the same origin:

```text
https://example.com       vs https://example.com/profile
https://example.com       vs http://example.com
https://example.com       vs https://api.example.com
https://example.com       vs https://example.com:8443
```

### B — CORS header

Run the local CORS server and identify the allowed origin.

### C — Browser inspection

Find an `Origin` or CORS-related header in a request/response if one naturally appears. Do not force requests against third-party systems.

### D — Reasoning

Explain why allowing JavaScript to read every other logged-in website's responses would be dangerous.

## Questions

1. Which three components define an origin?
2. Why does the Same-Origin Policy exist?
3. Are all cross-origin network requests completely blocked by SOP?
4. What does `Access-Control-Allow-Origin` communicate?
5. What is a CORS preflight?
6. What is the difference between `Host` and `Origin`?
7. Why can automatically attached cookies matter for CSRF?
8. Why are CORS and CSRF different concepts?
9. Are ports 8000 and 9000 on the same host the same origin?
10. Why does seeing a CORS header with curl not mean curl is enforcing CORS?

## Main takeaway

Browser security is strongly based on boundaries and trust decisions:

```text
origin
  ↓
browser security boundary
  ↓
cross-origin request
  ↓
CORS policy when applicable
  ↓
credentials/cookies
  ↓
server-side authorization and anti-CSRF controls
```

Understanding these boundaries makes later XSS, CSRF, CORS-misconfiguration and authentication labs much easier to reason about.
