# KaTeX Math Rendering in HTML Output

## Summary
Enable rendering of LaTeX math expressions (`$$...$$` block, `$...$` inline) in all HTML output across the A-ecosystem.

## What was fixed

### Bug 1: Mistune math plugin not enabled
- **File**: `A-core/src/A/core/markdown_parser.py`
- **Fix**: Added `plugins=["math"]` to both `create_markdown()` calls in `render_markdown()` and `get_parser()`
- **Effect**: `$$...$$` is now parsed as `<div class="math">` and `$...$` as `<span class="math">`

### Bug 2: KaTeX CDN not included in shared HTML template
- **File**: `A-core/src/A/core/markdown_html_view.py`
- **Fix**: Added KaTeX 0.16.11 CDN CSS + JS + auto-render to `_generate_html_wrapper()` head
- **Public constants**: `KATEX_VERSION`, `KATEX_HTML` (reusable by downstream modules)
- **Cache version**: Bumped to `CACHE_VERSION = 2`, cache key now `v2_` prefix

### Bug 3: KaTeX CDN not included in A-encik's own HTML template
- **File**: `A-encik/src/A_encik/display.py`
- **Fix**: Imported `KATEX_HTML` from A-core and added to `render_entry_html()` head

### Bug 4: vidi --html title not in user locale
- **File**: `A-encik/src/A_encik/display.py`
- **Fix**: Changed `next(iter(terminologio.values()))` to `entry_locale_title(entry)` in:
  - `render_entry_html()` - page title
  - `preview_entry()` - browser tab title
  - `render_linked_graph_html()` - node labels and graph title
  - `_resolve_inline_links()` - preview filenames
- `entry_locale_title()` respects: `--lingvo` flag > LC_ALL/LANG env > A-core config language > eo > en > first available

## Files Changed

### A-core (commit b7f23df)
- `src/A/core/markdown_parser.py` — enable mistune math plugin
- `src/A/core/markdown_html_view.py` — add KaTeX CDN assets + cache version
- `tests/test_markdown.py` — 4 new tests for math plugin + KaTeX CDN

### A-encik (commit 07f06da)
- `src/A_encik/display.py` — add KaTeX CDN + locale-aware titles in all HTML rendering
- `tests/test_cli.py` — 2 new tests for KaTeX CDN presence

## KaTeX Version
- Pinned to `0.16.11` matching autish-legacy
- Auto-render configured with `$$...$$` (block) and `$...$` (inline) delimiters
- `throwOnError: false`, `strict: 'ignore'`

## Issues
- A-core #76 (closed)
- A-encik #29 (closed)

## Known Issue
- `preview_entry()` produces nested HTML documents (two `<html>` tags): `render_entry_html()` generates a full HTML doc, then `preview_html()` wraps it in another. This is pre-existing and should be refactored in a follow-up.
