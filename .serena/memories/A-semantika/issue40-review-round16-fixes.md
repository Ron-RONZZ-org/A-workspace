# Issue #40: Code Review Round 16 Fixes

## Date: May 25, 2026

## Fixes Implemented

| Fix | Severity | File | Description |
|-----|----------|------|-------------|
| F1 | Medium | `data/storage.py` | Conditional FTS rebuild — only rebuilds `predicates_fts` if new default predicates were actually seeded |
| F2 | Low | `_node_service.py` | Single `COLLATE NOCASE` query instead of case-sensitive + NOCASE fallback |
| F3 | Low | `_cli_helpers.py`, `_cli_triples.py`, `_cli_modify.py` | `validate_type_flags()` returns `(datatype, object_type)` tuple instead of just datatype |
| F4 | Low | `_cli_query.py` | Replaced `print()` with `sys.stdout.write()` in `eksporti()` |
| F5 | Low | `_cli_modify.py` | Removed redundant FK re-validation (subject/object already validated by `resolve_node_id_prefix()`) |

## Testing
- 370 existing tests pass (unchanged count)
- `TestValidateTypeFlags` tests updated for tuple return type
- User-simulation verified: help, nodo CRUD, predikato CRUD, triple CRUD, serci, eksporti, modifi

## Branch
- fix/review-round16-fixes (merged to main)
- Commit: 845b1a4 (fixes), de9e355 (docs)
- Issue: #40 (closed)
