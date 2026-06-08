# 2025-05-17: DB hardening extraction to A-core + recovery

## What was done

### A-core: new DB hardening utilities in `A.data.base`
Extracted from A-encik's hard-won experience:
- `backup_db(db_path)` — snapshot DB before DDL (creates `.bak`)
- `health_check(db_path)` — PRAGMA quick_check via read-only `?immutable=1`
- `repair_db(db_path)` — WAL/SHM cleanup + VACUUM rebuild
- `readonly_recover(db_path, dest_path)` — mode=ro copy of readable entries
- `init_db(path, schema_sql, backup, migrate)` — combined factory
- `timeout=5.0` — already in SQLiteDB._get_conn()

### A-encik: refactored to delegate to A-core
- `_backup_db()` → calls `backup_db()` from A-core
- `_repair_if_corrupted()` → uses `health_check()` + `repair_db()` from A-core
- `_readonly_recover()` → delegates to `readonly_recover()` from A-core
- Keeps encik-specific semantika_cache drop/recreate logic

### All modules: updated get_db() with health check + backup
- A-vorto, A-organizi, A-medio, A-agento, A-sekurkopio
- Each `get_db()` now runs `health_check()` + `backup_db()` before DDL
- A-lien not updated (more complex get_db with path parameter)

### Pre-existing bugs fixed in A-organizi
- IndentationError in taglibro.py serci() (bad --gxis→gis refactor)
- NameError 'referenco' → 'referencoj' in forigi() of todo/taglibro/etikedi
- TypeError 'dato_gis' → 'dato_gxis' in okazajo.py serci()
- Test: --gxis→--gis flag name, kalendaro→okazajo subcommand path

### Tests added
- A-encik: 9 tests (TestBackupDb, TestRepairChecked, TestReadonlyRecover, TestInitCacheTable)
- A-core: 1 test (test_sqlitedb_connection_timeout for busy_timeout=5000)
- All: 243 total (A-encik 76 + A-core 167)

## Key numbers
- A-encik storage.py: 165 lines removed, 58 added (net -107)
- A-core base.py: 184 lines added (new utilities)
- All modules: +5 to +6 lines per storage.py (just imports + 2 calls)
- A-organizi: 6 files fixed (5 source + 1 test)

## Files changed
| Repo | Files | Change |
|------|-------|--------|
| A-core | 2 | +184 lines (base.py), +34 lines (test) |
| A-encik | 2 | -107 net (storage.py), -9 lines (test) |
| A-vorto | 1 | +4 lines |
| A-organizi | 7 | +33/-28 (bugfixes), +5 lines (storage) |
| A-medio | 1 | +4 lines |
| A-agento | 2 | +35 lines (context warming), +4 lines (storage) |
| A-sekurkopio | 1 | +6 lines |
