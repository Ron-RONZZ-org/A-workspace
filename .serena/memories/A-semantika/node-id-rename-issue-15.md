# Issue #15: Human-Readable Node IDs + Graceful Error Handling

## Column Rename: `nodes.uuid` → `nodes.node_id`

The `nodes` table was renamed from `uuid` to `node_id` to support human-readable IDs like `SPACO`, `HOMOTEST`.

### Key Implementation Details

**A-semantika scope only** — predicates, predicate_groups, and other tables keep `uuid`. Other modules (A-encik, A-vorto) keep auto-generated UUIDs.

**NodeService overrides 7 CRUDService methods** because CRUDService hardcodes `uuid` column:
- `get()`, `delete()`, `_move_to_trash()`, `restore()`, `_remove_from_fts()`, `_index_fts()`, `_ensure_fts()`

**FTS5 is fully self-contained** — does NOT use A-core's `build_fts_schema()` or `build_index_sql()` (both hardcode `uuid`):
- `_ensure_fts()` creates FTS table with `node_id UNINDEXED`
- `_index_fts()` builds INSERT manually with `node_id` column

**C1 removed** — UUID format validation was removed. Human-readable IDs like `SPACO` are accepted without any format check.

### Files Changed (13 source + 1 docs)
- `data/storage.py` — schema + FTS5
- `_node_service.py` — full rewrite of FTS and CRUD overrides
- `_cli_nodo.py`, `_cli_triples.py`, `_cli_modify.py`, `_cli_query.py`, `_preview.py` — node dict access
- `_triple_search.py`, `_triple_service.py` — node uuid references
- `tests/test_nodes.py`, `tests/test_edge_cases.py`, `tests/test_triple_search.py`, `tests/test_triples.py`

**Test status:** 216/216 passing.

## Alternative Considered
- Modifying A-core `CRUDService` / `build_fts_schema` / `build_index_sql` — rejected for scope isolation
