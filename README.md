# A-workspace

Shared workspace context for the **A-ecosystem** — a collection of modular CLI framework plugins.

## Purpose

This repo serves three functions:

1. **Developer tooling** — scripts for common development workflows (`tools/`)
2. **LLM/AI agent context** — `AGENTS.md` provides the master architecture, conventions, and API reference
3. **Cross-module issue tracker** — file issues here when they impact multiple `A-*` repos

## Contents

| Location | Description |
|----------|-------------|
| `AGENTS.md` | Master context — architecture, patterns, API reference (for humans and AI agents) |
| `tools/a-sync-all` | Reinstall all A-modules in editable mode |
| `tools/a-branch-cleanup` | Audit branches across all A-modules |
| `tools/recover_encik_db.py` | A-encik database recovery utility |
| `tools/recover_raw.py` | Raw data recovery utility |

## Usage

```bash
# Reinstall all modules after mass changes
./tools/a-sync-all

# Check for stale branches across all repos
./tools/a-branch-cleanup
```

## Modules

Each module extends this workspace:

| Module | Repository |
|--------|-----------|
| A-core | https://github.com/Ron-RONZZ-org/A-core |
| A-lien | https://github.com/Ron-RONZZ-org/A-lien |
| A-tempo | https://github.com/Ron-RONZZ-org/A-tempo |
| A-vorto | https://github.com/Ron-RONZZ-org/A-vorto |
| A-encik | https://github.com/Ron-RONZZ-org/A-encik |
| A-sistemo | https://github.com/Ron-RONZZ-org/A-sistemo |
| A-organizi | https://github.com/Ron-RONZZ-org/A-organizi |
| A-sekurkopio | https://github.com/Ron-RONZZ-org/A-sekurkopio |
| A-medio | https://github.com/Ron-RONZZ-org/A-medio |
| A-kunpiloto | https://github.com/Ron-RONZZ-org/A-kunpiloto |
| A-papero | https://github.com/Ron-RONZZ-org/A-papero |
| A-semantika | https://github.com/Ron-RONZZ-org/A-semantika |
| A-agento | https://github.com/Ron-RONZZ-org/A-agento |

## Updating

When master context changes:

1. Update `AGENTS.md` or `README.md` or `tools/` here
2. Push to GitHub

## License

GPL-3.0-only (same as A modules)
