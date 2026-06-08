# cli.py Monolith Split (May 2026)

## What
Split `cli.py` from 569 lines to 216 lines by extracting the 4 largest commands
to per-command modules. All under 250 lines per file (AGENTS.md hard limit).

## Files Created

| File | Lines | Content |
|------|-------|---------|
| `vidi_cmd.py` | 204 | vidi command (UUID/text lookup, clipboard, --html) |
| `aldoni_cmd.py` | 228 | aldoni command (create with duplicate check, ligilo, ref) |
| `modifi_cmd.py` | 234 | modifi command (update with clear-* flags, ligilo) |
| `serci_cmd.py` | 199 | serci command (FTS5, fuzzy, filtered search) |

## Strategy
- Each command module has ONE public function (e.g., `vidi_cmd.cmd_vidi`)
- Registered in `cli.py` via `app.command(name="vidi")(cmd_vidi)`
- Thin commands (forigi, malfari, rubujo, etc.) stayed in cli.py
- `_display_results` moved to `display_helpers.py`
- Zero test changes required — all 94 tests pass unchanged
- No user-facing behavior changes

## Branch/PR
- Branch: `refactor/cli-split`
- PR: #40 → squashed merged to main (commit 225a7f8)
- Issue: #39 (closed by PR)

## Cleanup Also Done
- Removed duplicate `## Testing` section from AGENTS.md
- Updated architecture tree in AGENTS.md
- Updated README.md test count (23 → 94)
