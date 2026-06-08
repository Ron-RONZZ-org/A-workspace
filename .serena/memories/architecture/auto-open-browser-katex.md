# Auto-Open Browser for KaTeX/Images in A-encik

## Decision
When `vidi` or `serci` single-result display encounters an entry with KaTeX (`$$`, `$`) or markdown images (`![]()`), auto-open the browser and inform the user, rather than showing a degraded CLI view with a "use -H" hint.

## Rationale
- Users cannot view KaTeX math or images in the terminal
- Previously required re-running with `-H`/`--open` flag
- Auto-open eliminates this friction

## Design
- **Caller-level check** (not inside `display_entry_panel`): A shared helper `auto_open_if_non_renderable()` is called from both `vidi` and `serci` `_copy_and_show` before `display_entry_panel()`.
- **Configurable opt-out**: `~/.config/A/A-encik/config.toml` → `[display] auto_open_browser = true` (defaults to `true`).
- **`display_entry_panel` unchanged**: Its existing `browser_fallback_hint()` remains as a fallback for when auto-open is disabled or fails.

## Implementation
- `display_helpers.py`: Add `_load_auto_open_browser()` + `auto_open_if_non_renderable(entry) -> bool`
- `_cli_crud.py` (`vidi`): Call helper before `display_entry_panel`, return early if opened
- `_cli_search.py` (`_copy_and_show`): Call helper before `display_entry_panel`, return early if opened
- `display.py`: No changes

## Files affected
- `A-encik/src/A_encik/display_helpers.py`
- `A-encik/src/A_encik/_cli_crud.py`
- `A-encik/src/A_encik/_cli_search.py`
