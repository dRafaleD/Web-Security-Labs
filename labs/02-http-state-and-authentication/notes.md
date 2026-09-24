# Day 2 — HTTP Methods, Headers, Cookies, Sessions and Authentication

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Move beyond simply recognizing an HTTP request. This lab studies methods, headers, cookies, sessions, authentication, authorization, browser storage, and important security attributes.

The exercises are observation-focused and use your browser or a local server.

## 1. HTTP methods

Common methods include:

| Method | Typical purpose |
| --- | --- |
| GET | Retrieve a resource |
| POST | Submit/create data |
| PUT | Replace/update a resource |
| PATCH | Partially update a resource |
| DELETE | Request deletion |
| HEAD | Request headers without a response body |
| OPTIONS | Ask which communication options/methods are available |

The method name alone does **not** provide authorization. A server must still decide whether the current user is allowed to perform the requested action.

## 2. Request anatomy

A conceptual request:

```http
POST /login HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
User-Agent: ExampleBrowser

username=eren&password=example
```

Notice the separation:

```text
request line
headers

body
```

Sensitive credentials above are only dummy training data.

## 3. Useful request headers

### Host

Identifies the target host:

```http
Host: example.com
```

### User-Agent

Describes the client software.

### Accept

Describes response formats the client can handle.

### Content-Type

Describes the format of the body:

```http
Content-Type: application/json
```

### Authorization

Can carry authentication credentials or tokens depending on the scheme.

Never commit real tokens, cookies, passwords, API keys, or session identifiers to this repository.

## 4. Useful response headers

Examples:

```http
Content-Type: text/html
Content-Length: 1234
Cache-Control: no-store
Set-Cookie: session=...
```

Response headers can influence browser behavior, caching, cookies, and security controls.

Later labs can examine headers such as Content-Security-Policy and Strict-Transport-Security in more detail.

## 5. Cookies

A server can ask the browser to store a cookie:

```http
Set-Cookie: theme=dark
```

The browser may later return it:

```http
Cookie: theme=dark
```

Cookies can store preferences, identifiers, or session-related values.

A cookie is not automatically secret merely because the browser stores it.

## 6. Important cookie attributes

### Secure

```http
Set-Cookie: session=example; Secure
```

Tells the browser to send the cookie only over secure HTTPS connections (with normal browser rules).

### HttpOnly

```http
Set-Cookie: session=example; HttpOnly
```

Prevents normal client-side JavaScript from reading the cookie. This is especially relevant when reducing the impact of some XSS scenarios.

### SameSite

Examples:

```text
SameSite=Strict
SameSite=Lax
SameSite=None
```

SameSite influences when cookies are sent with cross-site requests and is relevant to CSRF defenses.

`SameSite=None` is normally paired with `Secure` in modern browsers.

## 7. Cookies vs sessions

These terms are related but not identical.

A common design:

```text
Browser
   |
   | Cookie: session_id=abc123
   v
Server
   |
   | abc123 -> server-side session data
   v
Logged-in state
```

The browser may hold only an identifier while the meaningful session state lives on the server.

Other architectures can use self-contained tokens, so do not assume every application works exactly the same way.

## 8. Authentication vs authorization

These are fundamental security concepts.

**Authentication** asks:

```text
Who are you?
```

**Authorization** asks:

```text
What are you allowed to do?
```

Example:

A user can be successfully authenticated but still not be authorized to access an administrator page.

This distinction becomes extremely important when studying access-control vulnerabilities later.

## 9. Browser lab — inspect cookies and headers

Use a normal site you are comfortable inspecting or your own local application.

Open Developer Tools:

```text
Network -> select a request -> Headers
```

Identify:

- method
- path
- request headers
- response headers
- status code
- Content-Type

Then inspect the browser's storage/application panel and look at cookies for the selected origin.

Do **not** publish or screenshot real session values into the repository.

Record only attribute names or sanitized examples.

## 10. Local HTTP lab

Create an empty practice directory and run:

```bash
python3 -m http.server 8000
```

Then:

```bash
curl -i http://127.0.0.1:8000/
```

The `-i` option displays response headers together with the body.

Try a HEAD request:

```bash
curl -I http://127.0.0.1:8000/
```

Try verbose mode:

```bash
curl -v http://127.0.0.1:8000/
```

Verbose output helps distinguish lines sent by the client from lines received from the server.

## 11. Compare GET and HEAD

Run:

```bash
curl -i http://127.0.0.1:8000/
curl -I http://127.0.0.1:8000/
```

Compare:

- status
- headers
- response body

The HEAD method is designed to return the headers corresponding to a GET request without transferring the response body.

## 12. Build a tiny cookie lab

Create `cookie_server.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header(
            "Set-Cookie",
            "training_session=demo123; HttpOnly; SameSite=Lax"
        )
        self.end_headers()
        self.wfile.write(b"Harmless cookie lab\n")

HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

Run:

```bash
python3 cookie_server.py
```

Visit:

```text
http://127.0.0.1:8000/
```

Inspect the response and cookie attributes in Developer Tools.

This is deliberately a dummy cookie. It is not authentication and contains no secret.

## 13. Inspect with curl

Headers only:

```bash
curl -I http://127.0.0.1:8000/
```

If the tiny server does not implement HEAD, use:

```bash
curl -i http://127.0.0.1:8000/
```

Look for:

```http
Set-Cookie: training_session=demo123; HttpOnly; SameSite=Lax
```

## 14. Security reasoning

Consider a hypothetical session cookie:

```http
Set-Cookie: session=abc; Secure; HttpOnly; SameSite=Lax
```

Ask what each attribute contributes.

Do not think of any one attribute as a complete security solution:

- `Secure` concerns transport of the cookie.
- `HttpOnly` limits script access.
- `SameSite` controls some cross-site sending behavior.
- the server still needs strong session management and authorization.

Security comes from multiple controls working together.

## 15. Mini exercises

### A — Headers

Use Developer Tools and identify five request or response headers. Write one sentence describing the purpose of each.

### B — Methods

Compare GET and HEAD against your local server.

### C — Cookie

Run the local cookie server and identify:

- cookie name
- cookie value
- HttpOnly
- SameSite

Why is `Secure` intentionally missing from this HTTP-only localhost exercise?

### D — Authentication vs authorization

Explain this scenario:

```text
Alice successfully logs in.
Alice requests /admin.
Server returns 403 Forbidden.
```

Which step concerns authentication and which concerns authorization?

## Questions

1. What is the difference between GET and POST conceptually?
2. Does using POST make data automatically secure?
3. What is the difference between a request header and response header?
4. What does `Set-Cookie` do?
5. What is the purpose of `HttpOnly`?
6. What is the purpose of `Secure`?
7. Why is SameSite relevant to cross-site requests?
8. What is the difference between authentication and authorization?
9. Why should real session IDs never be committed to GitHub?
10. Why is learning normal HTTP behavior useful before studying vulnerabilities?

## Main takeaway

Web security starts with understanding state and trust.

```text
request
  ↓
method + path + headers + body
  ↓
authentication
  ↓
session/state
  ↓
authorization decision
  ↓
response
```

When you later investigate web vulnerabilities, these same pieces will help you identify where the application's assumptions and security controls fail.
