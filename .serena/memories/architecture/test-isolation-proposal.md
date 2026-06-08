# Test Isolation Proposal (Issue A-agento#36)

## Problem
Tests leak data into production paths: SQLite DB at `~/.local/share/A/agento.db` and API keys in system keyring.

## Three Pollution Vectors
1. **SQLite DB**: `storage.get_db()` → `data_dir() / "agento.db"`
2. **Keyring**: `save_api_key()` → `A.core.keyring.set_password()` → real system keyring
3. **Service singletons**: `_db` and `_service` global caches survive test runs

## Solution: Three-Layer Sieve

### Layer 1: Storage module overrides (per-module)
Each `storage.py` exposes `_DATA_DIR: Path | None` and `_DB_FILE: Path | None`.
`get_db()` uses them when set, falling back to `data_dir()`.
Also add `reset_db()` to clear the singleton.

### Layer 2: `autouse=True` conftest fixture (per-module)
Monkeypatches storage paths → `tmp_path`, keyring → in-memory dict, resets singletons.

### Layer 3: A-core testing.py helper (long-term, reusable)
`pytest_plugins = ["A.core.testing"]` + one-liner in conftest.py.

## Priority Order
1. Fix A-agento storage.py (add overrides)
2. Rewrite A-agento conftest.py (add isolation fixture)
3. Clean up test_agordo.py (remove redundant patches)
4. Update AGENTS.md (document pattern)
5. Add A-core testing.py (reusable fixtures)
6. Audit remaining modules

## Key Decision
- **Use monkeypatch + tmp_path, not just `@patch` decorators** — `@patch` is fragile (easy to forget, only covers decorated function, doesn't prevent DB file creation on reads)
- **`autouse=True` is mandatory** — every test runs isolated without individual opt-in
- **Keyring mock uses in-memory dict** — prevents persistent keyring pollution
