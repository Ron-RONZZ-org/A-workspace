# Architecture Decision: i18n Help Text Solution (Issue #35)

## Decision
Standardize ALL CLI `help=` parameters on `tr_multi(eo, en, fr)` exclusively.
Do NOT expand the `tr()` dict for CLI options.

## Rationale
- tr_multi() is self-contained — translation visible at use-site
- Already proven by A-vorto, A-sekurkopio, A-agento (3 fully migrated modules)
- Simple regex tooling can detect violations
- tr() dict is the wrong tool for 800+ unique strings

## Current State
| Module | Status | Pattern |
|--------|--------|---------|
| A-vorto | ✅ Done | tr_multi(eo, en, fr) |
| A-sekurkopio | ✅ Done | tr_multi(eo, en, fr) |
| A-agento | ✅ Done | tr_multi(eo, en, fr) |
| A-encik | ⚠️ Partial | A.console.tr() (needs EO, needs rename) |
| A-lien | ❌ Raw | English-only in options |
| A-medio | ❌ Raw | English-only in options |
| A-tempo | ❌ Raw | English-only everywhere |
| A-sistemo | ❓ Unknown | Needs audit |
| A-organizi | ❓ Unknown | Needs audit |
| A-core | ⚠️ Dict | tr() dict insufficient |

## Action Items
1. **Remove `A.console.tr()`** — confusing 3-arg wrapper, redirect to `A.tr_multi()`
2. **Expand `fix_i18n_help.py`** TRANSLATIONS dict to cover ~250-300 unique strings
3. **Pre-commit hook** — detect bare `help="..."` without `tr_multi()`
4. **Migration order**: A-tempo → A-lien → A-medio → A-encik → A-sistemo → A-organizi → A-core
5. **Update all module AGENTS.md** with i18n help requirements

## Non-Goals
- Do NOT expand tr() dict for CLI options (wrong tool)
- Do NOT use AI-generated translations (unreliable when offline)
- Do NOT use hybrid patterns (ambiguous rules)

## Migration Tool
`fix_i18n_help.py` at workspace root does string replacement:
help="English" → help=tr_multi("Esperanto", "English", "French")
