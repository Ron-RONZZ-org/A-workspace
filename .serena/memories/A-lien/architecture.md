# A-lien Architecture Decision Record

## Structure
- Two services in `service/`: `kontakto_service.py` and `retposto_service.py`
- Shared DB `lien.db` at A.core.paths.data_dir()
- Keyring for passwords (local keyring.py until A.core.keyring exists)
- FTS5 on contacts only (messages use IMAP SEARCH)
- JSON arrays for multi-value fields (phones, emails, CC/BCC)

## Implementation Phases
1. Foundation: DB schema + keyring abstraction
2. Contacts: KontaktoService (CRUD + FTS5 + VCF + categories)
3. Accounts: Account CRUD + keyring integration
4. Email: IMAP sync + SMTP send
5. Filters: Sieve + spam blocks + polish

## GitHub Issues
- A-core #24: keyring.py
- A-lien #2: Architecture + refactor (blocks 3,4,5)
- A-lien #3: DB + KontaktoService (phases 1-2)
- A-lien #4: Account mgmt + IMAP/SMTP (phases 3-4)
- A-lien #5: Filters + VCF + polish (phase 5)
