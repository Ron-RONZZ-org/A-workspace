# Debugging Session: A-sekurkopio Backup Rotation Failure

## Summary
**Issue**: Auto backup rotation was not deleting old backups (10 files existed instead of the configured 5).
**Root Cause**: Test database pollution corrupted the real `~/.local/share/A/sekurkopio.db`, setting `nombro=10` and `dosierujo=/tmp/pytest-.../`.

## Root Cause Chain

### 1. Module-level singleton initialization (Primary Bug)
- **Files**: `cli.py`, `auto_cmd.py`, `export_cmd.py`, `import_cmd.py`, `install_cmd.py`
- **Pattern**: `_service = get_service()` at module level
- **Why it's dangerous**: When pytest imports these modules during test collection, `get_service()` → `get_db()` connects to the **real** database at `~/.local/share/A/sekurkopio.db` BEFORE the conftest `autouse` fixture has a chance to redirect `data_dir`.

### 2. Insufficient conftest cleanup (Secondary Bug)
- **File**: `tests/conftest.py`
- **Pattern**: Only reset `storage_module._db_instance = None`
- **Problem**: The `_service` singletons in all 5 command modules still held references to the old `_SekurkopioService` object, whose `self.db` pointed to the real database. Resetting `_db_instance` created a new DB connection, but the old service objects continued using the stale (real) connection.

### 3. Eager DB init in service class
- **File**: `service.py`
- **Pattern**: `self.db = get_db()` in `__init__`
- **Problem**: Even if the service singleton is lazily created, the DB connection is eagerly opened at construction time.

## Fixes Applied

### A-sekurkopio

1. **`service.py` — Lazy DB initiation**:
   - Changed `self.db = get_db()` → `self._db = None` + `@property db` that creates on first access
   - `_SekurkopioService` can now be constructed without touching the database

2. **`conftest.py` — Reset ALL singletons**:
   - Now resets: `storage_module._db_instance`, `service_module._service`, and `_service` in all 5 command modules (cli, auto_cmd, export_cmd, import_cmd, install_cmd)

3. **`auto_cmd.py` — Validation in `_do_auto_backup`**:
   - Validates `nombro >= 1` (raises ValueError with fix instructions)
   - Handles `OSError` from `sorted()` with `st_mtime`
   - Changed `files[0].unlink(missing_ok=True)` → `files[0].unlink()` with error handling

4. **`auto_cmd.py` — Strategy validation in `cmd_daemon`**:
   - Validates `nombro >= 1` and `dosierujo.exists()` before starting backup

### A-vorto (same pattern)

1. **`service.py` — Lazy CRUDService initiation**:
   - Changed `self.crud = CRUDService(get_db(), ...)` → `self._crud = None` + `@property crud`
   - Mirror fix to the same anti-pattern discovered during systematic review

## Lessons Learned

### Pattern: Module-level singletons are dangerous in test environments
Module-level `_service = get_service()` or similar patterns connect to the real database at import time. Since pytest collects tests before running fixtures, the conftest cannot prevent this connection.

**Always use:**
- Lazy `@property` for database connections
- Lazy function-based initialization (e.g., `def _get_service(): ...`)
- Dependency injection (pass `db` as parameter) for testability

### Pattern: Reset ALL singletons in conftest
When a module has module-level singletons imported by multiple other modules, the conftest must reset EVERY stale reference — not just the factory module's singleton variable.

### Cross-Module Issues
- A-sekurkopio (5 modules): Fixed — lazy db + conftest reset
- A-vorto (1 module): Fixed — lazy CRUDService
- Other repos (A-encik, A-lien, A-semantika, etc.): Already use clean DI patterns — no fix needed

## Commit Hashes
- A-sekurkopio: `bbb1d58` on `main`
- A-vorto: `7b5e569` on `main`

## Tests
- A-sekurkopio: 17/17 passing
- A-vorto: 94/94 passing
