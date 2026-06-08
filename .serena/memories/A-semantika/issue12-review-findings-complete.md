# Issue #12 — Code Review Findings — Complete

## Summary
Comprehensive code review of A-semantika identified 5 medium-severity bugs, 4 low-severity issues, 4 suggestions, and test coverage gaps. All addressed in commit `510adac` on branch `fix/issue-12-review-findings`, merged to `main`.

## Bugs Fixed

### M1 — FTS5 Query Injection Risk
**File:** `_node_service.py:271` → `search()` method
**Fix:** Strip FTS5 special chars (`" * ^ - + ~ ( ) { } [ ] : < > %`) from tokenized words before building MATCH string. Also skip FTS5 reserved keywords (AND, OR, NOT, NEAR, COLUMN). Falls back to LIKE search when all tokens are stripped.

### M2 — Overbroad `except ValueError: pass`
**File:** `_cli_nodo.py:199-200`
**Fix:** Narrowed to only suppress "already exists" errors by checking `"already exists" in str(e)`. Other errors (FK violations, etc.) are re-raised.

### M3 — UUID Heuristic Misclassifies Short Labels
**File:** `_triple_search.py:30` → `_looks_like_uuid_prefix()`
**Fix:** Changed regex from `^[a-zA-Z0-9\-]+$` to `^[0-9a-fA-F\-]+$` (hex-only), and require 8-12 chars. Short labels like "tipo" (4 chars) or "Hundo" (5 chars) no longer trigger pointless DB lookups.

### M4 — Potential None Dereference on `new_object`
**File:** `_cli_modify.py:254`
**Fix:** Added `if new_obj is None: new_obj = object or ""` guard before `resolve_node_label(node_svc, new_object)`.

### M5 — `object_unit` Column Undocumented
**File:** `data/storage.py:71`
**Status:** Column already exists in schema. Verified.

## Low Severity Fixes
- L1: Fixed 7-space indent → 4-space in `AmbiguousUUIDError` class
- L2: Moved `import uuid` to module level in `_node_service.py`, `_predicate_service.py`, `_predicate_group_service.py`
- L3: Moved all `from A import error/info` to module level in `_preview.py`
- L4: Handle custom datatypes (non-xsd) in Turtle export — emit full URI for custom types

## Suggestions
- S1: `LIKE ... COLLATE NOCASE` for FTS5 fallback in `_node_service.py`
- S2: Predicate validation moved BEFORE confirmation preview in `_cli_triples.py`
- S3: Consistent `self.db.execute()` pattern in `remove_member` (now uses transaction with rowcount)
- S4: Added `clear_members()` method to `PredicateGroupService`

## Test Coverage
- Created `tests/test_edge_cases.py` with 40 tests
- Added `clear_members` test to `test_predicate_groups.py`
- Updated `test_triple_search.py` for new UUID heuristic
- **Total: 195 tests, all passing**

## Key Files Changed
- `_node_service.py` — FTS5 sanitization, import uuid at module, indent fix, COLLATE NOCASE
- `_cli_nodo.py` — Narrowed except ValueError
- `_triple_search.py` — UUID heuristic tightened
- `_cli_modify.py` — None guard
- `_triple_service.py` — Custom datatype Turtle export
- `_cli_triples.py` — Predicate validation before confirm
- `_predicate_group_service.py` — clear_members(), consistent db patterns
- `_cli_predikat_grupo.py` — Use clear_members() instead of raw SQL
- `_preview.py` — Module-level imports
- `_predicate_service.py` — Module-level import uuid
- `tests/test_edge_cases.py` — 40 new edge case tests
- `tests/test_triple_search.py` — Updated for new UUID heuristic
- `tests/test_predicate_groups.py` — Added clear_members test
