# UUID-per-Triple Decision (May 2026)

## Question
"Should we add a UUID column to each semantic triplet to simplify forigi/modifi UX?"

## Answer: ❌ NO — keep compound PK

### Key Findings

**RDF Semantics:**
- Triple identity is content-based (SPO tuple), not artifact-based
- All major triple stores (Jena, RDFlib, Virtuoso) hide internal IDs from exports
- UUID would violate RDF standard by exposing artifact identity

**Performance:**
- `WITHOUT ROWID` compound PK clusters table by (subject, predicate, object, type)
- This is optimal for triple-pattern queries (dominant access pattern)
- UUID PK would require secondary index on SPO, degrading performance

**UX Impact (Issue #8 R3):**
- UUID doesn't actually solve "cumbersome deletion" better than search-then-select
- Both require searching first to find the triple
- UUID just changes final step from "pick row #" to "copy UUID" (no improvement)
- Search-then-select provides same UX with zero schema cost

**Migration Cost:**
- Full table rebuild (schemas incompatible)
- All indexes recreated
- All scripts using compound-key queries break
- Test fixtures need complete rewrite
- Zero offsetting benefit for our use case

### Approved Exceptions (per workspace AGENTS.md)
- Triples table uses compound PK instead of UUID PK
- Justified: RDF semantics + performance + no UUID benefit
- Already documented in A-semantika AGENTS.md

### Path Forward (Issue #8)
- **R1 (--jes flag):** ✅ Implement
- **R2 (help strings):** ✅ Implement
- **R3 (triple UX):** Use search-then-select instead of UUID
  - Make predicate/object optional in `forigi`/`modifi`
  - When omitted, show interactive picker
  - Keep SPO syntax for scripting (backward compatible)

### Related Issues
- A-workspace issue #8 (RFC: A-semantika)
- A-semantika issue #8 (CLI improvements)
- Comments: 
  - Architecture analysis: A-semantika#8#issuecomment-4524654024
  - Workspace update: A-workspace#8#issuecomment-4524654642

### Decision Date
May 23, 2026

### Reviewers
- @architect (approved)
- Robotika R (filed)
