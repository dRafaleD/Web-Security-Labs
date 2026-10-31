# Day 30 — Error Handling and Information Disclosure

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Error Handling and Information Disclosure** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Show users a generic message and a correlation ID; keep stack traces, SQL and paths in server logs.
2. Distinct error messages for existing and missing accounts leak which accounts exist.
3. Turn debug mode off in production and test the error paths.

## Important distinctions
- The correlation ID connects the user's report to the log without exposing internals.
- Consistent timing also matters for enumeration, not only messages.
- Never reflect raw exception text to the client.

## Hands-on lab
Read `errors_demo.py` before running the following from this lab folder:

~~~bash
python3 errors_demo.py
~~~


## Assignments
1. Predict what the user sees for each error.
2. Run the demo and compare the response with the server log.
3. Add a new error type and confirm it is also generic.
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
