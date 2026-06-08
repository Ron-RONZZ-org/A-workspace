# Multi-Select for Triple `forigi` (Issue #66)

## Status
Implemented and merged (June 2026).

## What Was Done
- **A-core**: Added `select_candidates()` function in `A/utils/interactive.py` — same params as `select_candidate()` but returns `list[tuple[int, T]] | None`. Accepts space-separated input. Extracted `_build_candidate_table()` helper shared by both functions.
- **A-semantika**: Added `pick_triples()` in `_cli_helpers.py` — wraps `select_candidates()`. Modified `forigi()` in `_cli_triples.py` to use multi-select with batch delete and single confirmation. Reports `Forigis X el Y arkoj.` (partial failure tolerant).
- `pick_triple()` unchanged — `modifi` still uses single-select.

## Key Design Decisions
- Invalid tokens silently skipped
- Duplicate indices deduplicated via `seen` set
- Batch confirmation: single `confirm_action()` instead of per-triple prompts
- Follows Issue #13 partial-failure reporting pattern

## Files Modified
| File | Change |
|------|--------|
| `A-core/src/A/utils/interactive.py` | `_build_candidate_table()` helper + `select_candidates()` |
| `A-core/src/A/__init__.py` | Added `select_candidates` import |
| `A-core/tests/test_interactive.py` | 8 new tests for `select_candidates()` |
| `A-semantika/src/A_semantika/_cli_helpers.py` | `pick_triples()` function |
| `A-semantika/src/A_semantika/_cli_triples.py` | `forigi()` uses `pick_triples()` |
| `A-semantika/tests/test_cli_triples.py` | 2 new multi-select tests |
| `A-semantika/AGENTS.md` | Documented feature |

## Commits
- `2313e0a` (A-core): feat: add select_candidates() multi-select helper (#66)
- `a460acd` (A-semantika): feat: multi-select for triple forigi (#66)
- `aa7ad9c` (A-semantika): docs: update AGENTS.md with multi-select forigi (#66)
