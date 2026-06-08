# Bug: `encik serci` crashes on entries with inline links

## Issue #34

**Error:** `AttributeError: 'str' object has no attribute 'get'`

**Root cause:** `_display_html.py:_resolve_inline_links()` → `_replace()` callback passes `target_html` (rendered HTML string) as `entry` arg to `preview_entry()` (aliased as `_pe`). `preview_entry()` expects a dict entry and calls `entry.get("terminologio")` → crash.

**Fix:** replaced `_pe(target_html, ...)` with `preview_html(target_html, ...)` — `preview_html()` accepts a pre-rendered HTML string directly. Removed unused `preview_entry as _pe` import.

**Systematic review:** All other `preview_entry()` call sites correctly pass dict entries. Only this one call in `_display_html.py` was wrong.

**Commit:** `3f6cb3a` on A-encik
