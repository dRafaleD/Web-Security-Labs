# Day 31 — Dependency Pinning and Advisory Checks

[English](notes.md) · [Türkçe](notes.tr.md)

## Learning objective
This day explores **Dependency Pinning and Advisory Checks** with harmless local fixtures. The goal is to reason about controls, evidence, and limits rather than treating one output as proof.

## Core concepts
1. Pin exact dependency versions and use a lock file so builds are reproducible.
2. Check pinned versions against an advisory list on every build, not just once.
3. Version ranges such as `>=1.0` hide what is actually installed.

## Important distinctions
- An advisory means a vulnerable version exists, not that your code reaches the vulnerable function.
- Transitive dependencies matter as much as direct ones.
- Updating blindly can break behavior; run tests after each bump.

## Hands-on lab
Read `deps_demo.py` before running the following from this lab folder:

~~~bash
python3 deps_demo.py
~~~


## Assignments
1. Predict which pinned packages match an advisory.
2. Run the demo and record the fix versions.
3. Add an unpinned requirement and watch the check refuse it.
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
