# A modulo Module Registry System

## Location
- A-core repo: `src/A/core/registry.py`, `src/A/utils/interactive.py`, `modules.json`
- A-encik updated to use `select_candidate` from A-core

## Summary
Added `A modulo` CLI command group for module discovery. A curated `modules.json` manifest lives in the A-core repo root and is fetched by clients. Users can list, search, and view module info without leaving the CLI.

## Key Design Decisions
- **No pip wrapping** — users run `pip install` themselves; A-core provides info only
- **stdlib HTTP** — uses `urllib.request`, no new dependency
- **24h TTL cache** at `~/.cache/A/modules.json`, configurable via `module_cache_ttl`
- **Offline fallback** — stale cache used when network unavailable; clear error when no cache
- **Configurable registry URL** — `A_MODULE_REGISTRY_URL` env var or config key

## API

### A.core.registry
```python
fetch_registry(*, refresh=False) -> dict | None
search_registry(query: str) -> list[dict]
get_module_info(name: str) -> dict | None
get_installed_modules() -> list[dict]
```

### A.utils.interactive
```python
select_candidate(candidates, *, columns, row_formatter) -> tuple[int, T] | None
confirm_action(message, *, default=False) -> bool
```

## Test Coverage
- 29 registry tests, 11 interactive tests, 11 CLI tests
- Test patterns use `unittest.mock` + `@patch` for HTTP and entry_point mocking

## CLI
```
A modulo ls                # all available
A modulo ls --instalita   # installed only
A modulo serci <keyword>  # search with multi-select
A modulo info <name>      # module details
```

## Related
- Issue #40, PR #39 (A-core)
- PR #11 (A-encik migration)
