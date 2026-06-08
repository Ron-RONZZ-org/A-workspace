# Issue #11: Monolith File Split Progress

## Status: All P0/P1 modules split, tested, committed on `refactor/split-monoliths`

### Modules Completed (all green tests)

| Module | Files Split | Test Results |
|--------|-------------|-------------|
| **A-medio** | `youtube.py` (1435→8 files) | 91/91 youtube tests pass; 2 pre-existing storage.py failures (missing SQL constants from prior commit) |
| **A-agento** | `knowledge.py` (682→327), `enhancement.py` (637→310), `storage.py` (532→51) | 78/78 pass |
| **A-encik** | `_search_service.py` (589→10), `semantika_cache.py` (505→34) | 82/83 pass (1 pre-existing semantika help test) |
| **A-lien** | `imap/client.py` (561→308) | 122/122 pass |
| **A-vorto** | `display_helpers.py` (509→251) | 89/89 pass |

### Exceptions (agreed with user)
- A-core: `cli.py` (509), `core/service.py` (747) — risk too high
- A-vorto: `cli.py` (568) — Typer boilerplate, logic already extracted
- A-sekurkopio: `cli.py` (941) — not in scope

### Key Fixes Made During Split
- **A-medio/service.py**: Had 4 methods accidentally omitted (`download`, `estimate`, `get_by_id`, `search_local`) and `batch_download` orphaned outside class. Fixed + test patch paths updated.
- **A-medio/conftest.py**: Test isolation was incomplete — `_strategy.py` uses `from A.core.paths import data_dir` (local import), couldn't be patched via `A.core.paths.data_dir`. Needed `monkeypatch.setattr(strategy_module, ...)`.

### Pre-existing Bugs Found (not caused by split)
- **A-medio/storage.py**: SQL constants (`_CREATE_YOUTUBE_VIDEOS`, etc.) deleted in commit `33968d8` but references remain. 2 tests fail.
- **A-encik**: `test_semantika_shows_help` fails (exit 2 instead of 0) — pre-existing.

### Next Steps
1. User-simulation / smoke test each module
2. Push `refactor/split-monoliths` branches to origin
3. Create PRs and merge to `main` on each module
4. Update AGENTS.md/README.md per module
5. Close issue #11
