# Issue #23 — retposto vidi UUID prefix fix

## Completed (2026-05-04)

### Bug: Two Issues Found
1. **Primary**: `retposto vidi` did not support UUID prefixes (only exact match)
2. **Secondary**: `get_message()` queried `kontoj` (CRUDService's table) not `mesagxoj`

### Fix (PR #24 → merged to main)
- `get_message()` now directly queries `SELECT * FROM mesagxoj WHERE uuid = ?`
- Added `find_message_by_uuid_prefix()` to RetpostoService (matches `find_by_uuid_prefix()` for accounts)
- Added `_resolve_message()` CLI helper — exact match → prefix → 0/many handling
- Extracted contact auto-save to `RetpostoContactMixin` (`retposto_contact_mixin.py`)
- Pattern matches `_resolve_account()` in `cli/konton.py`

### Files affected
| File | Change |
|------|--------|
| `service/retposto_contact_mixin.py` | NEW — extracted from retposto_service.py |
| `service/retposto_service.py` | Fix get_message, add find_message_by_uuid_prefix, wire contact mixin |
| `cli/retposto.py` | Add _resolve_message, update retposto_vidi_mesago |
