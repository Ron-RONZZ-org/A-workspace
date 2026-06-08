# A-semantika: nodo kunfandi (node merge) — Architectural Decision

**Issue:** https://github.com/Ron-RONZZ-org/A-semantika/issues/64  
**Date:** 2026-06-02  
**Status:** Approved by @architect, issue filed, not yet implemented

## Problem
User accidentally created duplicate nodes `HOMO_SAPIENS` and `HOMO_SAPIEN` (typo). No mechanism to merge nodes in A-semantika.

## Solution
Add `A semantika nodo kunfandi <fonto> <celo>` subcommand.

## Key Architectural Decisions

1. **CLI placement**: subcommand under `nodo` group (not root command), consistent with `aldoni/modifi/forigi/vidi/ls`
2. **Transaction pattern**: Single transaction with `PRAGMA defer_foreign_keys=ON`, following `update_node_id()` pattern
3. **Label merge**: target-first dict merge `{**source, **target}`
4. **Triple reassignment**: UPDATE (not DELETE+INSERT) — SQLite `STORED GENERATED object_node_uuid` auto-recomputes
5. **Triple PK conflicts**: source triples that would collide with target's (P,O) are skipped via `WHERE NOT EXISTS`
6. **FTS**: Remove both nodes from FTS before data changes, re-index target after, all inside transaction

## Reused Patterns
| Pattern | Source |
|---------|--------|
| Triple reassignment w/ `defer_foreign_keys=ON` | `update_node_id()` in `_node_service.py` |
| Label merge (target-first) | `modifi()` in `_cli_nodo_crud.py` |
| Preview + confirm flow | `forigi` in `_cli_nodo_forigi.py` |
| FTS reindex inside transaction | `update_node_id()` / `update()` |

## Scope (files to modify)
- `_node_service.py` — `merge_nodes()` method
- `_cli_nodo_crud.py` or `_cli_nodo_kunfandi.py` (new) — CLI command
- `_cli_nodo.py` — register command
- `_preview.py` — optional preview helpers
- `AGENTS.md` — add documentation
- `tests/test_cli_nodo.py`, `tests/test_nodes.py`, `tests/test_triples.py` — tests
