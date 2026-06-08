# search_encik UUID prefix fix

## Problem
`search_encik` MCP tool returned full 36-char UUIDs to the LLM. The LLM then used these full UUIDs when generating `.enc` files, which is wrong — encik expects 8-character UUID prefixes.

## Files changed
- `A-agento/src/A_agento/tools.py`:
  - `_search_encik()`: truncate each result's UUID with `[:8]`
  - `_get_encik_entry()`: truncate UUID with `[:8]`
- `A-agento/tests/test_tools.py`: update tool count from 3 to 5

## Also fixed (cross-module)
- `A-organizi/pyproject.toml` — added `[tool.uv.sources]`
- `A-lien/pyproject.toml` — added `[tool.uv.sources]`
- `A-agento/pyproject.toml` — added `[tool.uv.sources]`

All three were missing `a-core = { path = "../A-core" }` in `[tool.uv.sources]`, causing `uv run` to fail because uv looked for a-core on PyPI.

## Commit
- A-agento: 5b92198 (closes #52)
- A-organizi: 76eddbc
- A-lien: 853f842
- A-workspace: #6 (cross-module tracking issue)
