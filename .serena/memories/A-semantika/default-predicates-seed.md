# Default Predicates Seed (Issue #18)

## Decision
Approved by architect. Seed 4 default RDF/OWL predicates at `init_db()` time in `data/storage.py`:

| Predicate ID | EO Label | Source |
|---|---|---|
| rdf:type | tipo | rdf |
| rdfs:subClassOf | subklaso | rdfs |
| owl:disjointWith | disjunkcio | owl |
| owl:inverseOf | inverso | owl |

**Excluded:** `rdfs:label`, `rdfs:comment` — labels/descriptions are stored as first-class columns (`etikedoj`/`difinoj`) on the `nodes` table, not as triple arcs. Adding them as predicates would imply a nonexistent usage pattern.


## Key Constraints
- Seed AFTER migrations (migrations drop predicates table)
- `INSERT OR IGNORE` for idempotency
- Keep `_ensure_predicate()` in `_cli_nodo.py` as backward-compat safety net
- Python constant (not data file) — tiny dataset

## Issue
https://github.com/Ron-RONZZ-org/A-semantika/issues/18
