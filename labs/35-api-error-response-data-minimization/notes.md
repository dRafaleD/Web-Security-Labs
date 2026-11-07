# Day 35 — Safe API Error Responses and Data Minimization

[English](notes.md) · [Türkçe](notes.tr.md) · [Practical](error_demo.py)

## Learning objective

This exercise uses only harmless, authorized local samples to study **Safe API Error Responses and Data Minimization**. Distinguish direct observations from unsupported conclusions.

## Core concepts

1. Public API responses need stable generic error codes rather than stack traces, credentials or internal paths.

2. Detailed diagnostics belong in protected server logs, subject to retention and redaction policies.

3. Correct status codes and request correlation IDs help troubleshooting without leaking sensitive information.

## Hands-on

Read the source and predict the output before running:

```bash
python error_demo.py
```

Try inserting a fabricated exception message; verify the response never reflects it.

## Assignments

1. Compare expected and observed results.
2. Document one positive and one negative case.
3. Explain why a single indicator cannot establish intent or safety.
4. Change a harmless boundary input and repeat the test.

## Knowledge check

- Which trust boundary is relevant?
- Which evidence may be missing or misleading?
- What independent validation would production require?

## Safety and limitations

No live malware, unauthorized systems or offensive targets. This toy exercise is not a production detector or safety guarantee.
