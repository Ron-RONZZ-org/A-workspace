# Issue #67 — `aldoni` KaTeX, Code Block flags & `-d`→`-D` rename

**Issue:** https://github.com/Ron-RONZZ-org/A-semantika/issues/67

## Architectural Decision (2026-06-03)

Key decisions made by @architect (summarized):

### Schema: No DDL changes
- Use existing `object_datatype` column with custom datatype URIs
- KaTeX: `object_datatype = 'https://w3id.org/autish/katex'`
- Code: MIME type in `object_datatype` (e.g. `text/x-python`)
- `object_type` stays `'literal'` — 100% backward compatible

### Code Language → MIME type
- `--kodlingvo/-L` maps short names ("python", "javascript") to MIME types
- Stored in `object_datatype`, not `object_lang` (which is for BCP-47 language tags)
- A `LANG_TO_MIME` dict in `_cli_helpers.py` or `data/storage.py`

### Validation rules
- `--katex`/`--kodbloko`/`--str`/`--str-dosiero`/`--int`/`--float`/`--bool` are all mutually exclusive
- `-L` requires `-K`; `-l` requires `-s`/`-D`
- KaTeX: strip `$...$` delimiters, no syntax validation
- `-d` kept as deprecated alias for `-D` with warning

### Files needing changes (~10 files, ~30 new tests)
See issue body for full list.

### Files NOT needing changes
`_triple_service.py` (add() already accepts object_datatype), `_triple_turtle.py` (custom datatype handler exists), `_triple_search.py` (LIKE search works as-is), `_cli_modify.py`, node/predicate/rubujo modules.
