# Issue #19 — Remaining Code Review Findings — Complete

## Summary
Addressed 5 remaining findings from the Issue #12 code review that were not covered by the first fix round. Branch `fix/issue-13-review-remaining-findings`, PR #20, merged to `main`.

## Fixes

### V1 — Bare `except: pass` in NodeService.delete()
**File:** `_node_service.py:226-227`
Replaced bare `except: pass` with `_warning()` log call. Violated AGENTS.md Rule 11.

### B1 — Dead code in aldoni() after Cancelled
**File:** `_cli_triples.py:177-180`
Removed 3 unreachable lines (copy-paste artifact) after `raise typer.Exit(0)` following `confirm_triple()` returning False. The lines duplicated the predicate-not-found error that appears earlier in the function.

### B4 — FTS re-index not wrapped in transaction
**File:** `_node_service.py:174-178`
`_remove_from_fts()` + `_index_fts()` in `NodeService.update()` now wrapped in `with self.db.transaction()` to prevent partial FTS corruption if re-index fails after removal.

### S1 — Missing UNIQUE constraint on predicate_group_members
**File:** `data/storage.py`
- Added `UNIQUE(group_uuid, predicate_id)` to `predicate_group_members` DDL
- Created `_migrate_predicate_group_members_unique()` for existing databases
- Migration deduplicates existing rows (first-wins via INSERT OR IGNORE)
- Uses PRAGMA foreign_keys=OFF/ON swap pattern (consistent with predicates migration)

### S3 — AGENTS.md schema outdated
**File:** `AGENTS.md`
- Updated `predicates` schema: removed `uuid TEXT PRIMARY KEY`, now `predicate_id TEXT PRIMARY KEY`
- Added `UNIQUE(group_uuid, predicate_id)` to `predicate_group_members` in docs
- Added changelog entry for this issue

## Files Changed
| File | Change |
|------|--------|
| `_node_service.py` | V1: warning() instead of pass; B4: transaction wrapping FTS re-index |
| `_cli_triples.py` | B1: removed 3 lines dead code |
| `data/storage.py` | S1: UNIQUE constraint + migration function; init_db() call |
| `AGENTS.md` | S3: updated predicates schema; added changelog entry |
| `tests/test_storage.py` | 4 new tests for migration + SQL-level constraint |

## Tests
- **4 new tests** in `test_storage.py::TestPredicateGroupMembersUniqueMigration`:
  - `test_migration_adds_unique_constraint` — old schema → migration → duplicate blocked
  - `test_migration_deduplicates_existing_rows` — 2 duplicates → 1 row after migration
  - `test_migration_idempotent` — running twice is safe
  - `test_new_schema_has_unique_constraint` — fresh DB has UNIQUE from start
- **227 total tests**, all passing
- **User-simulation** confirmed triple creation, FTS search after update, and UNIQUE constraint all work
