# 2025-05-17: Dropped legacy titolo column (PR #32)

## What changed
- Removed `titolo TEXT NOT NULL DEFAULT ''` from `_CREATE_ENCIK` DDL
- Migration: backfills `terminologio` from `titolo` for old entries, then `ALTER TABLE DROP COLUMN titolo` (graceful fallback for SQLite <3.35)
- `row_to_dict()` now synthesizes `entry["titolo"]` from `terminologio` for display compat (not DB column)
- `service.create()` no longer writes `titolo` column
- `migrate_from_autish.py`: backfills `terminologio` inline, dropped `titolo` from INSERT
- `_time_entry.py`: removed `"titolo"` from data dicts

## Monolith splits (files > 500 lines)
- `service.py` (592→243): extracted `SearchMixin` into `_search_service.py`
- `display.py` (637→24): extracted into `_display_html.py` (shared helpers), `_display_entry.py` (entry HTML), `_display_panel.py` (Rich Panel CLI), `_display_graph.py` (vis.js graph)

## Key files
| File | Size | Purpose |
|------|------|---------|
| `service.py` | 243 | Core EncikService (CRUD + lifecycle hooks) |
| `_search_service.py` | 352 | SearchMixin (find, search, reconcile) |
| `display.py` | 24 | Facade re-exporting from sub-modules |
| `_display_html.py` | 144 | Shared HTML helpers (_render_field, _resolve_inline_links, _escape_html) |
| `_display_entry.py` | 209 | render_entry_html, preview_entry, maybe_auto_open_browser |
| `_display_panel.py` | 195 | display_entry_panel (Rich Panel CLI output) |
| `_display_graph.py` | 99 | render_linked_graph_html (vis.js) |
| `storage.py` | 354 | SQLite schema, migration, row_to_dict |
