# PK Modification in A-semantika — Architectural Analysis (May 2026)

## Decision: Approve with modifications

Implement node_id/predicate_id renaming via **manual cascade in the service layer**, NOT via SQL-level `ON UPDATE CASCADE`.

## Why NOT ON UPDATE CASCADE

The `triples.object_node_uuid` column is `GENERATED ALWAYS AS (...) STORED REFERENCES nodes(node_id)`. 
SQLite cannot cascade updates through generated columns — the FK is a check constraint only.
Adding ON UPDATE CASCADE to the other FKs while excluding this one creates an inconsistent design.

## Approach

### NodeService.update_node_id(old_id, new_id, data)
- Separate method (not overloaded `update()`)
- Manual UPDATEs in a single transaction
- Critical order: (1) UPDATE node_id in nodes, (2) UPDATE triples subject_uuid, (3) UPDATE triples object_value
- This order ensures FK on object_node_uuid validates correctly
- Pre-check: new_id doesn't already exist; triple PK collisions
- FTS: remove old, index new
- `object_node_uuid` auto-recomputes from `object_value` (generated column behavior)

### PredicateService.update_predicate_id(old_id, new_id, data)
- Same pattern: manual UPDATEs in transaction
- Order: (1) predicates, (2) predicate_group_members, (3) triples
- FTS: remove old, index new

### CLI
- Add `--nova-id` / `-n` flag to existing `nodo modifi` and `predikato modifi`
- No schema changes needed — existing FKs without ON UPDATE CASCADE suffice

## Risks Mitigated
- Self-referencing triple: same-TX atomicity
- Triple PK collision: pre-check before TX
- FTS rowid: stable across PK change (rowid ≠ PK for nodes)
- object_node_uuid: auto-recomputes; FK validation passes due to correct order

## Non-Changes
- No `ON UPDATE CASCADE` added to any FK
- No synthetic UUID column added
- No new migration needed
