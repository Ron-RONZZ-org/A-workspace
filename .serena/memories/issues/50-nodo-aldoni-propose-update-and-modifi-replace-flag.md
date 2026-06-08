# Issue #50: nodo aldoni duplicate → propose update; nodo modifi → add -r flag

## What
Two related enhancements for `nodo` CLI:

### 1. `nodo aldoni` on duplicate
Per workspace AGENTS.md, `aldoni` must "propose to modifi if similar entry exists". Currently shows error + instructions. Should show diff and ask to update.

### 2. `nodo modifi -r`/`--anstatauxigi`
`predikato modifi` already has merge-by-default + `-r` for replace. `nodo modifi` needs the same `-r` flag.

## Implementation scope
- `_cli_nodo.py` — aldoni() duplicate flow + modifi() `-r` flag
- `_preview.py` — confirm_node_update() or adapt existing

No new files needed.
