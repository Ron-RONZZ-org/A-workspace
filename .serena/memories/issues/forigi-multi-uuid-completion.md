# Cross-Module `forigi` Multi-UUID Implementation

## Completed (May 23, 2026)

### A-semantika #13 — `forigi` multi-identifier support (3 commands)
- **Status**: ✅ Merged to `main`
- **Commands updated**: `nodo forigi`, `predikato forigi`, `predikat-grupo forigi`
- **Pattern**: 3-phase (resolve → batch preview → per-item delete)
- **Tests**: 206 passing

### A-agento #58 — `stilo forigi` multiple UUIDs
- **Status**: ✅ Merged to `main` (#59)
- **Commands updated**: `stilo forigi`, `stilo forigu` (deprecated alias)
- **Pattern**: Direct iteration, no confirmation (matches existing `delete_style_sample` behavior)
- **Tests**: Single, multi-UUID, deprecated alias

### A-organizi #24 — `todo forigi` per-item resolution
- **Status**: ✅ Merged to `main` (#25)
- **Commands updated**: `todo forigi`
- **Pattern**: Per-item `resolve_reference()` + per-item `typer.prompt` confirmation + summary report
- **Tests**: Single confirmed, single cancelled, multi confirmed, mixed confirm/cancel, nonexistent ref

### A-workspace AGENTS.md
- **Expanded `forigi` Contract**: Added normative section with canonical implementation pattern, required results, and acceptance criteria.

## Design Decisions
1. **Batch confirm vs per-item**: A-organizi uses per-item prompts (existing UX preserved); A-agento deletes silently (no confirmation in original).
2. **UUID first column in `ls`**: All list commands display UUID as first column for quick copy-paste into `forigi`.
3. **Error handling**: Partial success reports deleted/total count; not-found refs reported without aborting.
4. **No `rubujo` (trash) for A-agento**: Stilo samples use hard delete; `rubujo` group only for modules with soft-delete.
