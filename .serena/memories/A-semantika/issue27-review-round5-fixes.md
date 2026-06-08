# Issue #27: Code Review Round 5 Fixes

## Summary
Code review round 5 identified 3 issues plus a monolith split requirement. All fixed and merged to main (commit ecfb355).

## Fixes

### Q1: Shared Mutable State in TripleService._PREFIX_URIS
- **Problem**: Class-level `_PREFIX_URIS` dict was mutated by `register_prefix()`, affecting all instances globally. Thread-unsafe, test-polluting.
- **Fix**: Renamed to `_DEFAULT_PREFIXES`, copied to instance-level `self._prefix_uris` in `__init__`.
- **File**: `_triple_service.py`

### Q2: Dead Code in _cli_nodo.py:vidi()
- **Problem**: `for lang, val in defns.items() if isinstance(defns, dict) else []` — the `else []` branch was dead because `defns` is always a dict.
- **Fix**: Removed `if isinstance(defns, dict) else []`.
- **File**: `_cli_nodo.py`

### Q3: Broad ValueError Catch in ensure_predicate()
- **Problem**: `_ensure_predicate()` caught `ValueError` and string-matched the error message. Should catch specific exceptions.
- **Fix**: Changed to `except (ValueError, sqlite3.IntegrityError)`.
- **File**: Moved from `_cli_nodo.py` to `_cli_helpers.py` as `ensure_predicate()`.

### Split: _cli_nodo.py Under 500 Lines
- **Problem**: `_cli_nodo.py` was 521 lines (>500 limit).
- **Fix**: Moved `ensure_predicate()` to `_cli_helpers.py`. Now at 499 lines.

## Tests
- 8 new tests added, 274 total, all passing
- `TestTripleServicePrefixIsolation` (2 tests)
- `TestNodoVidiDefinitions` (3 tests)
- `TestEnsurePredicate` (3 tests)

## Monolith Test Files (Not Yet Split)
- `tests/test_edge_cases.py` (858 lines)
- `tests/test_cli.py` (754 lines)
- `tests/test_storage.py` (594 lines)

These test files exceed 500 lines but were not in scope for this fix round.
