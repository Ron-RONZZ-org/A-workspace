# Issue #43 — AmbiguousUUIDError Detail Dropped in forigi (May 2026)

## Problem
Two `AmbiguousUUIDError` catch sites discarded the exception detail:

1. `_cli_nodo.py:324` — `nodo forigi` caught without `as e`
2. `_cli_rubujo.py:118` — `_batch_resolve_trash_nodes` caught without `as e`

This violated AGENTS.md Rule #12 ("propagate to user with clear message").
Users saw only "ambigua prefikso" without the match count.

## Fix
Twofold approach:

1. **Error detail**: Both catch sites now capture `as e` and include `str(e)` in the error message.
2. **Prevention**: `nodo ls` and `rubujo ls` now automatically detect when 16-char prefixes collide and display the **full UUID** for those rows instead of truncating. Non-ambiguous entries still show compact 16-char prefixes.

**After fix:**
```
nodo ls
ID                                      Etikedo
──────────────────────────────────────────────────────
aa111111-1111-4111-8111-aaaaaaaaaaaa    NodoAlfa
aa111111-1111-4111-8111-bbbbbbbbbbbb    NodoBeta
```