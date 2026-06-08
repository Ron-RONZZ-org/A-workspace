# A-core Bug Fixes

## CRUDService.restore() — Closed Connection (2026-05-02)

**Bug:** `restore()` in `A-core/src/A/core/service.py` had `conn.execute(delete_sql, ...)` OUTSIDE the `with self.db.transaction()` block, operating on a closed connection.

**Fix:** Moved the delete inside the `with` block alongside the insert, matching the pattern used by `_move_to_trash()`.

**File:** `A-core/src/A/core/service.py`, lines 450-455

**Discovered by:** A-organizi test `test_todoj_restore_from_trash`
