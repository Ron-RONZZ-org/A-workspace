# Offline KaTeX for HTML Preview (A-core #77)

## Status: Approved, awaiting implementation

## Decision

KaTeX files are **inlined** into HTML (not `file://` references) because Chrome blocks `file://` → `file://` crossorigin requests.

## Design

1. `KATEX_HTML` becomes a function (not constant) — called at HTML generation time
2. `_ensure_katex()` downloads files to `~/.cache/A/katex/{version}/` on first use with atomic `.part` → rename pattern
3. `_inline_katex_html()` reads files and returns `<style>` + `<script>` blocks with content inlined
4. `_cdn_katex_html()` → fallback to CDN if download fails
5. `CACHE_VERSION` bumped 2→3 to invalidate old HTML
6. A-encik `_display_entry.py` changes `{KATEX_HTML}` → `{KATEX_HTML()}`

## Key constraint

No new Python dependencies — use `urllib.request` from stdlib.
