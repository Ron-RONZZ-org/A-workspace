# Monolith Split & Bug Fixes (2026-05-04)

## Bug Fix: Double autosave in sync_all()
- `retposto_service.py`: `sync_all()` was calling `_autosave_sync_contacts()` redundantly
- `sync_accounts_concurrent()` already calls `sync_account()` which calls `_autosave_sync_contacts()`
- Fix: Removed the redundant loop from `sync_all()`

## Monolith Split
All source files now ≤ 500 lines:

| File Before | Lines | Split Into | Lines each |
|-------------|-------|------------|------------|
| imap.py | 546 | imap/ package (4 files) | 35-328 |
| kontakto_service.py | 610 | kontakto_service.py + kontakto_vcf.py + kontakto_category.py | 83-305 |
| retposto_service.py | 530 | retposto_service.py + retposto_signature.py | 47-500 |
| cli/retposto.py | 530 | retposto.py + retposto_search.py | 135-419 |

## Other Fixes
- Removed duplicate `return True` in `delete_category()` (kontakto_service.py)
- Moved `imaplib` mock paths from `A_lien.imap.imaplib` to `A_lien.imap.client.imaplib`

## New GitHub Issue
- Created #20: Implement spamo CLI sub-typer (spam block management)
- AGENTS.md lists it but it was never implemented; DB table exists
