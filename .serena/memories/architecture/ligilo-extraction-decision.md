# Architecture Decision: HTML→Text Extraction for `--ligilo`

## Decision
Add **trafilatura** as an optional dependency in **A-agento** for main-content extraction from web pages. Keep the current `_html_to_text()` as a zero-dep fallback.

## Rationale
- Boilerplate removal (nav, sidebar, footer) is a **different problem** from math content handling
- Trafilatura is the best-in-class tool for boilerplate removal: actively maintained, battle-tested, precision/recall tuning
- A-core has a "zero deps for core/" policy — extraction code already lives in A-agento
- A-agento already uses optional deps (openai, ollama) and has the lazy-import pattern

## Library Comparison (rejected alternatives)
- **html2text/markdownify**: No boilerplate removal — would make output worse (converts nav HTML to markdown)
- **readability-lxml**: Returns HTML (needs extra strip step), less maintained, similar lxml dep
- **boilerpy3**: Less maintained, Java-port algorithm less robust on diverse page structures

## Critical Bug Discoveries (math content)
Three bugs in the current `_html_to_text()` cause the PreTeXt math page failure:

1. `<script>` tags entirely skipped → MathJax `<script type="math/tex">` content is lost
2. `\mathbf{x}` regex eats content → `[^}]*` in pattern captures braces content
3. Short `\`-prefixed lines are dropped → actual inline math lines skipped

**Trafilatura doesn't fix these** — it also strips `<script>` tags. A separate pre-processing step `_extract_mathjax(html)` is needed that both extraction paths benefit from.

## Implementation Guidelines
- Add `ligilo` optional dependency group: `trafilatura>=2.0.0`
- Implement `_extract_with_trafilatura(html)` with lazy import + install-on-first-use
- Add pre-processing step before both extraction paths
- Keep `_html_to_text()` as fallback with math bugfixes

## Cost-Benefit
- ✅ ~200KB dep for dramatically cleaner content
- ✅ Active maintenance
- ❌ lxml C extension install complexity (mitigated by fallback)
- ❌ Doesn't fix JS-rendered pages or PDFs (separate features)
