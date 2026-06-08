# Review Round 20 — Completed 2026-05-26

## Summary
Code review round 20 covering: Rubujo CLI refactoring, FTS transaction fixes, preview cleanup, +25 regression tests.

## Issues
- **Issue #45** (closed): All fixes + tests merged via PR #46 and PR #48

## Key Fixes

### 1. Rubujo CLI Refactoring
Extracted shared trash CLI helpers into `_rubujo_helpers.py` — parameterized by service type (supports both `nodes_rubujo` and `predicates_rubujo` tables). Both CLIs now use the same `resolve_trash_item()`, `batch_restore()`, `batch_permanent_delete()`, `build_trash_table()` helpers.

Files reduced: `_cli_rubujo.py` 490→290 lines, `_cli_predikato_rubujo.py` 401→229 lines.

### 2. FTS Transaction Fixes
- **create()**: INSERT + FTS index wrapped in a single transaction
- **_move_to_trash()**: FTS removal inside transaction; **reordered** FTS removal BEFORE DELETE from nodes table (FTS5 'delete' command needs the rowid from the content table)

### 3. Preview No typer.Exit
`build_triple_preview_table()` returns `(None, "")` instead of raising `typer.Exit(1)` on ambiguous prefixes. Also fixed: unit label resolution for typed literals was called outside the `try/except AmbiguousUUIDError` block.

### 4. Rollback Hard-Delete
`create_node_arcs()` rollback uses `soft=False` to prevent misleading trash entries for nodes never successfully created.

## Bug Fixes Discovered During Testing
1. **FTS "missing row" error**: `_remove_from_fts()` was called after `DELETE FROM nodes`, couldn't find rowid, leaving dangling FTS references that crashed subsequent MATCH queries.
2. **Unit label resolution**: `resolve_node_label()` for typed-literal units was outside the `try/except AmbiguousUUIDError` guard.

## Tests
- 426 total (401 existing + 25 new)
- Tests cover: hard-delete rollback (3), FTS in create (2), FTS in trash (2), preview returns None (5), resolve_trash_item (10), smoke (2)

## Files Modified
| File | Change |
|------|--------|
| `src/A_semantika/_rubujo_helpers.py` | NEW - shared trash CLI helpers |
| `tests/test_review_round20.py` | NEW - 25 regression tests |
| `src/A_semantika/_cli_rubujo.py` | Simplified to use shared helpers |
| `src/A_semantika/_cli_predikato_rubujo.py` | Simplified to use shared helpers |
| `src/A_semantika/_node_service.py` | FTS in transaction, FTS reorder in _move_to_trash |
| `src/A_semantika/_preview.py` | No typer.Exit in helper, unit fix |
| `src/A_semantika/_cli_helpers.py` | Rollback hard-delete |
| `pyproject.toml` | pytest marker config |
| `AGENTS.md` | Review round 20 entry |
