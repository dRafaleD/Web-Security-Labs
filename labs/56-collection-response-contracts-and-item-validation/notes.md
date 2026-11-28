# Day 56 — Collection Response Contracts and Item Validation

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](collection_contract.py)

Day 55 checked nested response projections. Today validate a fictional page containing up to three items, with count defined as the number in this page. Every item must have exactly id and title, both nonempty strings. Reject duplicate IDs, extra fields, malformed items and mismatched counts. Predict eleven cases and add a page with three distinct valid records. Explain why count here is not the total database count and why schema validation does not establish per-object authorization. No HTTP server or external targets.

## Run
```bash
python3 labs/56-collection-response-contracts-and-item-validation/collection_contract.py
```
