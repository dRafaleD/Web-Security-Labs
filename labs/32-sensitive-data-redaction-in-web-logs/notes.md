# Day 32 — Sensitive Data Redaction in Web Logs

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Sensitive Data Redaction in Web Logs** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Query strings, headers and bodies often hold tokens and passwords; do not log them verbatim.
2. Redact by field name for known sensitive keys, and by pattern for token-looking values.
3. Prefer an allow-list of fields to log over a deny-list of fields to hide.

## Important distinctions
- Redaction after the fact is a safety net; avoid collecting the data in the first place.
- URL paths can also carry secrets such as reset tokens.
- Test redaction with synthetic secrets.

## Hands-on lab
Read `log_redact_demo.py` before running the following from this lab folder:

~~~bash
python3 log_redact_demo.py
~~~


## Assignments
1. Predict the redacted log line.
2. Run the demo and confirm no secret remains.
3. Add a header the redactor does not know and see what happens.
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
