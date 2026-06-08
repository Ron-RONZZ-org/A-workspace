# Issue #41: Code Review Round 17 Fixes

## Date: May 25, 2026

## Fixes Implemented

| Fix | Severity | File | Description |
|-----|----------|------|-------------|
| M1 | Medium | `_cli_predikato.py:366` | Dead fallback — `pred.get("predicate_id", pred["predicate_id"][:16])` eagerly evaluates default, crashes on missing key. Changed to `pred.get("predicate_id", "")[:16]` |
| M2 | High | `_node_service.py:494` | LIKE wildcard escaping — LIKE fallback query did not escape `%`/`_`/`\`. Added `replace("\\","\\\\").replace("%","\\%").replace("_","\\_")` |
| M3 | Medium | `_preview.py:39` | Added clarifying comment for ValueError catch scope |
| M4 | Medium | `_cli_nodo.py:112` | JSON array guard — `json.loads()` can produce list, crashing on `.items()`. Added `isinstance(dict)` guard |
| M5 | Medium | `_triple_turtle.py:64` | URI encoding — `f"<{base_uri}{val}>"` with spaces/quotes produces invalid Turtle. Added `urllib.parse.quote(val, safe='')` |
| L4 | Low | `_cli_rubujo.py:59` | NULL date display — SQLite NULL returns `None`, `.get()` default never triggers. Changed to `(n.get() or "?")[:19]` |
| L5 | Low | `_node_helpers.py:74-76` | Added clarifying comment about `isinstance(val, str)` guard |

## Not Changed
- H1/H2: `except RuntimeError` is correct — A-core wraps all network errors
- L1: `--str` without `--nova-objekto` is a valid use case
- L6: `_label_from_etikedoj` wrapper kept — different signature from `label_from_json`

## Testing
- 13 new regression tests in `test_review_round17.py`
- 390 tests total (377 existing + 13 new), all passing
- User-simulation verified: M2 (LIKE escaping), M4 (JSON array in vidi), L4 (NULL date in rubujo ls), M5 (URI encoding)

## Branch
- fix/review-round17-fixes (merged to main)
- Commits: 5fe30ae (fixes), 4895489 (docs)
- Issue: #41 (created and closed)
