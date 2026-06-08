# Debug Session: FTS5 Dot Crash & Overbroad Duplicate Detection

## Date: 2026-05-26

## Bugs Fixed

### Bug 1: FTS5 crash with dots in labels
- **Symptoms**: `node_svc.search("John L. Holland")` crashed with `OperationalError: fts5: syntax error near "."`
- **Root cause**: FTS5 query sanitization kept `.` (dot) in tokens. The label "John L. Holland" was split into words "John", "L.", "Holland". The token "L." with trailing dot became `L.*` in the FTS5 query, which FTS5 interprets as column-prefix syntax (column `L`, prefix `*`).
- **Fix**: Removed `.` from allowed characters in `_node_service.py:477` and `_predicate_service.py:370`:
  - Before: `c in ("_", ".")`
  - After: `c == "_"`
- **Files**: `_node_service.py`, `_predicate_service.py`

### Bug 2: No propose-to-update on existing node_id
- **Symptoms**: `nodo aldoni H_JLHOLLAND -e en::John L. Holland` errored with "Node with ID H_JLHOLLAND already exists. Use modifi to modify it."
- **Root cause**: ValueError from `create()` at line 242 was immediately caught and exited with error (lines 243-245). The duplicate-handling code at lines 248-278 was never reached.
- **Fix**: In `_cli_nodo.py:aldoni()`, the `except ValueError` block now checks for "already exists" in the error message. If the node_id was provided and already exists, it shows the existing node info and asks if the user wants to update labels/definitions. In `-y` mode, silently exits with code 0.
- **File**: `_cli_nodo.py`

### Bug 3: Overbroad label-based duplicate detection
- **Symptoms**: Creating `genetika algoritmo` via `snar` falsely detected `ALGORITMO` as a duplicate.
- **Root cause**: The FTS5 search at line 253 used OR between tokens: `genetika* OR algoritmo*`. Any node containing "algoritmo" matched, even when the query was "genetika algoritmo" (two words).
- **Fix**: Changed to AND-like matching via Python post-filter. Get up to 10 FTS candidates, then require ALL query words to appear in the matched node's `label_text`. Single-word queries like "algoritmo" still correctly match "ALGORITMO".
- **File**: `_cli_nodo.py`

## Files Modified
- `src/A_semantika/_cli_nodo.py` - Fixes 2 and 3
- `src/A_semantika/_node_service.py` - Fix 1 
- `src/A_semantika/_predicate_service.py` - Fix 1
- `tests/test_fts5_sanitization.py` - 2 new regression tests for dot in labels
- `tests/test_nodo_errors.py` - Updated assertion for new -y behavior

## Tests: 429 pass (was 427 + 2 new)
