# Design: Graceful DB Corruption in semantika_cache

## Problem

`_check_db_cache()` raises `sqlite3.DatabaseError` on corrupted DB, preventing CSV/API fallback.

## Design

### Files Changed

1. **`A-encik/src/A_encik/data/storage.py`** — add public `repair_db()` function
2. **`A-encik/src/A_encik/data/semantika_cache.py`** — catch sqlite3 errors, trigger repair, fall through to CSV/API
3. **`A-encik/tests/conftest.py`** (new) — test isolation fixture

### Change 1: Public `repair_db()` in storage.py

Add a public API to decouple semantika_cache from private `_repair_if_corrupted()`:

```python
def repair_db() -> bool:
    """Public API: attempt DB repair. Returns True if repair was needed+succeeded."""
    global _db_instance
    if _db_instance is not None:
        _db_instance.close()
        _db_instance = None          # Force full re-init on next get_db()
    return _repair_if_corrupted()
```

**Order matters**: close stale connection FIRST, then repair WAL/SHM.

Fixes the existing double-repair call in `get_db()` (refactor as separate cleanup).

### Change 2: Error handling in semantika_cache.py

**Import**: add `import sqlite3`

**`_try_repair_db()`** — local helper:
```python
def _try_repair_db() -> None:
    try:
        from A_encik.data.storage import repair_db as _r
        _r()
    except Exception:
        pass
```

**All DB functions** — wrap in `try/except sqlite3.Error`:

| Function | Fallback | Rationale |
|----------|----------|-----------|
| `_check_db_cache()` | `return None` | Continue to CSV/API |
| `_check_negative_cache()` | `return False` | Allow API call |
| `_store_negative_cache()` | no-op | Cache write optional |
| `_batch_store()` | no-op | Cache write optional |
| `invalidate_old_entries()` | `return 0` | Stale data not critical |
| `get_cache_stats()` | `return {"total": 0}` | Stats not critical |

**Disk-full detection**: check `if "disk is full" in str(e).lower(): raise` — don't retry on disk-full.

**`_check_db_cache()` pattern** (example):
```python
def _check_db_cache(keyword: str) -> list[dict] | None:
    try:
        db = _get_db()
        rows = db.execute(...)
        ...
    except sqlite3.Error as e:
        if "disk is full" in str(e).lower():
            raise
        _warn(f"Cache unavailable: {e}")
        _try_repair_db()
        return None
```

**`lookup_property()`** — targeted catch on Layer 1 only:
```python
def lookup_property(keyword: str) -> dict[str, Any]:
    kw = keyword.strip().lower()
    try:
        cache_results = _check_db_cache(kw)
        if cache_results:
            return {"results": cache_results}
    except sqlite3.DatabaseError:
        _warn("SQLite cache unavailable, falling back to CSV/API")

    # Layers 2 and 3 are DB-independent
    csv_results = _check_csv_files(kw)
    ...
```

### Change 3: Test isolation fixture (conftest.py)

```python
@pytest.fixture(autouse=True)
def isolate_db(monkeypatch, tmp_path):
    import A_encik.data.storage as storage_module
    monkeypatch.setattr(storage_module, "_DATA_DIR", tmp_path)
    monkeypatch.setattr(storage_module, "_DB_FILE", tmp_path / "encik.db")
    storage_module._db_instance = None  # Reset singleton between tests
```

### Tests to add (test_semantika_cache.py)

1. `_check_db_cache` returns None on `DatabaseError`
2. `_check_negative_cache` returns False on `DatabaseError`
3. `_batch_store` silently ignores `DatabaseError`
4. `lookup_property` falls through to CSV when DB is corrupted
5. `_try_repair_db()` doesn't raise on healthy DB
6. Disk-full error re-raised (not silently caught)

### Deferred (not in scope)

- Double-repair call in `get_db()` — cosmetic perf issue, not a correctness bug
- FTS5 corruption detection — semantika_cache doesn't use FTS
- Thread safety — single-threaded CLI app
