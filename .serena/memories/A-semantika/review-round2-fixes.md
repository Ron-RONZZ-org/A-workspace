# A-semantika Review Round 2 - Completed Fixes (May 2026)

## Summary
Fixed 14 issues from a comprehensive code review of A-semantika. All 243 tests pass (was 227).

## Critical Fixes
1. **[C1/Critical]** `_cli_modify.py` — None dereference in modifi preview: `resolve_node_label(node_svc, new_object)` → `resolve_node_label(node_svc, new_obj)`. The variable `new_object` is the raw None-able Typer parameter, `new_obj` is the resolved value.

2. **[C2/New Feature]** Added `rubujo` subcommand group for trash management:
   - `_cli_rubujo.py` with commands: `ls`, `restaŭrigi`/`restauxrigi`, `malplenigi`, `forigi`
   - `_resolve_trash_node()` helper queries `nodes_rubujo` directly (not `nodes` table)
   - Registered in `cli.py`

3. **[C3/Bug]** `NodeService.restore()` — did not re-index FTS after restore, causing "database malformed" error on subsequent delete. Added `_index_fts(node_id)` call.

4. **[C4/Bug]** `NodeService.permanent_delete()` — CRUDService base uses `WHERE uuid = ?` but NodeService uses `node_id`. Added override.

## Medium Fixes
5. **[M1]** `_node_service.py:create()` — `data.pop()` → `data.get()` to avoid mutating caller's dict
6. **[M2]** `_predicate_service.py:delete()` — added warning when `soft=True` ignored
7. **[M3]** Moved `resolve_deprecated()` from `_cli_query.py` to `_cli_helpers.py`
8. **[M4]** Removed dead `else []` branch in `_cli_nodo.py:vidi()`
9. **[M5]** Split `data/storage.py` (540→253 lines) into `data/migrations.py` (312 lines)

## New Tests (16 new, total 243)
- `test_storage.py`: 8 migration tests (nodes uuid→node_id, predicates uuid→predicate_id)
- `test_cli_rubujo.py`: 5 rubujo CLI tests
- `test_cli_export.py`: 4 eksporti Turtle export tests
