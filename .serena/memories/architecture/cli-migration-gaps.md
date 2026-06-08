# Architecture Decision: CLI Help & Migration Gaps

## Date: 2026-05-03

## Context
Reviewed A-core and all A-modules (A-tempo, A-vorto, A-encik, A-sistemo, A-organizi, A-lien, A-sekurkopio, A-medio, A-agento).

Two gaps identified:
1. Global --help doesn't aggregate all plugin commands effectively
2. No unified migration CLI — each module has standalone migration code

## Gap 1 Decision: Fix + Enhance Existing Discovery

**Problem**: `A --help` should show all installed plugins. The infrastructure exists (entry points + `app.add_typer` in `main()`) but suffers from:
- Dual-registration bug (`main()` and `help_cmd()` both add plugins)
- Redundant `help` command conflicting with Typer's built-in `--help`
- `list` command shows only names, not descriptions

**Decision**: 
1. Remove `help_cmd()` — redundant with Typer's `--help`
2. Extract `_register_plugins()` as single registration point in `main()`
3. Enhance `list` command with descriptions and `--verbose` flag showing subcommand tree
4. Keep `app.add_typer()` for plugin registration (Typer-native grouping)

**Rationale**: Minimal changes. Typer's `--help` already handles aggregation when plugins are registered. The fix is removing the duplicate registration. The enhancement is in `A list --verbose`.

## Gap 2 Decision: Entry Point Discovery for Migrations

**Problem**: `A.core.migration` has `register_migration()`/`migrate_all()` framework but no module calls it. `migri_cmd()` uses hardcoded try/except imports.

**Decision**:
1. Add `A.migrations` entry point group in pyproject.toml of each module
2. Each module gets a `migration_register.py` that calls `register_migration()`
3. Refactor `migri_cmd()` to discover registrations via entry points
4. Keep `migrate_all()` as the orchestrator
5. A-organizi's multi-table result gets aggregated into single `MigrationResult`

**Rationale**: Entry points provide lazy discovery without eager imports. The framework already exists — just needs wiring up.

## Status
Not yet implemented. See task for implementation details.
