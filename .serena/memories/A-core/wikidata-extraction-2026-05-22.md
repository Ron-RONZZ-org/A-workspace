# A.core.wikidata Package Extraction

## What
Extracted Wikidata API client from A-encik into `A.core.wikidata` package.

## Public API
- `search_properties(query, languages=None)` — searches Wikidata properties, returns enriched results with `ligilo`, `etikedo`, `priskribo`, `aliasoj`, `fonto`
- `get_property_metadata(prop_id, languages=None)` — single property metadata (`etikedo`, `priskribo`, `aliasoj`)
- `search_languages(lingvo=None)` — resolves language codes from user input or env vars
- `COMMON_PROPERTIES` — ~45 pre-seeded common property entries (dict of keyword → list of `{id, label, description}`)
- `get_common_properties()` — returns copy of `COMMON_PROPERTIES`

## Package Structure
```
A/core/wikidata/
├── __init__.py   — re-exports public API
├── _client.py    — private: _api_get, _language_priority, _extract_entity_metadata, _properties_metadata
└── _common.py    — COMMON_PROPERTIES dict, get_common_properties()
```

## Tests
- `A-core/tests/test_wikidata.py` — 24 tests (language resolution, entity extraction, API mocking, common properties)
- Uses `unittest.mock.patch` (consistent with A-core's test_http.py)

## Key Decisions
1. **Package (not module)** — `_client.py` and `_common.py` are private submodules
2. **A-encik backward compat** — local `wikidata.py` is now a thin wrapper (41 lines vs 291)
3. **Cache stays in A-encik** — three-layer cache (`semantika_cache.py`) stays in A-encik (too coupled to A-encik's DB schema)
4. **CSV group management** — stays in A-encik (`semantika/config.py`)
5. **No network in tests** — all mocks, tests pass offline

## Commits
- A-core: `b835884` feat: add A.core.wikidata package extracted from A-encik (#9)
- A-encik: `c6aa5bc` refactor: use A.core.wikidata instead of local Wikidata client
