# Bug: LaTeX \t escapes mangled as tab characters

## Issue #36

**Root cause:** `escape_latex_style_backslashes()` in `_compat.py` had `valid_escapes = {"n", "t", '"', "'", "\\"}`. This treated `\t` as a valid TOML escape to keep as-is, but TOML interprets `\t` as tab (0x09). Same for `\n` → newline.

**Affected:** Any LaTeX commands in .enc files: `\theta`, `\tau`, `\times`, `\to`, `\newcommand`, etc.

**Parser fix (b38eb0a):** Removed `"t"` and `"n"` from `valid_escapes` in both multiline and single-line string handlers. Now `\t` → `\\t` (doubled) → TOML sees `\\t` → literal backslash-t.

**Data rehabilitation (b38eb0a):** 
- Added `SearchMixin.fix_latex_escapes()` → replaces literal tab/newline chars with `\t`/`\n`
- Added `--latex` flag to `repacigi` CLI command
- Also fixed a bug where `dif != entry["difinoj"]` was always False (same object ref)

**Manual fix after deploying:** `A encik repacigi --latex` (fixed 478 entries)
