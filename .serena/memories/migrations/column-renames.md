# A-semantika Column Rename Migrations

## Why migrations are needed

Schema changes (e.g., renaming `uuid` → `node_id`) use `CREATE TABLE IF NOT EXISTS` which does **not** alter existing tables. Without explicit migration code, existing databases crash with `OperationalError: no such column: <new_name>`.

## Migration functions in `data/storage.py`

Both are called from `init_db()` after the schema DDL runs:

### `_migrate_nodes_uuid_to_node_id()`
- Target: `nodes` table (PK renamed from `uuid` to `node_id`)
- Also handles `nodes_fts` (FTS5, dropped and recreated) and `nodes_rubujo`
- Triggered by commit 19be0ff (PR #15)

### `_migrate_predicates_uuid_to_predicate_id()`
- Target: `predicates` table (PK changed from `uuid` to `predicate_id`)
- Uses CREATE+INSERT+DROP+RENAME (safer for PK changes)
- Also handles `predicates_rubujo`
- PredicateService updated: `create()` no longer generates uuid, `update()`/`delete()` use `predicate_id`

## Tables that still use `uuid` PK (intentionally)
- `predicate_groups` — `group_name` is mutable (rename feature exists)
- `predicate_group_members` — references `predicate_groups(uuid)`
- `triples` — compound PK without uuid

### `_migrate_predicates_uuid_to_predicate_id()`
- Target: `predicates` table (PK changed from `uuid` to `predicate_id`)
- ALSO handles legacy column conversion: `label_eo`/`label_en`/`priskribo` (original schema 590d9b1) → `etikedoj`/`priskriboj` JSON (schema 035a4f5+)
- Uses CREATE+INSERT+DROP+RENAME (safer for PK changes)
- Handles both column layouts via SQLite `json_object()` for legacy → JSON conversion
- Also handles `predicates_rubujo`

## Tables that still use `uuid` PK (intentionally)
- `predicate_groups` — `group_name` is mutable (rename feature exists)
- `predicate_group_members` — references `predicate_groups(uuid)`
- `triples` — compound PK without uuid

## Adding a new migration (playbook)