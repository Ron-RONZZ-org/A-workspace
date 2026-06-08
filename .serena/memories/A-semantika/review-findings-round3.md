# Issue #25: Review Findings Round 3 — Code Quality & Orphan Prevention

**Date:** May 2026
**Branch:** `fix/review-findings-round3` (merged to main)
**Tests:** 254 total, all passing

## Fixed Issues

| # | Severity | File | Description |
|---|----------|------|-------------|
| F1 | Medium | `_cli_rubujo.py` | Removed dead `node_svc` parameter from `_resolve_trash_node()` |
| F2 | Medium | `_cli_nodo.py` | Pre-resolve arc targets before node creation — prevents orphan node on ambiguous `--tipo`/`--superklaso`/`--ne`/`--invers` |
| F3 | Medium | `_triple_service.py` | Replaced `_KNOWN_PREFIXES` tuple with `_PREFIX_URIS` dict; added `register_prefix()` method; dynamic `@prefix` in Turtle export |
| F4 | Low | `_cli_modify.py` | No-op modifi (same old=new) skips delete+insert, preserving `kreita_je` |
| F5 | Low | `_node_service.py` | `create()` catches `sqlite3.IntegrityError` instead of broad `Exception` |
| F6 | Low | `tests/test_cli_rubujo.py` | 6 new tests for interactive confirm paths without `-y` |

## Key Design Decisions

1. **Orphan prevention (F2):** Instead of try/finally cleanup, we restructured to resolve ALL arc targets BEFORE creating the subject node. This is cleaner — no partial state to clean up.
2. **Namespace prefixes (F3):** `_PREFIX_URIS` dict enables extensibility. Users can call `triple_service.register_prefix("foaf", "http://xmlns.com/foaf/0.1/")` for custom namespaces.
3. **IntegrityError (F5):** Using `except sqlite3.IntegrityError` is both faster (no string parsing) and safer (won't swallow unrelated DB errors).

## Verification
- All 254 automated tests pass
- User simulation confirmed each fix end-to-end
- Turtle export produces valid prefixed names with all 5 standard namespaces
