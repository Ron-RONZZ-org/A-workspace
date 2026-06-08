# Partial Match Search Design (May 2026)

## Decision
✅ Add partial label matching for subject/predicate/object in `serci` and the interactive `modifi`/`forigi` picker.

## Architecture

### Approach: Two-step lookup via `_triple_search.py` helper
TripleService stays pure (only accepts resolved UUIDs/predicate_ids). Resolution logic lives in a new helper module.

```
User text → resolve (UUID first, then label) → collect UUIDs/IDs → TripleService.search_triples()
```

### New Module: `_triple_search.py`
- `resolve_subjects(node_svc, text) → list[str]`
- `resolve_predicates(pred_svc, text) → list[str]`
- `resolve_objects(node_svc, text) → list[str]`
- `search_triples_by_labels(triple_svc, node_svc, pred_svc, subject?, predicate?, object?, limit) → list[dict]`

### TripleService Changes
- New: `search_triples(subject_uuids?, predicate_ids?, object_values?, object_types?, limit) → list[dict]`
- Takes pre-resolved lists (OR within each list, AND across lists)
- Used by both `serci` and the interactive picker

### Resolution Priority
- Subject: resolve_uuid_prefix() → NodeService.search() via FTS5
- Predicate: get_by_predicate_id() (exact) → PredicateService.search() via LIKE
- Object: resolve_uuid_prefix() → NodeService.search() via FTS5
- Literal objects handled via LIKE on object_value

### Disambiguation Heuristic
- Input ≤ 12 chars, alphanumeric/hyphens: try UUID prefix first
- Otherwise: go straight to label search (avoids unnecessary calls)

### Integration with Issue #8 R3 (Search-then-Select)
The same `search_triples_by_labels()` powers the interactive picker for `modifi`/`forigi`.

### UUID-per-Triple Re-evaluation
Partial matching makes UUID-per-triple even LESS necessary. Search-then-Select + partial labels provides the same UX benefit without schema changes.

### Files Changed
| File | Change | Lines |
|------|--------|-------|
| NEW: `_triple_search.py` | Resolution + search orchestration | ~120 |
| `_triple_service.py` | New `search_triples()` method | ~30 |
| `_cli_triples.py` | Delegate to search module | ~15 |
| NEW: `tests/test_triple_search.py` | Tests | ~150 |

### Related Issues
- A-semantika #8 (main issue tracking all 3 requirements + partial match)
- Comment: https://github.com/Ron-RONZZ-org/A-semantika/issues/8#issuecomment-4524675487
