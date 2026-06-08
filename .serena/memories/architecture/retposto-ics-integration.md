# Architectural Decision: Email-to-Calendar ICS Import

## Decision
Add `--retposto` option to `A-organizi okazajo aldoni` to import .ics attachments from A-lien email messages.

## Key Decisions
1. **Integration logic** lives in `A_organizi/utils/retposto_ics.py` (not in CLI module, not in A-lien)
2. **A-lien** gets one new method: `get_attachment_content(msg_uuid, attachment_uuid) -> bytes | None` on `RetpostoMessagingMixin` — reads BLOB first, falls back to IMAP download
3. **No short flag** for `--retposto` (`-r` taken by `--ripeto`)
4. **Additive semantics**: `--retposto` and traditional event flags coexist (both are processed)
5. **Message UUIDs only** (not account UUIDs) — precise, fast
6. **No A-core changes needed**

## Rationale
- Follows existing runtime detection pattern (`try: import A_lien`)
- Reuses existing `insert_ics_events()` in `A_organizi/utils/ics.py`
- Clean separation of concerns: email stays in A-lien, calendar stays in A-organizi
- `get_attachment_content()` avoids IMAP re-download when BLOB is already stored
