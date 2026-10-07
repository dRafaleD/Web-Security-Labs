# Day 9 — File Upload Security, Content Validation, Storage Isolation and Safe Serving

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand file upload security as a complete pipeline rather than a single extension check.

This day combines upload trust boundaries, filename risks, content validation, size limits, server-generated storage names, isolated storage, hashing, safe retrieval, authorization, quarantine concepts, parser risks, and audit logging.

## 1. Uploads are untrusted data

A useful model:

~~~text
client
  ↓
multipart upload
  ↓
filename + bytes
  ↓
validation
  ↓
storage decision
  ↓
metadata
  ↓
authorized retrieval
~~~

The original filename, Content-Type, and uploaded bytes all come from the client and must be treated as untrusted.

## 2. Original filename is metadata, not a trusted path

A client may upload a file named report.txt.

The server may keep that name for display, but it should not automatically become the physical storage path.

Safer pattern:

~~~text
original name -> metadata
server-generated ID -> storage identity
~~~

This reduces path manipulation and overwrite collisions.

## 3. Extension vs actual content

A file ending in .txt is not guaranteed to contain text.

The training app therefore checks three things:

- extension is .txt,
- size is within the lab limit,
- bytes decode as UTF-8.

This is intentionally simple. Real formats may need format-aware parsers.

## 4. Content-Type is not proof

A client can claim text/plain even when the bytes are something else.

Treat Content-Type as useful metadata, not a complete security decision.

## 5. File signatures and parser validation

Some formats have magic bytes or structural signatures.

A header match can help identify a format, but it does not prove that the entire file is valid or safe.

For complex file types, validation may require a real parser.

That parser itself becomes part of the attack surface and should be updated, bounded, and isolated when appropriate.

## 6. Size limits

Uploads consume bandwidth, memory, disk, parser time, and scanner time.

The local app limits files to 256 KiB.

It reads at most limit + 1 byte so it can detect an oversized upload without blindly reading arbitrary amounts into memory.

## 7. Isolated storage

Uploads should normally be stored separately from:

- application source,
- templates,
- executable scripts,
- configuration,
- other sensitive files.

A safer mental model is:

~~~text
application code/
upload data/
logs/
database/
~~~

with clear permissions between them.

## 8. Do not execute uploaded content

Uploaded content should usually remain data.

Risky design:

~~~text
upload -> executable directory -> runtime interprets as code
~~~

Safer design:

~~~text
upload -> validate -> store as inert data -> controlled retrieval
~~~

## 9. Object IDs instead of paths

Rather than letting the client request a storage path, the demo returns a server-generated object ID.

Retrieval becomes:

~~~text
/files/<object-id>
~~~

The server then maps:

~~~text
object ID -> metadata -> trusted stored filename
~~~

This connects directly to Day 8 path traversal defenses.

## 10. Path safety is separate from authorization

Even a perfectly safe storage path can expose another user's data if authorization is missing.

Always ask two separate questions:

1. Can this request escape the intended storage location?
2. Is this requester allowed to access this object?

Path safety and authorization solve different problems.

## 11. Hashing

The demo computes SHA-256 for every accepted upload.

Hashes can help with:

- artifact identity,
- duplicate comparison,
- audit trails,
- scanner correlation,
- integrity checks.

A hash does not prove that a file is safe.

## 12. Quarantine and scanning

A real product may use:

~~~text
upload
  ↓
quarantine
  ↓
validation
  ↓
scanner / parser
  ↓
policy decision
  ↓
publish
~~~

Do not expose content before required checks are complete.

A clean scanner result is not a guarantee of safety; detectors can miss things.

## 13. Archive risks

Archives add extra resource and path concerns:

- expanded size,
- file count,
- nesting depth,
- internal filenames,
- decompression bombs.

This training lab intentionally does not accept archives.

## 14. Image upload risks

Images may be passed through decoders, metadata parsers, or resizing libraries.

A safer production design may include:

- size and dimension limits,
- re-encoding,
- metadata policy,
- current libraries,
- process isolation.

## 15. Local lab

Run:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python safe_upload_demo.py
~~~

The service binds only to 127.0.0.1:5000.

Create a harmless file:

~~~bash
printf "hello upload lab\n" > demo.txt
~~~

Upload it:

~~~bash
curl -F "file=@demo.txt" http://127.0.0.1:5000/upload
~~~

Observe the returned object ID, original filename, size, and SHA-256.

## 16. Retrieve by object ID

Use the returned ID:

~~~bash
curl -OJ http://127.0.0.1:5000/files/<ID>
~~~

The client never chooses the internal storage path.

## 17. Safe negative tests

On your own local app, try:

- empty file,
- wrong extension,
- oversized file,
- invalid UTF-8 bytes.

The goal is not bypassing the control. The goal is verifying that invalid input fails predictably.

## 18. Logging

Useful fields include:

- object ID,
- authenticated user,
- original filename,
- size,
- SHA-256,
- validation result,
- scan/quarantine status,
- timestamp.

Avoid logging complete file contents without a clear reason.

## 19. Mini challenge — ownership

Add an owner field to the in-memory metadata and require a training identity before retrieval.

Explain why this is authorization, not upload validation.

## 20. Mini challenge — quarantine states

Add:

~~~text
pending
approved
rejected
~~~

Only approved files should be downloadable.

Do not build a malware scanner; simulate the workflow.

## 21. Mini challenge — image pipeline

Design a PNG/JPEG upload pipeline and describe controls at:

1. request layer,
2. size/type validation,
3. image parser,
4. storage,
5. authorization,
6. serving.

Do not rely on extension alone.

## 22. Code review checklist

~~~text
1. Is the client filename trusted as a path?
2. Is upload size bounded?
3. Is actual content validated?
4. Is storage isolated?
5. Can uploaded data become executable?
6. Are server-generated IDs used?
7. Is retrieval authorized?
8. Are archives bounded?
9. Are parsers isolated/updated?
10. Are hashes recorded?
11. Is quarantine/scanning needed?
12. Are internal paths hidden?
~~~

## Exercises

1. Run the local app.
2. Upload a valid text file.
3. Verify its SHA-256 independently.
4. Retrieve it by object ID.
5. Test an empty file.
6. Test a wrong extension.
7. Test an oversized training file.
8. Explain original filename vs stored name.
9. Explain extension vs content.
10. Explain path safety vs authorization.
11. Design the quarantine challenge.
12. Design an image-upload pipeline.

## Questions

1. Why is an uploaded file untrusted?
2. Why should the original filename not be the storage path?
3. Why are extensions insufficient?
4. Why is Content-Type insufficient?
5. Why do size limits matter?
6. Why isolate upload storage?
7. Why serve by object ID?
8. Why is hashing useful?
9. Why does a clean AV result not guarantee safety?
10. What extra risks do archives add?
11. Why can image parsers become attack surface?
12. Why is validation separate from authorization?

## Main takeaway

~~~text
untrusted file
    ↓
limit + validate
    ↓
server-generated identity
    ↓
isolated storage
    ↓
optional quarantine / scan
    ↓
authorization
    ↓
controlled serving
~~~

File upload security is a pipeline, not a single filename check.
