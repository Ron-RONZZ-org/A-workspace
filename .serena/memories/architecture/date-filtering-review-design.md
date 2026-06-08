# Architectural Decision: A-vorto Date Filtering + Interactive Review

## Part 1: Date Filtering

### Problem
A-vorto `serci --dato-de/--dato-gis` passes raw strings as exact-match filters on non-existent DB column. Broke during migration from autish-legacy.

### Solution
1. **A-core `A/utils/date.py`**: Add `date_range(dato_de, dato_gis) → (iso_start, iso_end)` helper that:
   - Strips hyphens from input (consistent with A-organizi's `_combine_date_time`)
   - Calls `parse_partial_date()` for each bound
   - Returns start-of-day / end-of-day ISO strings
   - Handles single-bound (None means unbounded)

2. **A-core `A/data/search.py`**: Add `range_filters: dict[str, tuple[str|None, str|None]]` parameter to `build_search_query()` that generates `WHERE col >= ? / <= ?` clauses. Backward-compatible (optional parameter).

3. **A-vorto `search_helpers.py`**: In `_run_search()`, call `date_range()` on `dato_de`/`dato_gis` at CLI layer, pass result as `range_filters={"kreita_je": (iso_start, iso_end)}` through service to FTS builder.

### Rationale
- Consistent with A-organizi pattern (parsing at CLI layer)
- `date_range()` encapsulates shared logic (hyphen stripping + start/end-of-day)
- `range_filters` is a 10-line backward-compatible FTS builder extension
- `kreita_je` column already exists (standard CRUDService timestamp); no schema migration

## Part 2: Interactive Vocab Review

### Architecture
- `recenzi_cmd.py` — CLI command, reuses `_run_search()` filter signature from `search_helpers.py`
- `recenzi_helpers.py` — review modes, scoring, celebration, history subcommands
- New tables (`recenzo_sesio`, `recenzo_rezulto`) in existing `vorto.db` via migration system
- Reuses `A.utils.interactive` for prompts

### Schema
Two tables in vorto.db, created via existing migration path in `A_vorto/data/migrate.py`.

### Key Decisions
- Same DB (no separate file) — consistent with A-organizi's multi-table pattern
- Implement modes incrementally: difinoj → flashcards → multiple-choice
- `ORDER BY RANDOM()` for distractor selection (acceptable for typical vocab sizes)
