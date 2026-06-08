# Corrections to Code Review Findings

During Issue #19 implementation, the following reviewer findings were determined to be **not bugs**:

## B2/B6 — `except ValueError` in `_triple_search.py`
**Reviewer claim:** Catching `ValueError` instead of `AmbiguousUUIDError` — the catch is overly broad.

**Reality:** This is intentional design. `resolve_subjects()` and `resolve_objects()` in `_triple_search.py` catch `ValueError` from `resolve_uuid_prefix()` as a fallback to label search. The comment explicitly says "Ambiguous or not found — fall through to label search". This provides better UX: if a UUID prefix is ambiguous, the search tries label-based matching as a second attempt rather than immediately erroring.

## `_preview.py:resolve_node_label()` exception ordering
**Reviewer claim:** `except AmbiguousUUIDError` followed by `except ValueError` — claims AmbiguousUUIDError is silently caught.

**Reality:** Python's exception handling matches the first `except` clause in order. `AmbiguousUUIDError` (a `ValueError` subclass) is caught by the first `except` and **re-raised** via `raise`, never reaching the second `except ValueError`. The ordering is correct.

## Test Count
**Reviewer estimate:** ~128 total tests.

**Reality:** The test suite had already grown to **223** tests before Issue #19 (now 227). Some coverage gaps flagged by the reviewer (e.g., `confirm_node_with_arcs`, `get_subject_objects`) may have been addressed by Issue #12's 40 new edge case tests.
