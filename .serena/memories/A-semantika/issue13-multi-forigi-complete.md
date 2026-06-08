# Issue #13 — Multi-Identifier `forigi` — Complete (May 2026)

## What was done
All 3 A-semantika `forigi` commands now accept multiple positional identifiers:

| Command | Old signature | New signature |
|---------|---------------|---------------|
| `nodo forigi` | `uuid: str` | `uuids: list[str]` |
| `predikato forigi` | `predicate_id: str` | `predicate_ids: list[str]` |
| `predikat-grupo forigi` | `group_name: str` | `group_names: list[str]` |
| Root triple `forigi` | SPO args | **Unchanged** (different semantics) |

## Canonical Pattern (3-phase)
1. **Resolve** each identifier independently — per-item errors don't block others
2. **Batch preview** — Rich table of resolved items → single `confirm_action`
3. **Execute** — per-item delete with `"Deleted X of Y items"` summary

## Cross-Module Audit
- **A-agento `stilo forigi`**: Single UUID — filed issue A-agento#58
- **A-organizi `todo forigi`**: Accepts `list[str]` but resolves only first — filed bug A-organizi#24
- **A-workspace AGENTS.md**: `forigi` Contract expanded with full normative section

## Files Changed (A-semantika)
- `_cli_nodo.py` — nodo forigi rewrite
- `_cli_predikato.py` — predikato forigi rewrite
- `_cli_predikat_grupo.py` — predikat-grupo forigi rewrite
- `test_cli.py` — 3 new multi-forigi tests
- `test_edge_cases.py` — 7 new edge case tests
- `AGENTS.md` — issue #13 progress entry

## Key Decision
- **Batch confirmation** (not per-item) — user already expressed intent by passing N identifiers
- **Keep root triple `forigi` as SPO-based** — fundamentally different identifier model
