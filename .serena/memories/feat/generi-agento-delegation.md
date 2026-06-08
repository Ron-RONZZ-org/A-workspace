# `encik generi` implemented via A-agento delegation

## What changed
- Replaced the TODO stub in `A-encik/src/A_encik/_cli_special.py` (line 198)
- `encik generi <prompto>` now delegates to A-agento's `generi` function with `formato="enc"`
- If A-agento is not installed, shows error + offers to install via `ensure_dependency`
- Accepts: `--konservi` (`-K`), `--verbose` (`-v`), `--provizanto` (`-p`)
- Does NOT replicate A-agento's full 9-parameter interface — only the most useful options
- Uses runtime detection (no hard dependency on A-agento)

## Files changed
- `src/A_encik/_cli_special.py` — new `generi()` function (53 lines instead of 4-line stub)
- `tests/test_cli.py` — 3 new test cases (requires prompto, no agento, delegation)
- `AGENTS.md` — updated command mapping + note about generi implementation

## Commit
`76902eb` on `main` — `feat: wire encik generi to A-agento with runtime detection`

## Related issues
- Issue #9 (closed): Implemented via delegation to A-agento
