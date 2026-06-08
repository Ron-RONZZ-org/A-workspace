# Issue #70: `--unuo`/`-u` node_id validation + `modifi` object_unit bug

## Summary
- Feature: validate `--unuo` value as existing node_id (resolve via prefix→substring fallback, same pattern as subject/object)
- Bug: `modifi` defines `--unuo` but its INSERT omits `object_unit` column — unit silently dropped

## Architectural Decisions (from @architect)
1. Validate in `aldoni()` and `modifi()` CLI handlers, NOT in `validate_type_flags()`
2. Do NOT add DB-level FK constraint on `object_unit` — application validation suffices
3. No schema changes, no migrations needed
4. No fuzzy suggestions — follow existing error patterns (`tr_multi()` + `error()` + `typer.Exit(1)`)
5. Resolve `unuo` to full `node_id` (like subject/object) before passing to service

## Files to Modify
- `_cli_triples.py:aldoni()` — add ~15 lines of unuo validation after `validate_type_flags()`
- `_cli_modify.py:modifi()` — same validation + fix the INSERT to include `object_unit`
- `_cli_helpers.py:validate_type_flags()` — NO changes (pure combinatoric validator)

## Edge Cases Covered
- Ambiguous prefix → `AmbiguousUUIDError` pattern (existing)
- Unit not found → "Unit not found" error (existing pattern)
- Empty string → handled by `if unuo:` guard
- id-rename cascade not covering `object_unit` is pre-existing gap, not introduced here

Issue: https://github.com/Ron-RONZZ-org/A-semantika/issues/70
