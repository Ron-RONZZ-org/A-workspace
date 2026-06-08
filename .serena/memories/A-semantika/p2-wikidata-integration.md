# A-semantika P2 Wikidata Integration (2026-05-22)

## Summary
Implemented Wikidata integration for `predikato serci` and `predikato aldoni`.

## Files Created
- `src/A_semantika/_wikidata_helper.py` — 149 lines, stateless wrapper around `A.core.wikidata`

## Files Modified
- `src/A_semantika/_cli_predikato.py` — added `--wikidata/-w` flag to `serci`, auto-detect in `aldoni`

## Architecture Decisions
1. **Opt-in flag** (`-w`/`--wikidata`) — network fetch only when user explicitly requests it
2. **Separate helper** — `_wikidata_helper.py` adapts `A.core.wikidata` return types to A-semantika's data model
3. **No auto-caching on search** — only `aldoni` writes to DB
4. **User flags override auto-fetch** — explicit CLI args always win
5. **Unified "Label" column** — search results show a single label column instead of separate `label_eo`/`label_en` (since Wikidata returns a single best-match label)
6. **Timeout defaults** — 5s for search, 10s for details fetch (via A-core #83)

## Design Patterns

### serci flow:
1. Always search local DB first (existing LIKE search)
2. If `--wikidata`: call `search_wikidata()` → map results → deduplicate by `predicate_id`
3. Display with unified Label + Fonto columns
4. Empty local results without `-w`: show hint

### aldoni flow:
1. Check if `is_wikidata_id()` → normalize to `wdt:` prefix
2. If Wikidata ID: call `fetch_wikidata_details()` for per-language labels
3. User flags (`-e`, `--en`, `-p`) override auto-fetched values
4. Force `source="wikidata"` for Wikidata IDs
5. Network failure → warning + manual fallback (doesn't crash)

## Edge Cases Handled
- Wikidata ID normalization: `P31` → `wdt:P31`, `p31` → `wdt:P31`, `wdt:P31` → `wdt:P31`
- Non-Wikidata IDs (`rdf:type`, `my:prop`, `foaf:knows`) pass through unchanged
- Local predicate with bare `P42` + Wikidata `wdt:P42` — different entries, no collision
- `--fonto manual` + Wikidata ID → force `source="wikidata"` (error if contradiction)
- Network failure: graceful fallback with warning
- Missing language labels (fr-only property): empty `label_eo`/`label_en` but no crash

## Dependencies
- A-core #82: `get_property_details()` — per-language labels (closed)
- A-core #83: `timeout` param on `search_properties()` etc. (closed)

## Tests
- `tests/test_wikidata_helper.py`: 27 unit tests
- `tests/test_cli.py`: 6 CLI integration tests
- Total: 117 tests, all passing
- All API calls mocked — zero network access in tests

## Commits
- A-core: `e360f9e` feat: add timeout parameter to wikidata API functions (#83) (#85)
- A-semantika: `db6baca` feat: P2 Wikidata integration (#2) (#4)
- A-semantika: `3bcd4ee` docs: update AGENTS.md with P2 status
