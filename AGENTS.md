# AGENTS.md — Workspace for A Project

This is the **workspace root context** — the parent directory containing multiple independent repositories:
- `A-core/` — Core framework
- `A-*/` — A-module plugins
- `autish-legacy/` — Original reference implementation

> **Important:** Each subdirectory is an **independent git repo** with its own `pyproject.toml`, `AGENTS.md`, and commits. Don't treat this workspace like a monorepo.

---

## Project Purpose

**A project** is reimplementing [autish](https://github.com/Ron-RONZZ-org/autish/) features as a modular A-ecosystem:

| Directory | Purpose |
|-----------|---------|
| `A-core/` | Framework (CLI, i18n, SQLite, CRUDService) |
| `A-tempo/` | Time/clock plugin |
| `A-vorto/` | Wordbook plugin |
| `A-encik/` | Knowledge encyclopedia plugin |
| `A-sistemo/` | System management plugin |
| `A-organizi/` | Calendar+todo+journal plugin |
| `A-sekurkopio/` | Backup/restore plugin |
| `A-lien/` | Email+contacts plugin |
| `A-medio/` | Media plugin |
| `autish-legacy/` | **Legacy reference only** — do not modify |

**Goal:** Better modularity, performance, and maintainability than autish-legacy.

---

## Rule: Use A-core Utilities

**All A-modules must import from `A-core`, never reinvent:**

```python
# ✅ CORRECT
from A import error, info, tr
from A.core.paths import data_dir
from A.data.base import SQLiteDB
from A.core.service import CRUDService

# ❌ WRONG - duplicating utilities
from pathlib import Path
import sqlite3
```

---

## Rule: Contribute to Core First

If you need a utility **reusable across A-modules**, don't write it locally — **open an issue on A-core**:

| Need | Action |
|------|--------|
| New i18n string | Open A-core issue |
| New CLI output style | Open A-core issue |
| New data layer feature | Open A-core issue |
| Shared utility function | Open A-core issue |

**Workflow:**
1. Check [A-core issues](https://github.com/Ron-RONZZ-org/A-core/issues)
2. If not covered → create issue describing the need
3. Wait for core enhancement before implementing locally
4. Use runtime detection for optional features


## Rule: use standard `eo` CLI Commands, when possible

Consistent naming reduces user confusion and enables cross-module tooling.

1. **Esperanto names** — all command names in Esperanto
2. **ASCII only** — avoid diacritics (`ĉ`, `ĝ`, `ĥ`, `ĵ`, `ŝ`, `ŭ`) in command names. Use plain ASCII equivalents:
   - `serci` not `serĉi`
   - `restauxrigi` (x-convention) or `restaŭrigi` (if ŭ is acceptable in the locale)
3. **Do NOT use bare `help`/`helpi` commands** `-h/--helpo/--help` flags are sufficient
4. **Domain-specific commands** (e.g., `konekti`, `restarti`, `generi`) are allowed but should be minimized
5. **Hidden aliases** — deprecated commands should be registered with `@app.command(hidden=True)` or `deprecated=True`

#### Standard Commands

| Command | Purpose | Required? | Notes |
|---------|---------|-----------|-------|
| `-h` / `--help` / `--helpo` | Help | **Required** | Configured via `context_settings={"help_option_names": ["-h", "--help", "--helpo"]}`. Do NOT add a bare `helpi` command. |
| `ls` | List items | **Required** for data modules | Alias `list` → `ls` with deprecation where `list` exists. |
| `vidi` | View single item detail | **Required** for data modules | Universal "show entry" command. |
| `aldoni` | Add/create item | **Required** for CRUD modules | |
| `modifi` | Update/modify item | **Required** for CRUD modules | |
| `forigi` | Delete item(s) | **Required** for CRUD modules | Accept multiple positional args for bulk delete. |
| `serci` | Search items | **Required** for data modules | Use ASCII `c` (NOT `serĉi` with diacritic). `serchi` may be kept as deprecated alias. |
| `importi` | Import data | Recommended | |
| `eksporti` | Export data | Recommended | |
| `rubujo` | Trash operations (as subcommand group) | For modules with soft-delete | See "Trash Commands" below. |
| `malfari` | Undo last operation | Optional | Only if module supports undo (A-core `UndoManager`). |

#### Trash Commands (subcommand group style)

Trash operations **must** be grouped under the `rubujo` subcommand, NOT as top-level commands:

| Command | Purpose |
|---------|---------|
| `rubujo ls` | List trashed items |
| `rubujo restaŭrigi` | Restore item from trash (accept `restauxrigi` as alias for keyboard portability) |
| `rubujo malplenigi` | Empty trash (delete older than N days) |
| `rubujo forigi` | Permanently delete specific item from trash |

Implementation pattern (Typer):
```python
trash_app = typer.Typer()
app.add_typer(trash_app, name="rubujo", help=tr_multi(...))
```

### Rule: Multi-lingual Help / User Docs

All user-facing text, including inline help, **must** be delivered in three languages using `tr_multi()`:

```python
tr_multi(
    "Esperanta teksto",   # Primary — shown when locale is unknown
    "English text",       # Fallback
    "Texte français",     # Fallback
)
```

**Order:** Esperanto (eo), English (en), French (fr).

**Where this applies:**

| Context | Function | Example |
|---------|----------|---------|
| CLI help strings (typer.Option/Argument `help=`) | `tr_multi(eo, en, fr)` | `help=tr_multi("Konto UUID", "Account UUID", "UUID compte")` |
| Typer app help | `tr_multi(eo, en, fr)` | `help=tr_multi("Administri kontaktojn.", "Manage contacts.", "Gérer les contacts.")` |
| Info/error/warning messages | `tr_multi(eo, en, fr)` | `info(tr_multi("Konto kreita.", "Account created.", "Compte créé."))` |
| Typer command docstrings | Plain English | Used as `--help` output, written in English |

---

## Hierarchical Context Model

> When working inside a module directory, load that module's `AGENTS.md` first, then merge with this workspace root.

**Context resolution order:**
1. Module AGENTS.md (e.g., `A-organizi/AGENTS.md`)
2. This workspace `AGENTS.md`
3. `autish-legacy/` for reference patterns only

---

## Architecture

### A-core Structure
```
src/A/
├── __init__.py         # Plugin discovery, exports
├── cli.py              # Main entry
├── core/              # Zero dependencies
│   ├── types.py
│   ├── paths.py
│   ├── i18n.py
│   ├── config.py
│   ├── exceptions.py
│   └── service.py      # CRUDService base class
├── data/
│   ├── base.py        # SQLiteDB
│   └── search.py      # FTS5 schema & query builder
└── utils/
    ├── output.py
    ├── subprocess.py
    └── normalize.py  # Text normalization
```

### A-module Structure
```
A_xxx/
├── src/A_xxx/
│   ├── __init__.py    # exports: app
│   ├── cli.py        # Typer app
│   ├── service.py   # Business logic
│   └── data/
│       └── storage.py  # SQLite
├── tests/
├── pyproject.toml
└── AGENTS.md
```

---

## Common Patterns

### Service Pattern (A-modules)
```python
from A.core.service import CRUDService
from A_xxx.data.storage import get_db

_service = None

def get_service() -> CRUDService:
    global _service
    if _service is None:
        _service = CRUDService(get_db(), "table_name")
    return _service
```

### Plugin Registration
```toml
[project.entry-points."A.commands"]
xxx = "A_xxx.cli:app"
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


**Special cases:**
- **User data** (contact names, email addresses, tags) — never translate
- **Technical identifiers** (UUIDs, file paths, DB column names) — never translate
- **Debug/log output** — English only (developers read these)
- **Short inline labels** — single-word labels (e.g. `"(jes)" / "(yes)" / "(oui)"`) use `tr_multi()`

**Concrete example from A-lien:**

```python
@konton.command("ls")
def konton_ls() -> None:
    """List email accounts."""  # ← docstring in English
    service = get_retposto_service()
    accounts = service.list_accounts()
    if not accounts:
        info(tr_multi(           # ← user message in 3 languages
            "Neniuj kontoj.",
            "No accounts.",
            "Aucun compte.",
        ))
        return
    for a in accounts:
        info(f"  {a['uuid'][:8]}  {a['retposto']}")
```

**Typer `help` option names** — always register all three:
```python
context_settings={"help_option_names": ["-h", "--help", "--helpo"]}
```

### Commit Format
[Conventional Commits](https://www Conventionalcommits.org/):
- `feat:`, `fix:`, `docs:`, `test:`, `refactor:`

---

## Testing

```bash
cd A-organizi
uv run pytest tests/ -v
```

Tests should use `typer.testing.CliRunner` for CLI tests.

---

## What to Avoid

- **Don't use `click`** — use Typer
- **Don't add GUI/TUI widgets** — text-only
- **Don't hardcode paths** — use `A.core.paths`
- **Don't skip documentation** — docs are first-class
- **Don't reinvent** — integrate existing tools
- **Don't duplicate A-core utilities** — contribute to core instead
- **Don't modify autish-legacy/** — reference only

---

## Cross-Module Dependencies

Use **runtime detection** for optional dependencies:

```python
def cross_plugin_feature():
    try:
        import A_other
    except ImportError:
        info(tr("Feature requires A-other"))
        return
```

Never require other plugins as hard dependencies.

---

## API Reference

### Core Imports
```python
from A import (
    tr, tr_multi,
    error, info, warning,
    ensure_dirs,
    AError,
    CRUDService,
)
from A.core.paths import data_dir, config_dir
from A.data.base import SQLiteDB
```

### Data Layer
```python
from A.data.base import SQLiteDB

db = SQLiteDB("mydb")
db.execute(sql)        # -> list[dict]
db.execute_one(sql)    # -> dict | None
db.transaction()     # context manager
```

---

## autish-legacy Reference

`autish-legacy/` is the **original implementation** — use only for:
1. Feature reference (what to implement)
2. Edge case handling
3. Known issues/workarounds

**Do not modify autish-legacy/** — it's kept for reference.

---

## Branch Convention

All A-* repos use `main` as the primary branch.

---

## .serena (AI Agent Memory) Convention

**All A-modules track `.serena/memories/`** for cross-developer knowledge sharing. This allows AI agents and developers to access project knowledge (architecture decisions, issue analysis) across sessions and team members.

### Rules

1. **Track `memories/`, not tool config.** Each module's `.gitignore` must exclude:
   - `.serena/cache/` — machine-specific binary caches
   - `.serena/project*.yml` — tool configuration (language server, excluded tools, etc.)
2. **`.serena/.gitignore`** inside the `.serena/` directory ignores `/cache` and `/project.local.yml`
3. **Memories are semi-permanent.** Don't rely on them for critical documentation — AGENTS.md files are still the canonical source. Memories augment, not replace.
4. **Review before committing.** Memories written by AI agents may contain inaccuracies. Edit or delete outdated memories.
5. **No secrets in memories.** Never commit API keys, passwords, or credentials to memories (same rule as any other file).

### Structure

```
.serena/
├── .gitignore           # Ignores /cache and /project.local.yml
├── project.yml          # Tool config (machine-specific, ignored by git)
├── project.local.yml    # Local overrides (ignored by git)
├── cache/               # Binary symbol caches (ignored by git)
└── memories/            # Tracked in git
    ├── architecture/    # Architectural decisions and rationale
    └── issues/          # Issue analysis and proposals
```

---

*(End of workspace AGENTS.md)*
