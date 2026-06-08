# DuplicateTripleError Fix

**Problem:** `_cli_nodo.py:aldoni()` used string matching (`"already exists" in str(e)`) to distinguish duplicate triple errors from other `ValueError`s — fragile to message changes, refactoring, or accidental substring matches.

**Solution:** Introduced `DuplicateTripleError(ValueError)` in `_triple_service.py`. `TripleService.add()` raises it; `_cli_nodo.py` catches it by type instead of parsing the message string.

**Files changed:**
- `_triple_service.py` — new exception class + `raise DuplicateTripleError` instead of `raise ValueError`
- `_cli_nodo.py` — `except DuplicateTripleError: pass` then `except ValueError: raise`

**Backward compatibility:** `DuplicateTripleError` is a subclass of `ValueError`, so any existing `except ValueError` handlers (including tests) still catch it without changes.

**Tests:** 310 pass (unchanged count).
