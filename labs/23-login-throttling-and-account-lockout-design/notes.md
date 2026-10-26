# Day 23 — Login Throttling and Account Lockout Design

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Login Throttling and Account Lockout Design** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Count failed logins per account and per source IP inside a sliding window.
2. Return one uniform message so responses do not reveal which usernames exist.
3. Hard per-account lockout can be abused to lock victims out, so use a temporary window and pair it with IP limits and MFA.

## Important distinctions
- Throttling slows guessing; it does not replace strong passwords or MFA.
- A per-IP limit alone fails against distributed attempts; a per-account limit alone enables lockout abuse.
- Locked accounts must reject even the correct password during the lock window.

## Hands-on lab
Read `throttle_demo.py` before running the following from this lab folder:

~~~bash
python3 throttle_demo.py
~~~


## Assignments
1. Predict the three printed messages before running the demo.
2. Run it and note when the correct password starts working again.
3. Change `window` to 60 seconds and explain the effect on both an attacker and a legitimate user.
4. Add an assertion that failures for `alice` do not block `bob` from the same IP below the IP limit.
5. Describe a distributed attack that stays under both limits.
6. Propose a corroborating control such as MFA, breached-password checks, or alerting on lockout spikes.

## Knowledge check
1. Where does the input originate, and who controls it?
2. What was directly observed, as opposed to inferred?
3. What assumptions might fail in production?
4. Which evidence would be insufficient on its own?
5. What should an automated test check?

## Safety and limitations
Use only authorized systems and synthetic data. The example is not a complete security or detection product.
