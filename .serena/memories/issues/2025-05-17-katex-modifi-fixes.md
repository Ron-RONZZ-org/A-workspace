# 2025-05-17: KaTeX rendering + modifi fixes

## KaTeX Math Rendering (A-core #76, A-encik #29)

### Root Cause
Two independent bugs:
1. **Mistune math plugin not enabled** in `A.core.markdown_parser.render_markdown()` — `$$...$$` was rendered as plain text instead of `<div class="math">`
2. **KaTeX CDN assets not included** in HTML templates — `_generate_html_wrapper()` and `render_entry_html()` lacked KaTeX CSS/JS

### Fix
- `A-core/src/A/core/markdown_parser.py`: added `plugins=["math"]` to both `create_markdown()` calls
- `A-core/src/A/core/markdown_html_view.py`: added `KATEX_HTML` constant with KaTeX 0.16.11 CDN links (CSS + JS + auto-render) + bumped cache to `v2_` prefix
- `A-encik/src/A_encik/display.py`: added `KATEX_HTML` to `render_entry_html()` template
- Tests: 4 new tests (A-core: block/inline math, HTML wrapper, cache key; A-encik: render_entry_html)

### Affected consumers
All downstream modules covered: A-encik, A-vorto, A-lien, A-core CLI

## modifi CLI fixes (A-encik #30)

### Root Cause
Three bugs found in `encik modifi`:
1. `dosiero` was `-D/--dosiero` option instead of positional argument (autish-legacy uses positional). User typed `-d` expecting `--dosiero` but it mapped to `--difino`
2. `-d/--difino` only set `difinio` column but display reads from `difinoj` dict — invisible change
3. `--titolo` only set `titolo` column but display reads from `terminologio` dict — invisible change

### Fix
1. Changed `dosiero` from `typer.Option` to `typer.Argument` (positional) — `encik modifi <uuid> <file.enc>`
2. `-d/--difino` now also updates `difinoj["eo"]` with the value
3. `--titolo` now also updates `terminologio["eo"]` with the value

### Key Files
- `A-encik/src/A_encik/_cli_crud.py` — modifi command
- `A-core/src/A/core/markdown_html_view.py` — KaTeX CDN + cache version
- `A-core/src/A/core/markdown_parser.py` — math plugin
- `A-encik/src/A_encik/display.py` — KaTeX template
