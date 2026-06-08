# Spamo CLI + Sieve Server Sync (#20, #26)

## Completed (2026-05-04)

### What was built
1. **cli/spamo.py** — 4 commands:
   - `ls` — list local spam blocks
   - `aldoni <rule>` — add rule (lowercase, stripped with UNIQUE constraint)
   - `forigi <uuid>` — delete by UUID
   - `sinkronigi --account <uuid>` — push all rules to ManageSieve server

2. **service/retposto_spamo.py** — RetpostoSpamoMixin:
   - CRUD via CRUDService on `spamo_blokoj` table
   - `is_spam(sender)` substring check
   - `sync_spam_blocks_to_sieve(uuid)` — wrapped merge into active Sieve script

3. **sieve_spamo.py** — Pure functions:
   - `generate_spam_sieve(rules)` — Sieve if-block with `fileinto "Junk"`
   - `merge_spam_sieve(existing, section)` — marker-based merge

### Architecture Decisions
- Wrapped merge strategy: `# A-lien spam rules begin/end` markers
- Partition rules: email (@) → `address :contains`; domain → `address :domain :contains`
- Sieve sync is optional via `--account` flag; explicit `sinkronigi` for recovery
- Best-effort: local mutation always succeeds, Sieve failures warn user

### Merge: PR #28 → main
Issues #20 and #26 closed.
