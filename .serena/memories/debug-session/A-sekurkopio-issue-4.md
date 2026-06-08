# Debugging Session: A-sekurkopio Issue #4

## Summary
**Issue**: A-sekurkopio daemon backup was failing silently; no new backups created despite cron setup.
**Root Cause**: Password path validation used `.exists()` instead of `.is_file()`, allowing directories to pass validation, causing `IsADirectoryError` when `read_text()` was called. Error was caught but hidden by cron's `>/dev/null 2>&1`.

## Fixes Applied

### 1. Password Path Validation (Primary Bug)
- **File**: `A-sekurkopio/src/A_sekurkopio/cli.py`
- **Change**: Line ~490, replaced `.exists()` with `.is_file()` in daemon function
- **Impact**: Now rejects directories explicitly with clear error message
- **Before**:
  ```python
  if not pw_path.exists():
      error("Pasvorta dosiero ne trovita...")
  ```
- **After**:
  ```python
  if not pw_path.is_file():
      error("Pasvorta dosiero ne trovita aux ne estas regula dosiero...")
  ```

### 2. Unhandled ImportError from py7zr
- **Files**: `_do_auto_backup()`, `_export_to_archive()`, `_import_from_archive()` in cli.py
- **Issue**: Lazy import of optional dependency `py7zr` was not caught
- **Fix**: Wrapped all three functions with try/except ImportError
- **Also**: Updated error handlers in eksporti, importi, and daemon to catch ImportError

### 3. Error Logging for Cron (Diagnostic Enhancement)
- **File**: `cli.py`, daemon function
- **New Option**: `--log-dosiero` allows logging errors to a file
- **Rationale**: When daemon runs via cron with `>/dev/null 2>&1`, errors are invisible. New option enables persistent logging.
- **Helper Function**: `_log_error(fh, message)` safely writes timestamped errors to file handle

### 4. Module Docstring Position
- **File**: `cli.py` lines 1-8
- **Issue**: Import was between `from __future__` and module docstring
- **Fix**: Moved `from A import confirm_action` to proper import section
- **Impact**: Module now has proper `__doc__`

### 5. Broken Test Fix
- **File**: `tests/test_service.py`, `test_collect_with_files`
- **Issue**: Monkeypatched `A_sekurkopio.service.data_dir` which doesn't exist
- **Fix**: Changed to mock `A.core.backup_targets.get_backup_targets` (the actual imported function)
- **Result**: Test now passes

## Lessons Learned

### Pattern: `.exists()` is not sufficient for file operations
- `.exists()` returns True for files, directories, and symlinks
- For file-reading operations, always use `.is_file()`
- Similar bugs found in: A-lien, A-core, A-organizi (filed as cross-module issue)

### Pattern: Lazy imports of optional dependencies must be caught
- `py7zr` is an optional dependency declared in `[project.optional-dependencies]`
- Lazy imports inside function bodies are good for performance, BUT
- `ImportError` is NOT a subclass of `OSError` or `ValueError`
- Must add `ImportError` to exception handlers, not rely on broad `Exception` catch

### Pattern: Cron diagnostics trap
- When cron runs with `>/dev/null 2>&1`, all errors vanish
- Should provide optional logging mechanism for long-running daemons
- `--log-dosiero` is a clean solution without forcing mandatory logging

## Cross-Module Issues Filed
- A-workspace issue created for ecosystem-wide `.exists()`→`.is_file()` audit
- Affected modules: A-lien, A-core, A-organizi

## Commit Hash
- `ba175ec` on A-sekurkopio main branch

## Tests
- All 14 tests passing (was 13 passing + 1 failing before fixes)
