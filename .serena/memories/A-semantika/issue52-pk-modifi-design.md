# Issue #52: Allow modifying node_id/predicate_id in modifi commands

## Status
- Issue filed: https://github.com/Ron-RONZZ-org/A-semantika/issues/52
- Implementation plan: https://github.com/Ron-RONZZ-org/A-semantika/issues/52#issuecomment-4545100807
- Architect: ✅ APPROVED (manual SQL cascade in service layer)
- Implementation: ⏳ Not started

## Key Architectural Decision
- **Manual SQL cascade** in service layer (NOT schema-level `ON UPDATE CASCADE`)
- Rationale: avoids migration complexity, bypasses `object_node_uuid` GENERATED FK blocker
- Follows existing patterns from `_cli_nodo_forigi.py` and `_cli_modify.py`

## Implementation Summary
- CLI flags: `--nova-id` / `-ni` on both `nodo modifi` and `predikato modifi`
- Service updates: extend `NodeService.update()` and `PredicateService.update()` to handle PK changes
- Cascade: UPDATE triples + predicate_group_members in same transaction
- FTS: re-index under new ID
- No schema changes, no new files

## Flag naming
Following `--nova-subjekto`/`--nova-predikato`/`--nova-objekto` convention from root `modifi` command.
`--nova-id` / `-ni` since each subcommand is already scoped.
