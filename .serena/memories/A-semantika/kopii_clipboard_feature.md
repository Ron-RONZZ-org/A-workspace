# `--kopii/-k` clipboard copy feature (Issue #69)

## Status
Implemented and closed (#69). Merged to main at 489940b.

## Implementation
1. `_cli_triples.py`: `--katex/-k` → `--katex/-K`; dropped `-K` from deprecated `--kodbloko`
2. `_cli_nodo_crud.py`: added `--kopii/-k` flag; `copy_to_clipboard(node_id_val)` after create
3. `_cli_predikato.py`: same pattern for `predikato aldoni`
4. 4 new tests; 534 total pass
5. All 5 user-sim checks pass