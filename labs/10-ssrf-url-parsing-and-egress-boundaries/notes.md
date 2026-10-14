# Day 10 — SSRF Foundations, URL Parsing, Redirects and Egress Boundaries

[English](notes.md) · [Türkçe](notes.tr.md)

**Goal:** extend Days 8–9 trust-boundary thinking to server-initiated outbound HTTP requests.

**Important:** the Python example only evaluates a URL policy; it makes NO HTTP or DNS requests and is not a production-ready SSRF defense.

## 1. SSRF threat model

Server-Side Request Forgery occurs when untrusted input influences server-side requests to unintended destinations. A server may have access to internal services or networks that an external browser cannot reach. The risk is where the request is made, not simply that a URL contains strange text.

## 2. URL authority and parser boundaries

A URL contains scheme, authority/hostname, optional port, path, query and fragment. Decisions should operate on a parsed authority, never naïve substring tests. For example, the intended hostname appearing inside another hostname is not authorization.

## 3. Scheme and port restrictions

Allow only protocols and ports required by the feature. This exercise accepts HTTPS and port 443 only. A generic URL fetcher may unintentionally expose other protocols, ports and services.

## 4. Userinfo, fragments and ambiguity

URLs can contain userinfo, fragments, Unicode, percent-encoding and multiple representations of hosts. Reject unnecessary syntax and parse consistently. Do not build security policy from browser-looking display text.

## 5. Allowlist versus blocklist

Known partner endpoints are better represented by an exact host allowlist. Blocklists of suspicious hostnames miss alternate representations and future destinations. Exact matching reduces ambiguity but does not eliminate runtime DNS risk.

## 6. DNS resolution and rebinding

A DNS name may resolve to unexpected internal, loopback or link-local addresses, or change between validation and connection. Production clients must validate actual resolved and connected IPs, account for IPv4/IPv6 and DNS rebinding, and enforce network egress restrictions. The demo deliberately does not connect.

## 7. Redirect handling

An allowlisted URL can redirect to a disallowed destination. Redirect targets require the same policy or redirects should be disabled. Never validate only the first hop and allow a general-purpose HTTP client to follow arbitrary destinations.

## 8. Network segmentation and egress controls

Host validation belongs with lower-level controls: outbound firewall rules, network namespace isolation, restricted DNS resolution and credentials limited to the requested task. Defense in depth matters if app-layer checks fail.

## 9. Cloud metadata and sensitive internals

Internal metadata services, admin dashboards and loopback interfaces are examples of resources a server may reach but clients should not choose arbitrarily. This lab never sends traffic to any such endpoints; reason about their protection conceptually.

## 10. Authorization, logging and privacy

Even an allowed outbound request must fit the authenticated user's task and resource permissions. Log destination policy decisions and request IDs without exposing sensitive tokens or URLs. A URL allowlist is not a substitute for authorization.

## Local exercise

Python 3 standard library only:

```bash
python3 url_policy.py
python3 -m unittest -v test_url_policy.py
```

The training allowlist uses the reserved names `reports.example.test` and `status.example.test`. It does not connect to them; it checks parsed hostname, scheme, port and syntax only. There is **no** DNS resolution, redirect follow-up or HTTP fetch.

### Decision flow

```text
untrusted URL
   ↓
parse + syntax validation
   ↓
scheme / port / exact host allowlist
   ↓
[training only: policy decision]
   ↓
production needs DNS/IP/redirect/egress enforcement
```

### Mini challenges

1. Explain why `reports.example.test.evil.test` cannot pass exact-host matching.
2. Design a policy recheck for every redirect destination, without implementing a network fetch.
3. Draw required production controls against DNS rebinding and IPv6 private-address access.
4. Explain why real tokens and sensitive full URLs should not be logged.

### Exercises

1. Identify URL components.
2. Distinguish hostname from path.
3. Execute the tests.
4. Examine protocol restriction.
5. Explain port checks.
6. Explain userinfo rejection.
7. Explain suffix/subdomain confusion.
8. Discuss IP literals.
9. Describe DNS rebinding.
10. Model redirect checks.
11. Design egress rules.
12. Write a short SSRF risk assessment.

### Review questions

1. Define SSRF.
2. What trust boundary is crossed?
3. Why parse hostnames?
4. Why are substring checks weak?
5. Why an exact allowlist?
6. Why not only a blocklist?
7. Why restrict schemes?
8. What is URL userinfo?
9. What is DNS rebinding?
10. Why consider IPv6?
11. Why must redirects be checked?
12. What does network egress control add?
13. Why are metadata services sensitive?
14. Does URL policy replace authorization?
15. Why is this demo not production-ready?

**Takeaway:** SSRF defense involves parser correctness, runtime destination validation and network egress boundaries—not simply blocking suspicious URL strings.
