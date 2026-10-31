# Day 28 — Content-Type Validation and MIME Sniffing

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Content-Type Validation and MIME Sniffing** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Do not trust the `Content-Type` header or the extension of uploaded files; check the leading bytes too.
2. Serve user content with an explicit type and `X-Content-Type-Options: nosniff` so browsers do not guess.
3. Compare the declared type with the detected one and reject mismatches.

## Important distinctions
- Magic bytes are a quick check, not a full validation of the file.
- Active content like HTML or SVG in an upload needs separate handling.
- Serve uploads from a separate origin when possible.

## Hands-on lab
Read `mime_demo.py` before running the following from this lab folder:

~~~bash
python3 mime_demo.py
~~~


## Assignments
1. Predict which uploads are rejected.
2. Run the demo and record the reasons.
3. Add an HTML file declared as an image and check the result.
4. Add an assertion for one security property.
5. Describe a negative case and a potential false positive.
6. Propose an independent corroboration method.

## Knowledge check
1. Where does the input originate, and who controls it?
2. What was directly observed, as opposed to inferred?
3. What assumptions might fail in production?
4. Which evidence would be insufficient on its own?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
