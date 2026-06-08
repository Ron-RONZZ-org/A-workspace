# Legacy Column Migration — Lessons Learned (titolo removal)

## Problem

The `encik` table had a `titolo` column that was a duplicate of `terminologio.eo`. 
It was removed from the schema definition in `storage.py` but existing databases 
still had the column with `NOT NULL` constraint.

## What went wrong

### 1. Silent DROP COLUMN failure
The original migration code at `storage.py` had:
```python
try:
    db.execute("ALTER TABLE encik DROP COLUMN titolo")
except Exception:
    pass  # ❌ Silent swallow hid the real error
```

This failed because **two indexes** (`idx_encik_titolo_lower`, `idx_encik_titolo_fold`) 
referenced `titolo`. SQLite refuses `DROP COLUMN` if dependent indexes exist.

### 2. Entry creation crashed
`EncikService.create()` and `TimeEntryService.ensure_year/decade/century()` 
passed data dicts without `titolo`, assuming the schema didn't have it. On old DBs 
that still had the column, `INSERT` failed with:
```
NOT NULL constraint failed: encik.titolo
```

### 3. Index dependency check
Before dropping any column, always check for dependent indexes:
```sql
SELECT name FROM sqlite_master 
WHERE type='index' AND sql LIKE '%column_name%'
```

## Fix pattern for column removal

```python
# 1. Drop dependent indexes
for idx_name in ("idx_table_column",):
    db.execute(f"DROP INDEX IF EXISTS {idx_name}")

# 2. Drop the column
db.execute("ALTER TABLE table_name DROP COLUMN column_name")

# 3. Backward-compat: ensure code doesn't crash if column still exists
if "titolo" not in data:
    data["titolo"] = fallback_value
```

## Files modified

| File | Change |
|------|--------|
| `A-encik/data/storage.py` | Drop dependent indexes before DROP COLUMN; log warning on failure |
| `A-encik/service.py` | Auto-set `titolo` from `terminologio.eo` in `create()` for backward compat |
