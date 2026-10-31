# Day 29 — Secure Random Tokens: Length and Entropy

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Secure Random Tokens: Length and Entropy** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Session IDs and reset tokens must come from a cryptographically secure random source.
2. 128 bits of randomness is a common minimum for tokens that guard accounts.
3. Predictable values such as timestamps, counters or a seeded general-purpose generator are not secure.

## Important distinctions
- Length alone does not make a token secure; the source of randomness does.
- A token that looks random can still be fully determined by a known seed.
- Store only hashes of long-lived tokens on the server.

## Hands-on lab
Read `token_demo.py` before running the following from this lab folder:

~~~bash
python3 token_demo.py
~~~


## Assignments
1. Predict which generator produces repeatable tokens.
2. Run the demo and compare the two outputs.
3. Compute how many bits a 16-character hex token has.
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
