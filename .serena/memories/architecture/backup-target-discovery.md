# Pluggable Backup Target Discovery

Implements issue #12 from A-workspace: replaces A-sekurkopio's hardcoded DB
list with a pluggable entry-point based mechanism.

## Architecture

### A-core: `A.core.backup_targets`

- `BackupTarget` dataclass (`path`, `category`, `module`, `label`)
- `get_backup_targets()` — combines entry-point discovery + `data_dir()` scan
- Entry point group: `A.backup`
- Scan fallback catches unregistered modules
- Entry points always win over scan (deduplication)

### Per-module registration

Each module with a DB adds:
1. `get_backup_targets()` returning `list[BackupTarget]`
2. `pyproject.toml` entry: `[project.entry-points."A.backup"]`

### Key decisions

- Return type is `BackupTarget` dataclass (not bare Path) to carry metadata
- `category` field distinguishes `data` vs `config` paths (A-sistemo uses config_dir)
- Scan fallback only scans `data_dir()` — config_dir modules must register
- Error isolation: try/except per entry point
- A-sistemo's hardcoded `Path.home()/.config/A/` was fixed to use `config_dir()`

### Files changed

- **New**: `A-core/src/A/core/backup_targets.py`
- **New**: `A-core/tests/test_backup_targets.py` (19 tests)
- **Edited**: A-core, A-sekurkopio, A-sistemo, A-vorto, A-encik, A-organizi,
  A-agento, A-medio, A-lien, A-semantika
- **Skipped**: A-tempo (stateless)
