# AGENTS.md — Master Context for A Project

This is the root context file for the entire **A** project. AI agents working from the root directory (`.`) should load this file first, then merge with module-specific AGENTS.md when in subdirectories.

---

## Hierarchical Context Model

> When working inside a directory, load the nearest `AGENTS.md` file and merge it with this root file.  
> Local rules override global rules.

**Context resolution order (highest priority first):**
1. Module AGENTS.md (e.g., `A-encik/AGENTS.md`)
2. Root `AGENTS.md` (this file)
3. autish-legacy for reference patterns

---

## Project Overview

**A** is a modular CLI framework — a ground-up rewrite of [autish](https://github.com/Ron-RONZZ-org/autish/) with better architecture.

### Design Principles
1. **Layered architecture**: CLI → Service → Data → Core (no reverse dependencies)
2. **Plugin-based**: each A-* module is independent
3. **Esperanto-first UI** with multilingual support (eo/en/fr)
4. **Minimal, calm output** — no spinners, no animations
5. **SQLite with WAL mode** for persistence

### Modules

| Module | Status | Description |
|--------|--------|-------------|
| [A-core](./A-core/) | ✅ Base | Shared utilities, CLI framework |
| [A-tempo](./A-tempo/) | ✅ | Time/clock (simplest plugin) |
| [A-vorto](./A-vorto/) | ✅ | Wordbook (basic CRUD) |
| [A-encik](./A-encik/) | ✅ | Knowledge encyclopedia |
| [A-sistemo](./A-sistemo/) | ✅ | System management |
| [A-sekurkopio](./A-sekurkopio/) | ✅ | Backup and restore |
| [A-organizi](./A-organizi/) | ? | Calendar+todo+journal |
| [A-lien](./A-lien/) | ? | Email+contacts |
| [A-medio](./A-medio/) | ? | Video+photo+audio |
| [autish-legacy](./autish-legacy/) | Legacy | Original reference |

---

## Architecture

```
src/A/
├── __init__.py           # Plugin discovery, exports
├── cli.py                # Main entry
├── core/                 # Zero dependencies
│   ├── types.py
│   ├── paths.py
│   ├── i18n.py
│   ├── config.py
│   ├── exceptions.py
│   └── service.py        # CRUDService base class (+ FTS5 support)
├── data/
│   ├── base.py           # SQLiteDB
│   └── search.py         # FTS5 schema & query builder
└── utils/
    ├── output.py
    ├── subprocess.py
    ├── editor.py
    └── normalize.py      # Text normalization (ligatures, accents)
```

**Plugin structure:**
```
A_xxx/
├── src/A_xxx/
│   ├── __init__.py       # exports: app
│   ├── cli.py            # Typer app
│   ├── service.py       # Business logic
│   └── data/
│       └── storage.ry    # SQLite
├── tests/
├── pyproject.toml
└── AGENTS.md
```

---

## Common Patterns

### Import from A (never duplicate)

```python
# CORRECT
from A import error, info, tr
from A.core.paths import data_dir
from A.data.base import SQLiteDB
from A.core.service import CRUDService

# WRONG - don't duplicate utilities
from pathlib import Path
import sqlite3
```

### Service Pattern (from A-vorto, A-encik)

```python
# service.ry
from A.core.service import CRUDService
from A_xxx.data.storage import get_db

_service = None

def get_service() -> CRUDService:
    global _service
    if _service is None:
        _service = CRUDService(get_db(), "table_name")
    return _service
```

### Plugin Registration (pyproject.toml)

```toml
[project.entry-points."A.commands"]
xxx = "A_xxx.cli:app"
```

### CLI Commands (Typer)

```python
# cli.ry
import typer
from A import error, info, tr

app = typer.Typer(name="xxx", help=tr("Helr text", "Help text", "Aide"))

@app.command()
def cmd(arg: str) -> None:
    """Help text."""
    ...
```

---

## Code Standards

1. **No bare `print()`** — use `A` output functions
2. **Type hints** on all public functions
3. **Docstrings** on all public functions
4. **Use `tr()`** for all user-facing strings
5. **Use `error()` for errors**, `info()` for info
6. **Tests required** for all modules
7. **WAL mode** for SQLite
8. **Import from `A`** — never duplicate utilities

### CLI Help Text
- Always use Esperanto (`tr()`) first, fall back to English
- Include usage examples
- Document all valid values for restricted options

### Commit Format
Use [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:`, `fix:`, `docs:`, `test:`, `refactor:`

---

## Testing

```bash
# Create venv with deps
uv venv .venv && uv pip install pytest pytest-mock typer rich --python .venv/bin/python

# Run tests
PYTHONPATH=../A-core/src:src .venv/bin/python -m pytest tests/
```

Tests should use `typer.testing.CliRunner` for CLI tests.

---

## What to Avoid

- **Don't use `click`** — use Typer
- **Don't add GUI/TUI widgets** — text-only
- **Don't hardcode paths** — use `A.core.paths`
- **Don't skip documentation** — docs are first-class
- **Don't reinvent** — integrate existing tools
- **Don't duplicate A-core utilities**

---

## Shell Integrations

Some features are better handled as shell aliases than plugins. See issue [#3](https://github.com/Ron-RONZZ-org/A-core/issues/3).

| Feature | Shell Instead | Why |
|---------|--------------|-----|
| kp (clipboard) | `xclip`, `xsel`, `pbcopy` | 60-line wrapper is wasteful for 1 bash command |

---

## Cross-Module Dependencies

### Optional Dependencies (Runtime Detection)

Modules may optionally depend on each other. Use runtime detection:

```python
def cross_plugin_feature():
    try:
        import A_other  # Detect at call time
    except ImportError:
        # Gracefully degrade
        info(tr("Feature requires A-other", "Feature requires A-other"))
        return
```

### Shared Data

In autish, vorto ↔ encik share `ligilo` (link) relations. In A plugins:
- **Detect optional plugins at call time**, not import time
- **Use feature detection** when available
- **Never require** other plugins as hard dependencies

---

## API Reference

### Core Imports (`from A import ...`)

```python
# Types
CommandResult, PluginInfo, Config
# Paths
data_dir, config_dir, cache_dir, state_dir, ensure_dirs
# i18n
tr, set_language, available_languages, get_current_language
# Exceptions
AError, ConfigError, PluginError, DataError, CommandError
# Config
load_config, save_config, get_setting, set_setting
load_profile, save_profile, export_profile, import_profile
# Output
error, info, warning
# Service
CRUDService
# Text Normalization
fold_search_text, normalize_french_ligatures, NORMALIZERS
# Search
FTSConfig
```

### Data Layer

```python
from A.data.base import SQLiteDB
db = SQLiteDB("mydb.db")
db.execute(sql)        # -> list[dict]
db.execute_one(sql)    # -> dict | None
db.transaction()      # context manager
db.raw_connection()   # context manager for lastrowid
```

### Search & FTS5

```python
from A.data.search import FTSConfig, build_fts_schema, build_search_query

# Configure FTS5 for a table
config = FTSConfig(
    table="vorto",
    fts_columns=["teksto"],
    filter_columns=["lingvo", "kategorio"],
    normalize={"teksto": fold_search_text},
)

# Use with CRUDService
service = CRUDService(db, "vorto", fts_config=config)
service.search_fts("query", filters={"lingvo": "fr"})
service.search_fuzzy("heelo", threshold=0.8)  # rapidfuzz if available
service.search_advanced("query", fuzzy=True)
```

### Text Normalization

```python
from A.utils.normalize import fold_search_text, normalize_french_ligatures

fold_search_text("Cœur")           # -> "coeur"
fold_search_text("Été")            # -> "ete"
normalize_french_ligatures("cœur", "fold")    # -> "coeur"
normalize_french_ligatures("coeur", "expand") # -> "cœur"
```

---

## Module-Specific Reference

Each module extends this root. See individual AGENTS.md for details:

| Module | AGENTS.md | Key Differences |
|--------|-----------|--------------|
| A-tempo | [Link](./A-tempo/AGENTS.md) | Simplest — no DB |
| A-vorto | [Link](./A-vorto/AGENTS.md) | CRUD + FTS5 (core-based) |
| A-encik | [Link](./A-encik/AGENTS.md) | CRUD + FTS5 + JSON columns (core-based) |
| A-sistemo | [Link](./A-sistemo/AGENTS.md) | Subprocess-heavy |
| A-organizi | [Link](./A-organizi/AGENTS.md) | Calendar+todos |
| A-lien | [Link](./A-lien/AGENTS.md) | Email+contacts |
| A-medio | [Link](./A-medio/AGENTS.md) | Media handling |

---

## Legacy Reference

[autish-legacy](./autish-legacy/) is the original implementation. Use for:
1. Reference patterns (how to implement features)
2. Edge case handling
3. Known issues/workarounds

**Rule:** When in doubt, consult autish source code.

---

*(End of root AGENTS.md)*

## Branch Convention

All A-* repos use `main` as the primary branch. Use `main` for all development.
