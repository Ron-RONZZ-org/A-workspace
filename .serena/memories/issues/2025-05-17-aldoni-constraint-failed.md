# 2025-05-17: aldoni constraint failed fix

## Root Cause
Triple issue:
1. **titolo not set** when all terminologio values were empty/falsy — `EncikService.create()` had no hard fallback, causing NOT NULL constraint violation on INSERT
2. **Schema mismatch**: `storage.py` had `titolo TEXT,` (nullable) but actual DB had `titolo TEXT NOT NULL` — misleading source code
3. **No IntegrityError handling**: raw SQLite error leaked to user

## Fix
1. `service.py`: hard fallback `data["titolo"] = "sen-titolo"` after existing terminologio iteration
2. `storage.py`: synced schema to `titolo TEXT NOT NULL DEFAULT ''`
3. `service.py`: `create()` and `update()` catch `sqlite3.IntegrityError` → re-raise as `ValueError` with error code
4. Test: `test_create_entry_with_empty_terminologio` verifies fallback works

## Related
- A-encik commit 210cdc2
- A-encik issue #31
