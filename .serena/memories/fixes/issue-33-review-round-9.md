# Issue #33: Code Review Round 9 Fixes

**Date:** 2026-05-25
**Branch:** `fix/review-round9-fixes` → `main` (f0d577c)
**Tests:** 310 total (295 existing + 15 new), all passing

## Fixes

| # | Severity | Description | Files |
|---|----------|-------------|-------|
| B1 | Medium | Case-insensitive COLLATE NOCASE in `resolve_uuid_prefix()` — consistent with trash module | `_node_service.py` |
| B2 | Medium | `predikat-grupo forigi` now uses prefix matching (exact→single→ambiguous→not found) | `_cli_predikat_grupo.py` |
| B3 | Low | LIKE wildcard escaping (`%`, `_`) in `resolve_uuid_prefix()` — same pattern as `_predicate_service.py` | `_node_service.py` |
| B4 | Low | `NodeService.get()` changed from LIKE prefix to exact `= COLLATE NOCASE` match | `_node_service.py` |
| B5 | Low | POSIX trailing newline in Turtle export | `_triple_turtle.py` |
| B6 | Low | SQL-side date filtering in `malplenigi --days N` via `get_trash_older_than()` — avoids loading all trash into memory | `_cli_rubujo.py`, `_node_service.py` |

## Key Implementation Notes

- **LIKE escaping pattern** must match `_predicate_service.py:151`: escape `\` first, then `%`, then `_`, with `ESCAPE '\\'` clause.
- **`get()` vs `resolve_uuid_prefix()` distinction**: `get()` is for exact-match by internal code (update/delete). Prefix resolution goes through `resolve_uuid_prefix()` which has ambiguity detection.
- **Batch resolution pattern**: forigi commands resolve each identifier independently (not failing fast). Errors collected per-item and reported together.
