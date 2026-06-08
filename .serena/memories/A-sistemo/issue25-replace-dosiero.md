# Issue #25: `-R/--replace-dosiero` for espanso aldoni (and modifi)

## Status: ✅ Implemented & Merged
- Commit: 377fdc5 on main
- Branch: feat/espanso-replace-dosiero

## Summary
Added `-R/--replace-dosiero` option to `espanso aldoni` and `espanso modifi` commands.
Allows reading replace content from a text file (`.md`, `.txt`, etc.) for multi-line replace.

## Key Decisions
- Flag: `-R/--replace-dosiero` (pragmatic hybrid, consistent with existing `--replace`)
- Error if both `--replace` and `--replace-dosiero` given (fail-fast, per Ron feedback)
- File validation: exists, is regular file, not binary (null-byte check)
- Applied to both `aldoni` and `modifi` for parity

## Files
- `src/A_sistemo/cli/espanso_alias.py` — `_read_replace_file()` helper + `_resolve_replace_text()` + CLI params
- `tests/test_espanso_alias.py` — 13 tests (aldoni + modifi, happy path + error cases)