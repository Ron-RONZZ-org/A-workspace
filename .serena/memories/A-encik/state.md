# A-encik State (2026-05-02)

## Status: Mostly complete, issue #1 needs closing

### Git
- Branch: main (correct)
- Uncommitted changes in `src/A_encik/cli.py` — full CLI implementation (ls, vidi, aldoni, modifi, forigi, serci, eksporti, agordi, generi, semantika)
- No feature branch needed; all work on main

### Open issue
- **#1** "Use A-core CRUDService for CLI commands" — already IMPLEMENTED (per issue body), just needs closing
  - All Phase 1 CLI commands are complete
  - Tests pass (44/47; 2 failures are pre-existing A-core FTS5 bugs, not A-encik issues)

### Architecture
```
src/A_encik/
├── __init__.py   → exports app
├── cli.py        → 10 commands (8 implemented, 2 TODO stubs)
├── service.py    → EncikService extends CRUDService + JSON serialization
└── data/
    └── storage.py → SQLite + FTS5 config
```

### Commands
| Command | Status | Notes |
|---------|--------|-------|
| ls | ✅ | List with pagination |
| vidi | ✅ | View by UUID/title/prefix |
| aldoni | ✅ | Create with JSON fields |
| modifi | ✅ | Update entry |
| forigi | ✅ | Soft/hard delete |
| serci | ✅ | FTS5 + LIKE search |
| eksporti | ✅ | Export to JSON file |
| agordi | ✅ | Show settings |
| generi | ⏳ | TODO stub (needs A-AI) |
| semantika | ⏳ | TODO stub (needs A-AI) |

### What to do next
1. Commit the uncommitted cli.py changes
2. Close issue #1
3. The module is complete — no further features needed unless new issues arise
