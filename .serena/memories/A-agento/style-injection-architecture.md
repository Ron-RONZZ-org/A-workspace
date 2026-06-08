# Dynamic Prompt Injection for Writing Style — Architecture Decision

## Decision
Two-phase approach for style adaptation in A-agento:
- **Phase 1 (v0.2.0)**: Few-shot injection of 2-3 user writing samples via XML-delimited prompt sections
- **Phase 2 (v0.3.0)**: RAG-based retrieval with embedding storage and input sanitization

## Rationale
- Few-shot is simple, secure, and requires no additional dependencies
- Full fine-tuning deemed overkill for style emulation (high maintenance cost)
- RAG delayed to Phase 2 to minimize prompt injection attack surface initially
- Structured XML delimiters enforce OWASP-recommended separation between instructions and data

## Security Controls
1. Retrieved content treated as untrusted — sanitized before injection
2. XML tags (`<writing-style>`, `<examples>`, `<sample>`) isolate style from instructions
3. Max 2-3 samples prevents prompt dilution and limits injection surface
4. Confirmation gate on write actions (existing `_confirm_action` pattern) — style only affects drafts
5. Local-only storage — no third-party embedding service in Phase 2

## Key Files
- `prompts.py` — `STYLE_SECTION_TEMPLATE`, `inject_style()`
- `service.py` — Modified `generate_reply()` with style injection
- `storage.py` — New `stiloj` table and CRUD
- `cli.py` — New commands: `stilo`, `stilo-listo`, `stilo-forigu`, `stilo-analizu`

## Issue
https://github.com/Ron-RONZZ-org/A-agento/issues/6
