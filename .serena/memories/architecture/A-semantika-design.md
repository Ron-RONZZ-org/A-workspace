# A-semantika Design Decision (2026-05-22)

## Status
RFC filed at https://github.com/Ron-RONZZ-org/A-workspace/issues/8
Architecture review completed — APPROVED with revisions.

## Key Decisions
1. **Clean start** — do NOT clone A-encik. Start from minimal template (A-agento/A-tempo).
2. **Multi-table DB** — 5 tables (nodes, predicates, predicate_groups, predicate_group_members, triples)
3. **TripleService** — custom service for triple CRUD (not CRUDService-compatible)
4. **3-phase approach** — P1: core store, P2: Wikidata, P3: OWL/RDFS
5. **URI + literal objects** — `--tipo uri|literal` flag on triple aldoni
6. **Turtle export in Phase 1** — essential for interoperability
7. **A-encik deprecation deferred** — to be evaluated when A-semantika is stable
8. **A-core prerequisite** — extract Wikidata client from A-encik to A.core.wikidata (separate issue)
