# Issue #17 — A retposto enhancements

## Completed (2026-05-04)

### Fixes Applied
1. **no_args_is_help=True** on retposto/konton typers (was False, inconsistent)
2. **Email in output**: retposto_preni shows account email instead of UUID prefix
3. **Accurate count**: Only accounts WITH passwords are counted before syncing
4. **UUID prefix resolution**: --account flag supports short UUIDs
5. **Better errors**: IMAP connection errors include username@host; concurrent syncs include [email]
6. **Monolith split**: cli.py (1418 lines) → cli/ package (8 files, each <500 lines)
7. **Pre-existing test fixes**: DB isolation fixture, sync_folder signature, malfermi→malfari typo, missing kategorio_app

### Architecture Change
- `src/A_lien/cli.py` → `src/A_lien/cli/` package with 8 modules:
  - `__init__.py` — main app + wire sub-typers
  - `retposto.py` — email commands (preni, sendi, vidi, serci, dosierujoj)
  - `konton.py` — account management (ls, vidi, aldoni, forigi, modifi)
  - `subskribo.py` — signature management
  - `filtraj.py` — Sieve filter management
  - `kontakto.py` — contact read commands (ls, serci, vidi, malfari, purigi)
  - `kontakto_edit.py` — contact write commands (aldoni, modifi, forigi, importi, eksporti)
  - `kategorio.py` — category management

### PR #18 → merged to main, issue closed

## Systematic Review Results

### Confirmed Bug: Double autosave in sync_all()
`retposto_service.py`: `sync_all()` calls `sync_accounts_concurrent()` which internally calls `sync_account()` for each account. `sync_account()` already calls `_autosave_sync_contacts()`. Then `sync_all()` iterates results and calls `_autosave_sync_contacts()` AGAIN. Redundant but not destructive (upsert skips duplicates).

### Monolith Files (>500 lines)
- `src/A_lien/service/retposto_service.py` (530 lines)
- `src/A_lien/service/kontakto_service.py` (610 lines)
- `src/A_lien/imap.py` (546 lines)

### Missing Feature: spamo CLI sub-typer
AGENTS.md lists `spamo` in CLI tree but it was never implemented. DB table `spamo_blokoj` exists.
