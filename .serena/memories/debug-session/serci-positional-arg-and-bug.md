# Debug Session: `serci` Positional Argument Bug

## Date
2026-05-28

## Bug
`serci H_HFORD` (positional argument, no flags) returned "Neniuj arkoj trovitaj" while `serci -s H_HFORD` worked correctly.

## Root Cause

In `A-semantika/src/A_semantika/_cli_query.py` lines 109-112 (before fix):

```python
if search_term and not (subject or predicate or object):
    subject = search_term
    predicate = search_term
    object = search_term
```

The positional `search_term` was set as ALL THREE fields (subject, predicate, object). Since `search_triples_by_labels` ANDs across fields, and `resolve_predicates("H_HFORD")` returned an empty list (no predicate matches the node ID/label), the combined AND query returned zero results. TripleService.search_triples() has an early return when any list is empty:

```python
if predicate_ids is not None:
    if not predicate_ids:
        return []
```

## Fix (v2 — user corrected: OR was the intent)

Added `search_triples_any_field()` to `_triple_search.py` which:
1. Resolves the search term independently for each field
2. Does 1-3 separate `search_triples()` calls (one per non-empty field)
3. Merges results with deduplication by compound key

This gives true OR semantics across subject/predicate/object.

The `serci` function in `_cli_query.py` now calls `search_triples_any_field()` when a positional argument is given without explicit flags.

```python
if search_term and not (subject or predicate or object):
    subject = search_term
```

Also updated the docstring and help text to clarify the behavior.

## Files Changed
- `A-semantika/src/A_semantika/_cli_query.py` — fix + docstring update
- `A-semantika/tests/test_cli_triples.py` — added `test_triple_serci_positional_arg` test

## Scope
The bug pattern (setting all three fields from one positional arg) only existed in `_cli_query.py`. No other files were affected.
