## Key Learnings from #11 Fix

### Bug: A-agento was completely unimportable

The CLI module had **3 syntax errors** that blocked all imports:

1. **`cli.py`** — Duplicate `else:` in `agu()` command loop
2. **`contract.py`** — Nested `"""` inside outer `"""` docstring closed it prematurely
3. **`prompts.py`** — Duplicate malformed `__all__` entries outside the list

### Secondary: Missing import + wrong function name in `service.py`

- `warning()` was called but not imported from `A`
- `get_active_samples_by_type` doesn't exist (should be `get_active_samples`), but was actually unused anyway

### FTS5 Query Sanitization

Raw email text (with periods, apostrophes, quotes) passed to FTS5 `MATCH` causes `OperationalError`. All FTS5 query input must be sanitized — `_sanitize_fts_query()` in `storage.py` strips non-alphanumeric chars and joins with OR.

### Testing

- Mock the `get_agent_service` too when testing CLI commands (the real service accesses DB)
- 33 tests pass after fixes
