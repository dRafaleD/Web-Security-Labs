# Day 26 — Session Idle and Absolute Timeouts

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Session Idle and Absolute Timeouts** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. An idle timeout ends a session after a period without activity; an absolute timeout ends it after a fixed lifetime regardless of activity.
2. Check both on the server for every request; a cookie expiry alone is not enforcement.
3. Rotate the session ID on privilege changes and expire the server-side record on logout.

## Important distinctions
- Idle timeouts limit stolen-session exposure on unattended devices; absolute timeouts limit exposure of a continuously used stolen session.
- Timeouts are a trade-off between security and user friction; choose by data sensitivity.
- The client clock is untrusted; use server time.

## Hands-on lab
Read `timeout_demo.py` before running the following from this lab folder:

~~~bash
python3 timeout_demo.py
~~~


## Assignments
1. Predict the result of each request before running the demo.
2. Run it and record which requests are rejected and why.
3. Change the idle timeout to 60 seconds and describe the effect.
4. Add an assertion that activity cannot extend a session past the absolute limit.
5. Describe how an attacker with a stolen session ID benefits from each timeout type.
6. Propose an independent control, such as binding sessions to device signals or re-authentication for sensitive actions.

## Knowledge check
1. Where does the input originate, and who controls it?
2. What was directly observed, as opposed to inferred?
3. What assumptions might fail in production?
4. Which evidence would be insufficient on its own?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
