# Day 1 — HTTP Fundamentals and Request/Response Analysis

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand the HTTP request/response model and learn to inspect normal browser traffic before studying web vulnerabilities.

## Basic model

When you open a web page:

```text
Browser
   |
   | HTTP request
   v
Web server
   |
   | HTTP response
   v
Browser
```

HTTPS protects HTTP traffic in transit with TLS, but the application still works with HTTP concepts such as methods, paths, headers, status codes, and bodies.

## A simple HTTP request

Conceptually:

```http
GET / HTTP/1.1
Host: example.com
User-Agent: Browser
Accept: text/html
```

Important parts:

- **Method:** what action is requested, such as `GET` or `POST`
- **Path:** which resource is requested
- **Headers:** metadata about the request
- **Body:** optional data sent with the request

## A simple HTTP response

Conceptually:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>...</html>
```

Important parts:

- **Status code:** result of the request
- **Headers:** metadata about the response
- **Body:** returned content

Common status-code groups:

```text
2xx -> success
3xx -> redirection
4xx -> client-side request problem
5xx -> server-side error
```

## Lab 1 — Browser Developer Tools

Open your browser's Developer Tools and select the **Network** tab.

Visit:

```text
https://example.com/
```

Select the document request and inspect:

- Request URL
- Request Method
- Status Code
- Request Headers
- Response Headers

Do not change anything yet. The first goal is simply to read the conversation between browser and server.

## Lab 2 — Compare requests

Reload the page and look at the requests for the document and any additional resources.

Ask:

- Which request loads the main document?
- Which HTTP method is used?
- Which status code is returned?
- What is the `Content-Type`?
- Which side sends the `User-Agent` header?

## Optional local exercise

Start a simple local server in an empty practice directory:

```bash
python3 -m http.server 8000
```

Visit:

```text
http://127.0.0.1:8000/
```

Now inspect the local request in Developer Tools.

Because the server is running on your own machine, this is a safe target for basic request observation.

## Burp Suite connection

Later labs can use Burp Suite as an intercepting proxy.

For now remember the flow:

```text
Browser -> request -> server
Browser <- response <- server
```

A proxy can sit between these sides so the traffic can be inspected during authorized testing.

## Questions

1. What HTTP method loaded the page?
2. What status code did you receive?
3. Which header describes the returned content type?
4. What is the difference between a request header and a response header?
5. What does HTTPS add to HTTP communication?

## Main takeaway

Before learning vulnerabilities, become comfortable reading normal web traffic.

For every request, ask:

```text
Who sent it?
What method was used?
What path was requested?
Which headers were included?
Was there a body?
What did the server return?
```

These questions become the foundation for later web security analysis.
