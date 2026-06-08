# Auto-contact creation & IMAP sync pipeline

## Auto-contact helpers (in `A_lien/imap.py`)

- `should_autosave_contact(email_addr)` — filters no-reply, noreply, mailer-daemon,
  and throwaway local-parts (>30 chars, >60% digits). Returns bool.
- `_extract_sender_name(from_header)` — extracts "Name" from "Name <addr@dom.ain>"
- `_parse_email_address(value)` — extracts email from "Name <addr@dom.ain>"

Patterns from autish-legacy, imported into `A_lien/imap.py` as module-level functions.

## MessageStore protocol (in `A_lien/imap.py`)

Protocol class with two methods:
- `get_known_uids(konto_id, dosierujo_id) -> set[str]`
- `store_message(data) -> str`

Implemented by `RetpostoService` in `retposto_service.py`.

## IMAP sync changes

- `sync_folder()` now requires `konto_id`, `dosierujo_id`, and `db_store: MessageStore`
- Uses IMAP UIDs (message_id hash fallback) for dedup against known_uids
- `_store_message()` now actually persists via `db_store.store_message()`
- `sync_account()` requires `konto_id` and `db_store` parameters

## Auto-contact creation triggers

1. **IMAP sync**: After sync, `_autosave_sync_contacts(konto_id)` scans unseen messages
   and upserts contacts from sender addresses.
2. **Send email**: In `send_email()`, after SMTP send, iterates all recipients and
   upserts contacts. Also saves a copy of the sent message to mesagxoj.

## Key files

| File | Purpose |
|------|---------|
| `A_lien/imap.py` | IMAP engine, MessageStore protocol, auto-contact helpers |
| `A_lien/service/retposto_service.py` | MessageStore impl, auto-contact upsert, send+sent-save |
| `A_lien/service/kontakto_service.py` | Contact CRUD + `find_by_email()` |
