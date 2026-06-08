# Code Review Round 14 Fixes — A-semantika

**Branch:** `fix/review-round14-fixes`
**PR:** [#38](https://github.com/Ron-RONZZ-org/A-semantika/pull/38)
**Issue:** [#37](https://github.com/Ron-RONZZ-org/A-semantika/issues/37)
**Tests:** 353 (+9 new)

## Fixes Applied

### B1 — Bulk Triple Query (Medium)
Added `TripleService.get_by_nodes()` that accepts multiple node IDs and fetches all referencing triples in a single SQL query using `WHERE ... IN (...)`. Updated `nodo forigi` to call `get_by_nodes(resolved_ids_list)` instead of looping `get_by_node()` per node. This is O(1) queries instead of O(N).

### Q1 — Shared Constants Module (Low)
Created `_constants.py` with `FTS5_KEYWORDS` frozenset. Both `_node_helpers.py` and `_predicate_service.py` now import from this shared module instead of maintaining separate copies.

### Q2 — Consolidated Triple-Find Logic (Low)
Created `_find_triple_by_spo()` in `_cli_helpers.py` as the single URI→literal→last-resort lookup function. Both `find_triple_direct()` (used by modifi) and the now-removed `_find_triple_for_delete()` (used by forigi) were >80% identical. The new function returns the matched triple dict; callers extract what they need.

### Q4 — Cached Node Label Resolution (Low)
Added `resolve_node_label_from_node()` in `_preview.py` that extracts the display label from a pre-resolved node dict, avoiding redundant `resolve_uuid_prefix()` calls. Updated `build_triple_preview_table()` to use cached subject/object nodes for both label and raw ID display.

### Q5 — Narrowed Exception (Low)
Changed `except Exception` → `except (sqlite3.Error, ValueError)` in `_cli_predikato.py:forigi()`, consistent with the project's systematic exception narrowing culture (14 rounds).

### B2 — Typed Literal Preview Label (Low)
Replaced empty third column in typed literal label row with descriptive text like "Tipita literal (integer)" (trilingual using tr_multi).

