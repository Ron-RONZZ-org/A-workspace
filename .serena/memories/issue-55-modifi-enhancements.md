# Issue #55: Predicate Merge + Modifi Correctness Fixes

## Changes
- **Predicate merge on rename collision**: `update_predicate_id()` now auto-merges when `new_id` already exists:
  - Labels: old+new+data dict merge (data wins, then new, then old)
  - Source: priority-based (wikidata>owl>rdfs>rdf>manual)
  - `kreita_je`: earliest of old/new
  - Triples: new-wins PK collision resolution
  - Group members: new-wins UNIQUE collision
  - FTS cleanup out of transaction (fixes premature-commit bug)
- **FTS transaction fix** also applied to simple rename path (pre-existing atomicity bug)
- Stale FTS auto-heal: `_ensure_fts()` rebuilds when count mismatch detected

## Commit
`159e7d8` — "feat: auto-merge on predicate rename collision"

## Usage
Now works: `predikato modifi rs:titolo -ni rs:titolon` — merges labels and redirects all triples even if `rs:titolon` already exists.
