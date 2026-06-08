# Issue #42: Code Review Round 18 — Transaction, Exception Narrowing, Duplication Extraction, Modifi Split, Coverage

**PR:** #42 (merged to main)
**Branch:** fix/review-round18-fixes
**Date:** May 25, 2026
**Tests:** 399 pass (390 → 399)

## Problems Fixed

### Medium
1. **Missing transaction in `PredicateService.update()`** — FTS re-index not wrapped in transaction. If `_remove_from_fts()` succeeded but `_index_fts()` failed mid-flight, the only recovery was a full FTS rebuild. Fixed by wrapping in `with self.db.transaction()`.

2. **Broad `except Exception` in `eksporti()`** — `_cli_query.py:230` caught all exceptions. Narrowed to `except (sqlite3.Error, ValueError)` — only DB errors and JSON decode errors are expected from `export_turtle()`.

### Code Quality
3. **Duplicated UUID resolution** — `_resolve_node_by_label()` helper extracts the common UUID-prefix-then-FTS5 pattern shared by `resolve_subjects()` and `resolve_objects()`. Returns `(node_ids, ambiguous)` tuple so `resolve_objects()` can skip literal fallback when prefix is ambiguous.

4. **Monolith `modifi()` split** — Extracted `_resolve_subject_id()` (replaces 3×12-line duplicated blocks) and `_resolve_new_object_value()` helpers. `modifi()` body reduced from ~362 to ~160 lines.

5. **PEP 8 blank lines** — Trimmed extra blank lines in `_predicate_service.py`.

### Coverage
6. Added 9 new tests for previously untested functions: `get_subject_objects()`, `build_modify_preview()`, `resolve_deprecated()`, `empty_all_trash()`.

## Key Files Changed
- `_predicate_service.py` — Transaction + PEP 8 blank lines
- `_cli_query.py` — Exception narrowing + sqlite3 import
- `_triple_search.py` — `_resolve_node_by_label()` extraction
- `_cli_modify.py` — `_resolve_subject_id()`, `_resolve_new_object_value()` helpers
- 4 test files — 9 new coverage tests
