# A_DIR Env Var Override — Design Decision

**Issue:** A-core #87 — env var override for path functions

## Decision

Add `A_DIR` environment variable to `A.core.paths` that overrides all four path functions (`data_dir`, `config_dir`, `cache_dir`, `state_dir`).

## Key Points

- **Name is `A_DIR`** (NOT `A_DATA_DIR` as originally proposed in issue #87)
  - Rationale: `A_DATA_DIR` implies only `data_dir()` is affected, but it overrides all 4
  - `A_DIR` is parallel to `JAVA_HOME`, `NODE_PATH` conventions
- **Nesting**: `$A_DIR/data/`, `$A_DIR/config/`, `$A_DIR/cache/`, `$A_DIR/state/`
  - NOT `$A_DIR/A/data/` (no redundant `A/` namespace)
- **Lazy evaluation**: `os.environ.get()` on every call, not at import time
- **Empty string**: treated as unset (falls back to XDG)
- **Relative paths**: resolved to absolute via `.resolve()` at call time
- **No auto-creation**: path functions query, they don't create dirs
- **`patch_paths` simplification**: from 4 monkeypatches to 1 `monkeypatch.setenv("A_DIR", str(tmp_path))`

## Files affected
1. `src/A/core/paths.py` — add `_base()` helper, update 4 functions
2. `src/A/core/testing.py` — simplify `patch_paths`
3. `tests/test_paths.py` — new test file (7 test cases)

## Breaking change
None. Unset `A_DIR` = same XDG behavior as today.
