# Day 14 — CORS Origin Validation, Preflight and Credential Boundaries

[English](notes.md) · [Türkçe](notes.tr.md)

## Goal
Understand cors origin validation, preflight and credential boundaries through a fully local, harmless experiment. Keep observation separate from inference.

## Core concepts
1. **same-origin policy versus CORS** — document the boundary, expected behavior and limitations.
2. **Origin and Access-Control-Allow-Origin** — document the boundary, expected behavior and limitations.
3. **preflight OPTIONS request** — document the boundary, expected behavior and limitations.
4. **credentials and allowlisted origins** — document the boundary, expected behavior and limitations.
5. **Vary: Origin** — document the boundary, expected behavior and limitations.
6. **CORS is not server-side authorization** — document the boundary, expected behavior and limitations.

## Procedure
The included `cors_demo.py` is a synthetic training example. From the lab directory:

```bash
python3 cors_demo.py
```

```bash
curl -i -H 'Origin: http://localhost:3000' http://127.0.0.1:8081/
```

```bash
curl -i -H 'Origin: https://untrusted.example' http://127.0.0.1:8081/
```

```bash
curl -i -X OPTIONS -H 'Origin: http://localhost:3000' -H 'Access-Control-Request-Method: GET' http://127.0.0.1:8081/
```

**Expected:** Allowlisted Origin receives CORS response headers; unrelated origins do not.

## Observations to record
Write down the machine/tool versions, exact command, input, actual output, unexpected behavior, and interpretation. Explain which results are facts and which remain hypotheses.

## Exercises
1. Run the baseline and save the observed output.
2. Change one harmless input and predict what happens before running.
3. Add a negative test and distinguish a rejection from a failure to observe.
4. Restore the original, rerun it, and explain why regression tests matter.
5. Identify two realistic false-positive explanations.
6. Identify a useful independent corroborating observation.
7. Draft a short report stating limitations explicitly.

## Review questions
1. What does same-origin policy versus CORS mean, why does it matter, and what does it not guarantee?
2. What does Origin and Access-Control-Allow-Origin mean, why does it matter, and what does it not guarantee?
3. What does preflight OPTIONS request mean, why does it matter, and what does it not guarantee?
4. What does credentials and allowlisted origins mean, why does it matter, and what does it not guarantee?
5. What does Vary: Origin mean, why does it matter, and what does it not guarantee?
6. What does CORS is not server-side authorization mean, why does it matter, and what does it not guarantee?
7. What would improve the confidence of your result?
8. Which regression test should be automated first?

## Ethics and scope
Use only locally generated data and infrastructure you own or are authorized to study. Findings from an individual signal are not proof of an incident.
