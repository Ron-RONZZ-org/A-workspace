# Issue #31: Code Review Round 8 — B3/B2/Q1 Fixes

## Summary
Three findings from the eighth code review of A-semantika, fixed on branch `fix/review-round8-code-quality`.

## Fixes

### B3 (Medium): `_cli_rubujo.py` — Missing COLLATE NOCASE
- **Problem:** `_resolve_trash_node()` used LIKE for prefix matching without `COLLATE NOCASE`, so uppercase human-readable IDs (e.g. `SPACO`) couldn't be found via lowercase prefix (`spaco`).
- **Fix:** Added `COLLATE NOCASE` to both the exact match and LIKE prefix queries.

### B2 (Low): `_triple_search.py` — Spurious literal warning
- **Problem:** `warning()` fired for EVERY object falling through to literal mode. Users searching literal values got confusing "No node found — searching as literal value" warnings.
- **Fix:** Suppress warning when text is obvious literal (numeric, multi-word, quoted). Only warn for single non-numeric words that could be mistyped node labels.

### Q1 (Low): `_preview.py` — Duplicated label logic
- **Problem:** `resolve_predicate_label()` duplicated the eo→en→first fallback logic from `storage.label_from_json()`.
- **Fix:** Delegated to `label_from_json()`, removed ~15 lines duplicated code.

## Tests
10 new tests (295 total). All passing.

## Timeline
- Branch: `fix/review-round8-code-quality`
- Merged: commit 3607f4c to main
- Issue: https://github.com/Ron-RONZZ-org/A-semantika/issues/31
