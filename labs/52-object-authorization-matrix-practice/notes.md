# Day 52 — Practice Day: Object Authorization and Response Contracts

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](authorization_matrix.py)

Practice object-level authorization using a local policy function. Authentication is represented by a trusted user registry. GET permits same-tenant owners and administrators; PATCH permits only owners. Missing and concealed resources use the same 404 status according to this fictional application's policy.

| Request | Status |
|---|---:|
| Owner reads own record | 200 |
| Owner patches own record | 200 |
| Other member reads record | 404 |
| Same-tenant admin reads | 200 |
| Admin patches another owner's record | 403 |
| Cross-tenant read | 404 |
| Unknown user | 401 |
| Unsupported method | 405 |

**Exercises:** Predict all 15 responses. Add a second record in tenant a, write owner/non-owner assertions, and compare denied reads with missing records. Explain why matching status codes alone cannot guarantee indistinguishable responses. Sketch how a real backend would use authenticated identity and database-scoped authorization.

Expected summary: 15 cases + 1 response-consistency check passed. No HTTP server, actual identifiers, requests to third-party systems, or data mutations. This is a toy policy, not a universal HTTP status-code convention.

## Run
```bash
python3 labs/52-object-authorization-matrix-practice/authorization_matrix.py
```
