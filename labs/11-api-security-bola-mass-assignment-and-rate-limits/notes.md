# Day 11 — API Security: BOLA, Mass Assignment and Rate-Limit Design

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

This hands-on day builds on earlier labs, using only local harmless training data. Verify assumptions, distinguish observation from inference, and do not treat tool output as automatic security proof.

## Learning objectives

- Object-level authorization
- BOLA test design
- Mass assignment
- Authentication vs authorization
- Rate-limit models
- Response safety
- Negative testing
- Operational controls

## Data flow and threat model

```text
controlled training input
        ↓
parser / evaluator / analyst
        ↓
security or evidence check
        ↓
observable result
        ↓
review assumptions and limits
```

## 1. Object-level authorization

Enforce ownership on every read/update; object IDs alone never imply access rights.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## 2. BOLA test design

Compare own record vs another user's record and require a non-disclosing rejection.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## 3. Mass assignment

Only explicitly allowed JSON fields may modify resources; prevent changes to owner or role.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## 4. Authentication vs authorization

Use verified identity on server; never trust a user ID sent as a privileged claim.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## 5. Rate-limit models

Design per-identity request budgets, time windows and distributed counters; a demo is not production middleware.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## 6. Response safety

Return controlled 400/404 errors and avoid leaking record contents or internal stack traces.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## 7. Negative testing

Test cross-owner read, unauthorized update, unexpected fields and wrong types.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## 8. Operational controls

Review audit logs, scope, revocation, pagination and abuse detection as additional layers.

**Task:** Explain which trust-boundary mistake this control prevents, with a concrete example.

## Local exercise

Use only the files in this repository. This example is not a production security service.

```bash
python3 api_demo.py
```

## Test matrix

| Scenario | Expected | Reason |
|---|---|---|
| Valid training input | Accept / match | Baseline |
| Wrong owner or header | Reject / no match | Scope / structure |
| Truncated or missing field | Controlled failure | Input validation |
| Unrelated benign sample | No accidental claim | False-positive awareness |

## Exercises

1. Run and record the example.
2. Write an initial hypothesis.
3. Verify the positive case.
4. Add one negative case.
5. Add another negative case.
6. Test a boundary value.
7. Find the responsible source-level check.
8. Separate observations from inferences.
9. Change one control in a working copy.
10. Rerun the whole test matrix.
11. Document limitations.
12. Write a one-page analysis report.

## Review questions

1. What is the primary trust boundary?
2. Which inputs are untrusted?
3. What does the positive test establish?
4. What does the negative test establish?
5. What does the observed output support?
6. What does it not support?
7. Which input is the most important?
8. Give an example boundary value.
9. What is fail-closed behavior?
10. Why is the demo not production-ready?
11. Describe one potential false positive.
12. Describe one potential false negative.
13. Which fields belong in an audit log?
14. What personal data is unnecessary?
15. Why record tool versions?
16. Which regressions need retesting?

## Mini challenges

1. Add a new negative test and document its expected and actual results.
2. Break one assumption in a working copy and identify which test catches it.
3. Write a short report containing source, hash, tool version, command, observation and limitations.

## Takeaway

Measure actual behavior rather than overgeneralizing from synthetic cases. Security decisions, authorization and forensic inferences require independent checks.
