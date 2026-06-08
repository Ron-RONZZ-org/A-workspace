# Pull sync now imports remote-only events

## Summary
`A okazajo sinkronigi` (`pull` operation) previously only updated `remote_href` for events that already existed locally. Remote-only events were silently dropped. Now they are imported.

## Strategy
1. Event exists only on local → kept; auto-push sends it to remote
2. Event exists only on remote → imported into local DB using remote UID as local UUID
3. Event exists on both → remote_href updated; local data preserved (local-first)
4. Dedup by content (title+start+end) before import; skip events without DTSTART

## Key Implementation Details
- New function `_import_remote_event()` in `src/A_organizi/utils/sync.py`
- Uses remote UID as local UUID for round-trip consistency (future push/update reference the correct resource)
- All ICS fields are mapped: DTSTART, DTEND, SUMMARY, LOCATION, CATEGORIES, DESCRIPTION, RRULE, ATTENDEE
- The test isolation fix was critical: `patch.dict("sys.modules")` removes imported modules from `sys.modules` on exit, causing function `__globals__` to reference a different namespace than the patched module. Use `sys.modules["keyring"] = Mock()` instead.

## Files Changed
- `src/A_organizi/utils/sync.py`: +108 lines (helper + pull logic)
- `tests/test_sync.py`: +390 lines (new test class + import isolation fix)
- Issue #37
