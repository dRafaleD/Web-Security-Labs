# Day 27 — Request Smuggling: Header Ambiguity Checks

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Request Smuggling: Header Ambiguity Checks** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. When a request has both `Content-Length` and `Transfer-Encoding`, two servers can disagree about where it ends.
2. Reject ambiguous requests at the edge instead of trying to guess which header wins.
3. Duplicate or malformed length headers are rejected the same way.

## Important distinctions
- This lab is a defensive validator; keep front end and back end parsers consistent.
- Upgrading to HTTP/2 end to end removes many of these ambiguities.
- Test with synthetic header lists, not live traffic.

## Hands-on lab
Read `ambiguity_demo.py` before running the following from this lab folder:

~~~bash
python3 ambiguity_demo.py
~~~


## Assignments
1. Predict which header sets are rejected.
2. Run the demo and record the rejection reasons.
3. Add a request with a negative Content-Length.
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
