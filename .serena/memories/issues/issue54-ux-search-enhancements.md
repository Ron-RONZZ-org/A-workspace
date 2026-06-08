# Issue #54: A-semantika UX/Search Enhancements (May 2026)

## Changes Implemented

### Preview Formatting
- `confirm_node_with_arcs()`: node label+ID shown as heading before arcs table; arcs displayed in 2-column (Predikato / Objekto) table
- `build_triple_preview_table()`: string literal row shows `"literal"` or `"literal, lang: en"` instead of blank
- String literal value moved from Row 2 back to Row 1 (labels row) — was misplaced

### Bold Output (Rich markup)
- `nodo vidi`: `[bold]` on ID, label values, definition values
- `predikato vidi`: Fonto shown before ID; `[bold]` on ID and label values

### Search Flags
- `nodo serci --id`: LIKE search on `node_id` column only
- `predikato serci --id`: LIKE search on `predicate_id` column only
- `nodo serci --lingvo LANG`: `json_extract(etikedoj, '$."LANG"') LIKE ?`
- `predikato serci --lingvo LANG`: same approach
- `nodo serci` plain search: FTS5 fallback also does LIKE on `node_id`
- Invalid language code → error + exit code 1

### Monolith Splits
- `_preview.py` 570→448: predicate helpers to `_preview_predicate.py` (146)
- `_cli_nodo.py` 672→499: forigi+`_format_delete_error` to `_cli_nodo_forigi.py` (190)
- `_cli_predikato.py` 533→481: helpers to `_cli_helpers.py` (489)

### Pre-existing Bug Fixed
- `_cli_helpers.py:194`: missing indent on `raise` statement

### Tests
- 28 new tests in `test_issue54_ux_search.py`
- Updated `test_review_round13.py` import
- Suite: 476 tests pass (448 + 28)

## Key Files
- `src/A_semantika/_cli_helpers.py` — shared helpers (parse_lang_value_pairs, etc.)
- `src/A_semantika/_cli_nodo.py` — nodo commands (vidi bold, serci enhanced)
- `src/A_semantika/_cli_nodo_forigi.py` — nodo forigi (extracted)
- `src/A_semantika/_cli_predikato.py` — predikato commands (vidi format, serci enhanced)
- `src/A_semantika/_preview.py` — preview tables (literal metadata, confirm_node_with_arcs)
- `src/A_semantika/_preview_predicate.py` — predicate preview (extracted)
- `tests/test_issue54_ux_search.py` — 28 new tests
