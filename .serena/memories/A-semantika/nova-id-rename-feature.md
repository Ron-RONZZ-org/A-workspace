# --nova-id Feature Implementation (May 2026)

## Summary
Implemented `--nova-id` / `-ni` flag on both `nodo modifi` and `predikato modifi`
commands, resolving Issue #52. Also fixed help text strings that referred to
just 'modifi' instead of the full command path.

## Key Technical Decisions

### Manual Cascade with PRAGMA defer_foreign_keys=ON
- PK rename uses manual SQL UPDATEs in a single transaction
- `PRAGMA defer_foreign_keys=ON` is required because changing the PK
  temporarily orphans FK-referencing rows before they are re-parented
- Without this, SQLite's immediate FK check rejects the PK change

### Transaction Order (NodeService.update_node_id)
1. UPDATE nodes SET node_id = new_id WHERE node_id = old_id
2. UPDATE triples SET subject_uuid = new_id WHERE subject_uuid = old_id
3. UPDATE triples SET object_value = new_id WHERE object_type='uri' AND object_value = old_id
4. FTS: remove old, index new

### Transaction Order (PredicateService.update_predicate_id)
1. UPDATE predicates SET predicate_id = new_id WHERE predicate_id = old_id
2. UPDATE triples SET predicate_id = new_id WHERE predicate_id = old_id
3. UPDATE predicate_group_members SET predicate_id = new_id WHERE predicate_id = old_id
4. FTS: remove old, index new

### Pre-checks (before transaction)
- Source exists
- New ID doesn't already exist
- FK collision detection (defense-in-depth; redundant with 'already exists' check
  due to FK constraints preventing orphan references)

### New Files
- `_id_rename_helpers.py` — shared collision check functions
- `test_nodo_id_rename.py` — 11 tests
- `test_predikato_id_rename.py` — 8 tests

### Known Limitations
- No undo tracking for ID renames (v1)
- Collision checks are defense-in-depth; they never fire independently
  from the 'already exists' pre-check due to FK constraints

## Tests: 448 pass (429 existing + 19 new)
