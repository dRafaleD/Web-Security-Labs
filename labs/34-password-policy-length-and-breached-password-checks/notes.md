# Day 34 — Password Policy: Length and Breached-Password Checks

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Password Policy: Length and Breached-Password Checks** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Prefer a minimum length (for example 12 characters) over complex composition rules.
2. Reject passwords that appear in a list of known breached or very common passwords.
3. Compare in a normalized form so trivial variations of a bad password are also caught.

## Important distinctions
- A long passphrase can still be reused or breached; the list check covers that.
- The policy complements rate limiting and MFA; it does not replace them.
- Never log the password you are checking.

## Hands-on lab
Read `policy_demo.py` before running the following from this lab folder:

~~~bash
python3 policy_demo.py
~~~


## Assignments
1. Predict which of the five passwords are accepted.
2. Run the demo and record each reason.
3. Add a trivial variation of a listed password and see whether it is caught.
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
