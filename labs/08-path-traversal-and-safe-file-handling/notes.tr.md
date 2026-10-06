# Gün 8 — Path Traversal, File Handling ve Güvenli Resource Mapping

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Understand why file paths are a security boundary, how path traversal arises, why “user input + filesystem path” is dangerous, and how allowlisted resource mapping can reduce risk.

This day combines:

1. filesystem paths in web apps,
2. path traversal root cause,
3. normalization/canonicalization concepts,
4. allowlist-based resource mapping,
5. safe download patterns,
6. file extension/content-type confusion,
7. least-privilege filesystem access,
8. error handling and logging,
9. local Flask testing,
10. code-review and mini challenge.

## 1. Where paths enter a web app

Applications often map HTTP input to files:

```text
request
  ↓
parameter
  ↓
application path logic
  ↓
filesystem
  ↓
response
```

Examples:

- document download,
- avatar/image retrieval,
- template loading,
- report export,
- attachment serving.

The important question is:

> Does user-controlled input directly influence a filesystem path?

## 2. Root cause of path traversal

A dangerous pattern is:

```python
candidate = BASE_DIR / user_input
```

followed by opening the result without a trustworthy boundary check.

The problem is not one magical string. The problem is that user input can influence **where** the application looks.

Think:

```text
trusted base directory
        +
untrusted path component
        ↓
potentially different resource
```

## 3. Relative paths

Relative paths are resolved from another location.

Examples:

```text
files/report.txt
../config.txt
../../other/location
```

Dot segments can change the resolved location.

A security review should ask:

- Is the input a filename or a path?
- Are separators accepted?
- Are `..` segments possible?
- Is normalization performed?
- Is the final resolved path still inside the intended base?

## 4. Canonicalization / normalization

Two path strings can refer to the same location after normalization.

Conceptually:

```text
base/a/../b.txt
        ↓ normalize
base/b.txt
```

Security decisions should be based on the **resolved/canonical destination**, not only the raw string.

However, canonicalization alone is not a complete design. Symlinks, platform differences and race conditions can complicate filesystem checks.

## 5. Better design: logical identifiers

Instead of letting the client choose arbitrary filesystem paths, map a small logical key to a trusted file.

Example:

```python
ALLOWED_FILES = {
    "public": "public.txt",
    "guide": "guide.txt",
}
```

The client sends:

```text
name=guide
```

The server chooses:

```text
guide.txt
```

This changes the trust model:

```text
user chooses logical key
      ↓
application chooses trusted path
```

## 6. Local training app

Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python safe_file_demo.py
```

The app listens only on:

```text
127.0.0.1:5000
```

Routes:

```text
/unsafe?file=public.txt
/safe?name=public
/download?name=guide
```

## 7. Compare unsafe and safe designs

Unsafe route:

```python
requested = request.args.get("file", "")
candidate = BASE_DIR / requested
```

Safe route:

```python
filename = ALLOWED_FILES.get(name)
```

The key difference is not “one has more validation.”

It is:

```text
unsafe -> user influences path structure
safe   -> user selects from application-defined resources
```

## 8. Why extension checks are weak

A common weak design is:

```text
if path.endswith(".txt"):
    allow
