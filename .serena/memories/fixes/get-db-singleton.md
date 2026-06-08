# get_db() Singleton Caching Fix (May 2026)

## Problem
`get_db()` in `storage.py` returned a new `SQLiteDB` connection on every call.
When multiple services called `get_db()` within the same request flow, multiple
sqlite3 connections accessed the same WAL-mode database file concurrently,
causing "database is locked" errors with 5-second timeouts.

## Affected Modules
All A-* modules using `A.data.base.SQLiteDB` had this pattern:
1. **A-vorto** (`storage.py`) — fixed in commit a13afda, issue #38
2. **A-organizi** (`data/storage.py`) — fixed same pattern, issue #26
3. **A-sekurkopio** (`data/storage.py`) — fixed same pattern, issue #5

## Fix Pattern
```python
_db_instance: SQLiteDB | None = None

def get_db() -> SQLiteDB:
    global _db_instance
    if _db_instance is not None:
        return _db_instance
    # ... create connection, init schema ...
    _db_instance = db
    return db
```

## Test Changes
- Added `test_get_db_is_singleton` test to each repo
- Updated conftest.py to reset `_db_instance = None` between tests
- Set `A_DIR` env var in conftest to redirect all A-core paths to `tmp_path`
  (prevents `LinksDB`/`backup_db()` from writing to real `~/.local/share/A/`)

## A-sekurkopio Bonus: cli.py Monolith Split
Found and fixed cli.py at 999 lines (exceeded 500-line limit):
- Extracted to: export_cmd.py (118), import_cmd.py (122), auto_cmd.py (340), install_cmd.py (304)
- cli.py reduced to 85 lines
