# Code Block Preview: Show Actual Content

## Issue
https://github.com/Ron-RONZZ-org/A-semantika/issues/68

## Summary
Issue #68 — Preview should show actual code block content instead of placeholder.
Closed 2026-06-03. Merged to main at be9c987.

## Changes
1. **_preview_triple.py** — Row 1 now shows actual code value (`val_preview`) 
   instead of `"code (lang)"`. Row 2 shows `"→ {MIME}, {N} chars"`.
2. **_cli_triples.py:370** — After-creation notification uses compact 
   `"{MIME}, {N} chars"` for code blocks (keeps one-line summary clean).
3. **tests/test_preview_helpers.py** — `test_build_code_block_preview` verifies
   content on Row 1, MIME+chars on Row 2, and correct row order.