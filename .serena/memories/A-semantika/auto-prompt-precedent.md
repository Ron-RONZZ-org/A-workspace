# Auto-Prompt on Duplicate: Precedent in A-encik & A-vorto

## Fact Finding

### A-encik Implementation (from _cli_aldoni.py:242-265)
When `.enc` file with duplicate `terminologio` is imported:
1. Detects duplicate via `service.find_by_terminologio()`
2. Shows error message with UUID
3. **Prompts user:** `"Ĉu ĝisdatigi? (J/n)"` (interactive prompt with typer.prompt)
4. On "yes" → calls `service.update()` and shows success
5. On "no" → returns without error (interactive cancel)

**Key constraints:**
- Only applied when `--dosiero` path is provided (file-based import)
- Time-based entries (--jaro, --jardeko, --jarcento) use different code path with `ensure_*` methods
- Direct API still errors on duplicate

### A-vorto Implementation (from cli.py)
When `aldoni <word>` is called:
1. Checks for duplicate via `_find_duplicate(teksto)`
2. Shows info message: `"Jam ekzistas: \"word\" (UUID)"`
3. **Prompts UNLESS `-y` is passed:** `confirm_action(default=False)` (from A-core)
4. On confirmation → calls `service.update()` 
5. On cancel → returns silently
6. On `-y` (skip) → skips prompt, goes straight to create logic

**Key constraints:**
- Only when interactive (respects `-y` flag)
- Uses `confirm_action()` from A-core (proper Yes/No with NOCASE handling)
- **Single entry point** — all `aldoni` flows go through this

## Cross-Module Pattern

| Module | Pattern | Behavior | Constraints |
|--------|---------|----------|-------------|
| A-encik | Auto-prompt | File-based only; direct API errors | `.enc` import feature |
| A-vorto | Auto-prompt | All `aldoni`; respects `-y` | Interactive-aware |
| **A-semantika (proposed)** | **(To decide)** | — | — |

## User Feedback Signal
User states: "user feedback is positive" (for A-encik & A-vorto implementations).

No quantitative data provided; claim based on observed usage patterns.

## Architectural Notes
- **Not a breaking change:** Both A-encik and A-vorto have this feature built-in from inception
- **Semantic model:** "aldoni existing → update instead" is the current A-encik/A-vorto expectation
- **Flag consistency:** A-vorto uses `-y` (same as A-semantika AGENTS.md), respects it correctly
- **Precedent for A-semantika:** Would be **consistent with sister modules**, not novel or risky
