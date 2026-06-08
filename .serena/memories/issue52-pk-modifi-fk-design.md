# Issue #52: PK Change FK Cascade Design

## Problem
`predikato modifi --nova-id` and `nodo modifi --nova-id` change the primary key of a node or predicate. SQLite FK constraints are checked at **statement level**, not transaction level — so `UPDATE predicates SET predicate_id = ?` fails immediately because `triples.predicate_id` still references the old value.

## Solution
**`PRAGMA foreign_keys = OFF/ON` pattern** — temporarily disable FK enforcement during the PK change transaction:

```python
conn = self.db._get_conn()
conn.execute("PRAGMA foreign_keys = OFF")
try:
    with self.db.transaction():
        # PK change + cascade all FK references
        self.db.execute("UPDATE predicates SET predicate_id = ? WHERE ...", ...)
        self.db.execute("UPDATE triples SET predicate_id = ? WHERE ...", ...)
        self.db.execute("UPDATE predicate_group_members SET predicate_id = ? WHERE ...", ...)
finally:
    conn.execute("PRAGMA foreign_keys = ON")
```

- `PRAGMA foreign_keys` must be set **outside** the transaction (SQLite ignores pragma changes inside a transaction)
- The `try/finally` ensures FK is re-enabled even if the transaction rolls back
- This is the standard, well-documented SQLite pattern for manual FK cascade
- No schema migration needed, no `ON UPDATE CASCADE` changes, no `object_node_uuid` GENERATED column changes

## Why not `ON UPDATE CASCADE`
- Would require schema migration (breaking, complex)
- The `object_node_uuid GENERATED ALWAYS AS ... STORED REFERENCES nodes(node_id)` column in triples table is a generated column — SQLite does not support `ON UPDATE CASCADE` on generated column FK references
- Manual cascade gives us full control over which FK references to update

## Files modified
- `_node_service.py` (FTS + non-FTS paths), `_predicate_service.py` — both use the OFF/ON pattern