```

Extensions are labels, not trustworthy security boundaries.

Questions:

- Is the resolved file actually where expected?
- Is the file type what the application thinks it is?
- Could an uploaded file be renamed?
- Does downstream software interpret content differently?

Do not treat extension-only checks as a full file security model.

## 9. Content-Type is not file identity

HTTP `Content-Type` helps clients understand response content.

It is not cryptographic proof of what a file is.

Likewise, an upload's client-supplied MIME type can be wrong.

Useful distinction:

```text
filename extension -> naming convention
Content-Type       -> declared media type
actual bytes        -> real content evidence
```

## 10. Safe downloads

Framework helpers such as Flask's `send_from_directory` are preferable to manually concatenating arbitrary paths.

But safe usage still depends on:

- trusted base directory,
- controlled filename selection,
- appropriate response headers,
- authorization.

A download endpoint can be path-safe but still authorization-unsafe.

## 11. Authorization still matters

Imagine two users:

```text
user A -> invoice A
user B -> invoice B
```

Even if path traversal is impossible, the app must still decide whether user A is allowed to download user B's file.

So:

```text
path safety != authorization
```

This connects directly to Day 6.

## 12. File upload connection

Uploads introduce related risks:

- attacker-controlled filename,
- attacker-controlled bytes,
- storage location,
- executable content,
- overwrite collisions,
- public serving,
- malware scanning requirements.

A good design often stores uploads using server-generated identifiers rather than trusting original filenames as storage paths.

## 13. Least-privilege filesystem access

The application process should ideally read/write only directories it actually needs.

Ask:

- Does the web app need access to the whole home directory?
- Does it need write access where it only serves static files?
- Can uploaded content reach executable/template directories?

Filesystem permissions limit impact when application logic fails.

## 14. Symlink awareness

Even a path that appears to remain under a base directory can behave unexpectedly if symlinks are involved.

Conceptually:

```text
base/link -> /some/other/location
```

Therefore filesystem security sometimes requires reasoning about the resolved target, not only string prefix checks.

For beginner labs, prefer simpler allowlisted mappings.

## 15. Error handling

Avoid exposing raw filesystem errors such as full internal paths.

Bad response:

```text
FileNotFoundError: /home/app/private/config.txt
```

Better external behavior:

```text
404 Not Found
```

while internal logs record enough detail for troubleshooting.

## 16. Logging

Useful fields:

- route,
- logical resource key,
- authenticated user,
- allow/deny result,
- timestamp,
- request ID.

Avoid logging secrets or unnecessarily exposing full sensitive paths.

## 17. Mini challenge — safe reports endpoint

Design:

```text
/reports?name=monthly
```

Requirements:

- only `monthly` and `annual` are valid,
- server maps keys to filenames,
- invalid key returns `400`,
- missing file returns `404`,
- no raw internal path is returned,
- access control is checked before the file is served.

Explain which controls address:

- path traversal,
- authorization,
- error leakage.

## 18. Mini challenge — upload design

Without writing upload code yet, design a safe workflow:

```text
user upload
   ↓
server-generated ID
   ↓
type/size validation
   ↓
quarantine/storage directory
   ↓
metadata record
   ↓
authorized retrieval
```

Decide whether the original filename should be used as the actual storage path.

## 19. Code-review checklist

```text
1. Which input influences a file path?
2. Is the client choosing a path or a logical resource?
3. Is normalization/canonicalization relevant?
4. Are symlinks possible?
5. Does the app use a trusted base directory?
6. Are extensions being mistaken for identity?
7. Is authorization checked separately?
8. What filesystem permissions does the app have?
9. Are internal paths exposed in errors?
10. Are uploads stored safely?
```

## Exercises

1. Run the local Flask app.
2. Request the safe `public` resource.
3. Compare unsafe vs allowlisted path construction in source.
4. Explain why path normalization matters.
5. Explain why allowlisting logical keys is stronger than filtering suspicious substrings.
6. Inspect how `send_from_directory` is used.
7. Explain path safety vs authorization.
8. Write the reports mini challenge.
9. Design the upload workflow.
10. Write a least-privilege filesystem policy for the app.

## Questions

1. What is the root cause of path traversal?
2. Why are `..` segments important?
3. What is canonicalization?
4. Why is substring blocking weak?
5. Why are logical IDs useful?
6. Why is extension-only validation insufficient?
7. Why is Content-Type not file identity?
8. Why can symlinks complicate path checks?
9. Why does path safety not replace authorization?
10. Why does filesystem least privilege matter?

## Main takeaway

```text
untrusted request input
        ↓
do not let it define arbitrary paths
        ↓
map logical identifiers to trusted resources
        ↓
authorize
        ↓
serve with least privilege
        ↓
handle errors/logging safely
```


> Türkçe çalışma notu: Bu günün ana fikri “kötü stringleri filtrele” değil, **user'ın path seçmesine izin verme; mümkünse logical ID seçtir, gerçek path'i server belirlesin**. Ayrıca path güvenliği ile authorization'ı ayrı problemler olarak düşün.
