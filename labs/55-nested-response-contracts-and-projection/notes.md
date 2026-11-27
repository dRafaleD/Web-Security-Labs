# Day 55 — Nested Response Contracts and Projection

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](nested_dto.py)

Day 54 checked top-level response contracts. Today build a new nested object from explicit allowed fields rather than copying the full profile. An allowed parent key does not automatically authorize all child keys. Eight response cases and three projection checks cover nested extra fields, missing fields and wrong types. Add a fictional domain-only nested property and confirm it is absent from the result. Extend the contract with an approved display field and update both positive and negative tests. This is an offline DTO exercise assuming prior authorization; field names do not guarantee that allowed text contains no sensitive content.

## Run
```bash
python3 labs/55-nested-response-contracts-and-projection/nested_dto.py
```
