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

## Cross-Module Issues

**Issues with cross-module impact** (design decisions, shared standards, API compatibility, breaking changes) must be filed on **this repo** ([A-workspace](https://github.com/Ron-RONZZ-org/A-workspace/issues)), not on individual module repos.

Examples of cross-module issues:
- Adding a new standard CLI command format
- Changing the plugin discovery mechanism
- Updating i18n conventions
- Introducing a shared utility that affects multiple modules

Module-specific bugs or features go on each module's own issue tracker.

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
2. **Verb infinitive form** — command names must be verbs in their base/infinitive form (`-i` suffix). Examples: `aldoni`, `forigi`, `modifi`, `vidi`, `generi`, `agordi`. Avoid nouns (`agordo`, `listo`, `helpo`) — use the verb form (`agordi`, `ls`, `helpo` is not needed since `-h`/`--help` suffices). The only exception is `ls` (universally recognized abbreviation).
3. **ASCII only** — avoid diacritics (`ĉ`, `ĝ`, `ĥ`, `ĵ`, `ŝ`, `ŭ`) in command names. Use plain ASCII equivalents:
   - `serci` not `serĉi`
   - `restauxrigi` (x-convention) or `restaŭrigi` (if ŭ is acceptable in the locale)
4. **`no_args_is_help=True`** for Typer apps with subcommands — calling without args shows help instead of "Missing command". Root apps with `invoke_without_command=True` and a callback are exempt.
5. **Do NOT use bare `help`/`helpi` commands** `-h/--helpo/--help` flags are sufficient
6. **Domain-specific commands** (e.g., `konekti`, `restarti`, `generi`) are allowed but should be minimized
7. **Hidden aliases** — deprecated commands should be registered with `@app.command(hidden=True)` or `deprecated=True`

#### Standard Commands

| Command | Purpose | Required? | Notes |
|---------|---------|-----------|-------|
| `-h` / `--help` / `--helpo` | Help | **Required** | Configured via `context_settings={"help_option_names": ["-h", "--help", "--helpo"]}`. Do NOT add a bare `helpi` command. |
| `ls` | List items | **Required** for data modules | Alias `list` → `ls` with deprecation where `list` exists. |
| `vidi` | View single item detail | **Required** for data modules | Universal "show entry" command. |
| `aldoni` | Add/create item | **Required** for CRUD modules | must have duplicate verification: propose to modifi if similar entry exists |
| `modifi` | Update/modify item | **Required** for CRUD modules | |
| `forigi` | Delete item(s) | **Required** for CRUD modules | Accept **multiple positional args** for bulk delete. See [`forigi` Contract](#forigi-contract-crud-modules) below. |
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

##### `forigi` Contract (CRUD Modules)

All `forigi` commands **must**:

1. **Accept multiple positional args** — use `list[str] = typer.Argument(...)` or `Annotated[list[str], typer.Argument(...)]` for the primary identifier parameter.
2. **Iterate independently** — each input identifier must be resolved independently. Failure, ambiguity, or not-found on one must not block the remaining items. Report per-item and continue.
3. **Show batch preview** — before deletion, display a summary table of all successfully-resolved items with their display names and truncated UUIDs (or domain-appropriate primary identifiers).
4. **Single confirmation** — ask once "Delete these N items?" with `default=False`. Accept `-y`/`--jes`/`--yes` to skip.
5. **Partial success report** — after the operation, report "Deleted X of M items." with details on individual failures.
6. **Respect identifier types** — use the domain-appropriate identifier (UUID prefix, name, predicate ID, etc.). Not all `forigi` commands use UUIDs.

**Exceptions:**
- Root commands operating on fundamentally different identifiers (e.g., SPO triples in A-semantika) may use a separate pattern, documented with rationale.
- `rubujo forigi` permanently deletes a specific trashed item — still accepts multiple identifiers.

**Canonical implementation pattern:**
```python
@app.command("forigi", help=tr_multi("...", "...", "..."))
def forigi(
    identifiers: list[str] = typer.Argument(
        ...,
        help=tr_multi("... (pluraj)", "... (multiple)", "... (plusieurs)"),
    ),
    yes: bool = typer.Option(
        False, "-y", "--jes", "--yes",
        help=tr_multi("Preterpasi konfirmon", "Skip confirmation", "Ignorer la confirmation"),
    ),
) -> None:
    \"\"\"Delete items.\"\"\"
    svc = get_service()

    # Phase 1: Resolve all identifiers
    resolved: list[dict] = []
    errors: list[tuple[str, str]] = []
    for ident in identifiers:
        try:
            item = svc.resolve(ident)
            if item:
                resolved.append(item)
            else:
                errors.append((ident, tr_multi("ne trovita", "not found", "non trouvé")))
        except Exception as e:
            errors.append((ident, str(e)))

    # Report resolution errors
    for input_val, reason in errors:
        error(tr_multi(
            "Forigi {i}: {r}", "Delete {i}: {r}", "Supprimer {i} : {r}",
        ).format(i=input_val, r=reason))

    if not resolved:
        error(tr_multi("Nenio forigebla.", "Nothing to delete.", "Rien à supprimer."))
        raise typer.Exit(1)

    # Phase 2: Batch preview
    if not yes:
        from rich.table import Table
        from rich.box import SIMPLE as BOX_SIMPLE
        table = Table(show_header=True, box=BOX_SIMPLE, header_style="bold")
        table.add_column("UUID", no_wrap=True)
        table.add_column(tr_multi("Etikedo", "Label", "Étiquette"), no_wrap=True)
        for item in resolved:
            table.add_row(item["uuid"][:8], _get_display_name(item))
        info(table)

        from A.utils.interactive import confirm_action
        if not confirm_action(
            tr_multi(
                "Ĉu forigi {n} erojn?", "Delete {n} items?", "Supprimer {n} éléments?",
            ).format(n=len(resolved)),
            default=False,
        ):
            info(tr_multi("Nuligita.", "Cancelled.", "Annulé."))
            raise typer.Exit(0)

    # Phase 3: Delete each
    deleted = 0
    for item in resolved:
        try:
            svc.delete(item["uuid"])
            deleted += 1
        except Exception as e:
            error(tr_multi(
                "Eraro forigante {u}: {e}",
                "Error deleting {u}: {e}",
                "Erreur lors de la suppression de {u} : {e}",
            ).format(u=item["uuid"][:8], e=str(e)))

    info(tr_multi(
        "Forigis {d} el {t} eroj.",
        "Deleted {d} of {t} items.",
        "Supprimé {d} sur {t} éléments.",
    ).format(d=deleted, t=len(resolved)))
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
| Typer command help text | `tr_multi(eo, en, fr)` | Set via `@command(help=tr_multi(...))` or `app.command(help=tr_multi(...))` |
| Command function docstring | English | Internal developer docs only — NOT shown in CLI `--help` |

### Rule: interactive config / TOML config storage

Modules with > 5 user-facing options **must** expose all of them through three channels:

| Channel | Audience | When |
|---------|----------|------|
| CLI options (`--flag`) | All users | Quick tweak, scripting |
| Interactive modal | New users | First-time setup guidance. **Must prompt for ALL user-facing options**, not just a subset. If the user invokes the command without flags, every configurable option should be offered interactively. |
| TOML file (direct edit) | Power users | Sharing configs, dotfiles |

#### Priority order (higher wins)

```
CLI flag > TOML file > hardcoded default
```

A module should load config in this order:
1. Parse TOML file for baseline values
2. Override with CLI-flag values at invocation time

#### TOML file location

**Always per-module, never shared.** Every module gets its own file at:

```python
from A.core.paths import config_dir

# ~/.config/A/A-modulo/config.toml
path = config_dir() / "A-modulo" / "config.toml"
```

No shared `~/.config/A/config.toml` — per-module consistency is more important than reducing the file count. Use `tomllib` (stdlib, Python ≥ 3.11) for parsing.

#### Secrets warning

**Never store API keys, passwords, or tokens in TOML files.** TOML files are plain text and easily committed to version control by accident.

- Secrets → system keyring via `A.core.ai.save_api_key()` or `keyring` directly
- Everything else (model names, UI preferences, server URLs) → TOML is fine

#### Implementation: use A-core `ConfigSchema`

**Do not implement the three channels manually.** A-core provides a `ConfigSchema` utility that derives CLI options, interactive prompts, and TOML read/write from a single schema:

```python
from A.core.config import ConfigSchema

schema = ConfigSchema("A-modulo", {
    "provider": {"type": "str", "default": "ollama", "help": "LLM provider"},
    "timeout":  {"type": "int", "default": 30,      "help": "Request timeout (s)"},
    "color":    {"type": "bool", "default": True,    "help": "Enable colors"},
})

# One call generates CLI flags, interactive prompts, and TOML persistence.
# TOML path: ~/.config/A/A-modulo/config.toml
```

Feature request: https://github.com/Ron-RONZZ-org/A-core/issues/60

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
9. **UUID primary key** for all data tables — use `uuid TEXT PRIMARY KEY` for every table that stores user-facing entries. Exceptions (e.g., singleton configs, append-only logs, import caches without cross-references) must document the reason. UUIDs prevent collision bugs like A-agento#32 where `(provider, profile)` was non-unique.

10. **UUID first column in `ls` output** — all `ls`/`list` commands must display UUID as the first column. This allows users to quickly reference entries by UUID for `vidi`, `modifi`, `forigi`, and other commands. Exception: tables where UUID is not the primary identifier (rare).


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

## Package Manager: `uv` is Required

All A-ecosystem development **must** use `uv` as the package manager:

| Operation | Command |
|-----------|---------|
| Install dependencies | `uv pip install <pkg>` |
| Install project in dev mode | `uv pip install -e .` |
| Run tests | `uv run pytest tests/` |
| Install CLI tools (poetry, etc.) | `uv tool install <tool>` |
| Add dev dependency | `uv add --dev <pkg>` |

**Exceptions:**
- `pip` in README install instructions is acceptable for end users who may not have `uv`
- Readthedocs platform build may require `pip` (platform constraint)
- Runtime `install-on-confirmation` code may fall back to `pip` if `uv` is unavailable (see A-core AGENTS.md)

---

## Testing

```bash
cd A-organizi
uv run pytest tests/ -v
```

Tests should use `typer.testing.CliRunner` for CLI tests.

### Test Isolation (MANDATORY)

Every A-module test suite **MUST** have an `autouse=True` fixture that isolates all external side effects:

| Side effect | Isolation method |
|-------------|-----------------|
| Database path | `patch_paths(monkeypatch, tmp_path)` — redirects `data_dir`, `config_dir`, `cache_dir`, `state_dir` to `tmp_path` subdirectories |
| System keyring | `patch_keyring(monkeypatch)` — mocks `save_api_key` and `get_api_key` |
| Network calls | Mock all HTTP/IMAP/SMTP calls (never reach real servers) |

**Canonical pattern** (uses `A.core.testing`):

```python
# tests/conftest.py
import pytest
from A.core.testing import patch_paths, patch_keyring

@pytest.fixture(autouse=True)
def isolate_module(monkeypatch, tmp_path):
    patch_paths(monkeypatch, tmp_path)
    patch_keyring(monkeypatch)
    # Module-specific singleton resets go here...
    # e.g. storage_module._db = None
    # e.g. service_module._service = None
```

This is the **required** pattern for all modules. See `A.core.testing` for details.

**Rule:** `@patch` decorators are for controlling return values, NOT for isolation. The `autouse` fixture is the safety net. Tests that write to real databases or keyrings will be rejected in code review.

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
