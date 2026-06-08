# Code Review Round 11 — Literal Modifi, UUID Truncation, Exception Narrowing

Closed as issue #35 on A-semantika: https://github.com/Ron-RONZZ-org/A-semantika/issues/35

## Changes

### Q2: `_cli_predikato.py` — Narrow `except Exception` → `except ValueError`
`PredicateService.update()` only raises `ValueError` — catching `Exception` was unnecessarily wide.

### Q1: `_cli_predikat_grupo.py` — Extract `_match_groups_by_prefix()`
Consolidated duplicate SQL (`SELECT * FROM predicate_groups WHERE group_name LIKE ?`) between `_resolve_group_name()` and `forigi()` into a shared helper function.

### B4: `_cli_modify.py` — Literal Triple Support
**This was the biggest change.** Previously modifi hardcoded `object_type='uri'` everywhere:
- Interactive mode: rejected non-URI triples with a hard error message
- Direct mode: always resolved object as a UUID node, hardcoded `'uri'` in SQL

Now:
- **Interactive mode**: works with any `object_type` (no more rejection)
- **Direct mode**: `_find_triple_direct()` tries URI match first, then searches triples by subject+predicate+object_value for literal match
- **Type flags** added: `--str`, `--int`, `--float`, `--bool`, `--lingvo`, `--unuo` (same as `aldoni`)
- **No-op detection**: compares old vs new on (subject, predicate, object_value, object_type) — not just value
- **DELETE/INSERT**: use correct `object_type` and pass `object_lang`/`object_datatype`
- Preview shows literal values with quotes and language tags

### F1: UUID Display Truncation 8 → 16 Chars
Changed `node_id[:8]` → `node_id[:16]` across ALL CLI files and `_node_service.py:get_display_label()`. Updated `_looks_like_uuid_prefix()` heuristic in `_triple_search.py` from `8<=len<=12` to `8<=len<=16`.

## Tests
4 new tests in `test_triple_modifi_edge.py`: string literal modifi, integer literal modifi, URI→literal conversion, literal no-op.

**Total: 314 tests, all passing.**
