# deps-auto-install-fix — COMPLETED

## Goal
Fix `A.utils.deps.ensure_dependency()` — CLI tool's yt-dlp auto-install failed because raw `pip install` was used instead of `ensure_dependency()`.

## Summary
Replaced all raw `sys.executable -m pip install` patterns across the A-ecosystem with `A.utils.deps.ensure_dependency()` which uses uv-first priority and surfaces stderr on failure.

## Results
| Repo | PR | Change |
|------|----|--------|
| A-core | [#94](https://github.com/Ron-RONZZ-org/A-core/pull/94) | Enhanced `ensure_dependency()` with `timeout`, stderr capture, `TimeoutExpired` handling. 11 tests. |
| A-medio | [#16](https://github.com/Ron-RONZZ-org/A-medio/pull/16) | yt-dlp install → `ensure_dependency('yt_dlp', 'yt-dlp')`. 109 tests. |
| A-sistemo | [#23](https://github.com/Ron-RONZZ-org/A-sistemo/pull/23) | psutil install → `ensure_dependency('psutil')`. 55 tests. |
| A-organizi | [#28](https://github.com/Ron-RONZZ-org/A-organizi/pull/28) | A-lien install → `ensure_dependency('A_lien', 'A-lien')`. 197 tests. |
| A-agento | [#61](https://github.com/Ron-RONZZ-org/A-agento/pull/61) | trafilatura install → `ensure_dependency('trafilatura')`. 155 tests. |

## Key Bug Found (A-core tests)
`call_count` in `_import` helper was counting ALL `importlib.import_module` calls (24 from internal `patch()` setup), making the fast-path look successful. Fixed by tracking `fake_call_count` only for `_FAKE_MODULE`.

## Audit
No remaining `sys.executable -m pip install` or `check_call.*pip.*install` patterns found in A-module source code. All user-facing "pip install" messages are in help text (not runtime install code).

## Issue: #16 (closed)

## Goal
Fix `A.utils.deps.ensure_dependency()` — CLI tool's yt-dlp auto-install fails because raw `pip install` is used instead of `ensure_dependency()`.

## Phase 1 (A-core) — DONE
- Enhanced `ensure_dependency()`: added `timeout` param, replaced `check_call(stderr=DEVNULL)` with `subprocess.run(capture_output=True)`, stderr surfacing in error messages, `TimeoutExpired` handling
- Created `tests/test_deps.py` with 11 tests (all passing)
- **Key bug found**: `call_count` in `_import` helper was counting ALL `importlib.import_module` calls (24 from internal `patch()` setup), making the fast-path look successful. Fixed by tracking `fake_call_count` only for `_FAKE_MODULE`.

## Next Phases
1. Commit A-core changes
2. Create GitHub issue on A-workspace
3. Fix A-medio (`_wrapper.py` → `ensure_dependency('yt_dlp', 'yt-dlp')`)
4. Fix A-sistemo (`system_info.py` → `ensure_dependency('psutil')`)
5. Fix A-organizi (`okazajo_retposto.py` → `ensure_dependency('A_lien', 'A-lien')`)
6. Fix A-agento (`_context_helpers.py` → `get_pip_command()`)
7. Audit remaining repos for similar patterns
