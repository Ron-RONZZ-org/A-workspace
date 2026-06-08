# vici default filter implementation

## What Changed
`vici` (sync queue listing) default view now hides `completed` jobs, showing only `pending`/`failed` (actionable states). An `--all` / `-a` flag shows everything.

## Why
The sync queue is both a work queue and an audit log. Completed jobs clutter the default view but must remain in DB for debugging. Filter-by-status still works: `vici completed`, `vici pending`, etc.

## Implementation
- `list_sync_queue()` in `sync.py`: now accepts `stato` as `str | tuple[str, ...]` for multi-status filtering
- `vici` in `okazajo_util.py`: defaults to `stato_filter = ("pending", "failed")`; explicit `stato` arg or `--all` overrides this
- No DB changes, no data loss, backward compatible

## Commit
`6f7b512` on `main` (merged from `feat/vici-default-hide-completed`)
Issue #36
