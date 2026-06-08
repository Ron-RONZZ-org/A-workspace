# Issue #8 — CLI Improvements — Complete

## Summary
Multi-phase implementation of CLI improvements for A-semantika:

### R1: --jes flag rename (2026-05-23)
- Renamed `--yes` to `--jes` across 4 CLI files (12 occurrences)
- Kept `-y`/`--yes` backward compat aliases
- Clarified help strings for type flags (`--str`, `--int`, `--float`, `--bool`)

### R2: Partial label search for serci (2026-05-23)
- Created `src/A_semantika/_triple_search.py` with:
  - `resolve_subjects()` — UUID prefix, FTS5 label, or empty
  - `resolve_predicates()` — exact ID or partial LIKE search
  - `resolve_objects()` — UUID prefix, FTS5 label, or raw text
  - `search_triples_by_labels()` — combines all resolvers with limit
- Added `TripleService.search_triples()` — multi-filter with optional subject/predicate/object
- Updated `serci()` CLI to delegate to search_triples_by_labels()

### R3: Interactive search-then-select picker (2026-05-23)
- Added `_pick_triple()` helper in `_cli_triples.py` using `select_candidate` from A-core
- Made `predicate`/`object` optional in `forigi()` and `modifi()` — missing args trigger interactive picker
- Added CLI integration tests: backward compat, subject-only, subject+predicate, no-match
- Fixed fragile UUID parsing in tests by switching from `nodo ls` output parsing to explicit UUIDs

## Key files created
- `src/A_semantika/_triple_search.py` (167 lines)
- `tests/test_triple_search.py` (260 lines)

## Key files modified
- `src/A_semantika/_cli_triples.py` (+228 lines)
- `src/A_semantika/_triple_service.py` (+62 lines)
- `tests/test_cli.py` (+223 lines)

## Test count
151 tests all passing (up from 42 before Issue #8 work).
