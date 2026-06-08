# Architectural Decision: Text Wrapping in Rich Table Displays

## Status
Approved — filed as A-workspace Issue #19

## Problem
Rich `Table` columns across A-modules use `no_wrap=True`, truncating long content.

## Decision
Implement text wrapping with a three-tier policy:
1. **Never wrap** — IDs, `#`, priority, timestamps, type tags, numeric values (`no_wrap=True`)
2. **Wrap with max_width** — labels, titles, descriptions, content (`no_wrap=False, max_width=80`)
3. **Overflow fold** — raw data dumps only (`overflow="fold"`, rare)

## Implementation phases
1. **A-core**: `select_candidate()` gains `no_wrap`/`max_width` in column dicts (backward-compatible)
2. **A-semantika** `_preview.py` split into `_preview_helpers.py`, `_preview_triple.py`, `_preview_node.py`, `_preview_predicate.py`
3. **A-semantika** content columns → `no_wrap=False` (explicit on every `add_column()`)
4. **Other modules** (A-encik, A-organizi, A-agento, A-sistemo): already use Rich's default wrapping on content columns — no changes needed

## Implementation complete
- A-core: commit 1110010
- A-semantika: commit 636891c
- A-workspace Issue #19 closed