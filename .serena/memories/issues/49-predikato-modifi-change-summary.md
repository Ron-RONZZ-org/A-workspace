# Issue #49: predikato modifi silently discards malformed input; nodo/predikato modifi lack change summary

## Summary
Two bugs fixed in A-semantika:
1. `_parse_lang_value_pairs()` only accepted `LANG::TEKSTO` (double colon), silently skipping single-colon entries
2. `predikato modifi` and `nodo modifi` lacked change-summary preview before confirmation

## Root Causes
- `_parse_lang_value_pairs()` checked `if "::" in item` and silently returned `{}` for entries with single `:`
- No no-op detection — identical-data updates reported "Predikato modifita" with only timestamp changing
- Neither `predikato modifi` nor `nodo modifi` showed old→new values before asking for confirmation

## Fixes (commit f915a37)
- `_parse_lang_value_pairs()` now tries `::` first, then single `:`, warns about entries with no separator
- `predikato modifi` uses `build_predicate_modify_preview()` for old→new summary table
- `nodo modifi` uses `build_node_modify_preview()` (new _parse_lang_tag_pairs helper)
- `nodo aldoni` warns about malformed -e/-d entries
- Both modifi commands detect no-op changes and skip the UPDATE

## Files changed
- `src/A_semantika/_cli_predikato.py` — _parse_lang_value_pairs() + modifi() refactor
- `src/A_semantika/_cli_nodo.py` — new _parse_lang_tag_pairs() + modifi()/aldoni() refactor
- `src/A_semantika/_preview.py` — build_predicate_modify_preview() + build_node_modify_preview()

## Testing
All 427 tests pass. Manual verification: single-colon `-e "eo:teksto"` now works, no-op detection shows "Neniu ŝanĝo", malformed entries show warning.
