# Review Round 7 — B3, RDF-G3, M1 Fixes + Monolith Test Split

## Summary
Three code review fixes applied + monolith test file split. 285 tests total (8 new, all passing).
Issue #30 (closed), PR #29, commit 852c9e7.

## Fixes

### B3: validate_type_flags exit path
- **File:** `_cli_helpers.py:validate_type_flags()`
- **Before:** Warnings only for `--lingvo` without `--str` or `--unuo` without `--int`/`--float`
- **After:** `error()` + `raise typer.Exit(1)` — prevents silent wrong triple type

### RDF-G3: External URI support in Turtle export
- **File:** `_triple_turtle.py:_format_turtle_uri()`
- **Before:** Unknown namespace predicates (e.g. `wdt:P1082`) concatenated with `base_uri` → `https://example.org/wdt:P1082`
- **After:** Unknown prefixes emit as full URIs `<wdt:P1082>`. Known prefixes with invalid local parts resolve to full namespace URIs. Known prefixes with valid local parts still emit prefixed names.

### M1: Group rename prefix ambiguity
- **File:** `_cli_predikat_grupo.py:_resolve_group_name()` (new helper)
- **Before:** `predikat-grupo modifi` used exact match only → prefix input got "not found"
- **After:** Exact match first, then LIKE prefix match, with ambiguity reporting when multiple groups match

## Monolith Test File Split
Split 3 large files (857 + 794 + 594 lines) into 21 focused files:
- `test_edge_cases.py` → 10 files (max ~140 lines)
- `test_cli.py` → 8 files (max ~237 lines)
- `test_storage.py` → 3 files (max ~358 lines)

All source and test files are now under 500 lines.
