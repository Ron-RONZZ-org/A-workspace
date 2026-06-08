# Issue #10 — EO Locale Compliance — Complete

## Summary
Systematic Esperanto locale review across all A-semantika CLI commands. All user-facing argument metavars, option flags, and output strings now use Esperanto per workspace AGENTS.md.

## Key Decision
- Only **user-facing** CLI surface changed (argument metavars, option flags, output text)
- Python parameter names left in English (internal code)
- `--str`/`--int`/`--float`/`--bool` kept as-is (universal data-type identifiers)
- `--limit`/`--output`/`--base-uri`/`file`/`query`/`uuid` kept as-is (universal technical terms)

## Files Changed/Created

### New files
- `_cli_query.py` — extracted from `_cli_triples.py`: `serci`, `vidi`, `eksporti`, `resolve_deprecated()`
- `_cli_modify.py` — extracted from `_cli_triples.py`: `modifi` command
- `_cli_helpers.py` — extracted from `_cli_triples.py`: `pick_triple()`, `count_type_flags()`, `validate_type_flags()`

### Modified files
- `_cli_triples.py` — now only `aldoni` and `forigi`; metavar fixes; help string fix
- `_cli_predikato.py` — `tr_multi()` for table headers (`ls`) and info labels (`vidi`)
- `_cli_predikat_grupo.py` — `tr_multi()` for Grupo/UUID info labels
- `tests/test_cli.py` — updated 4 flag refs + 3 new backward-compat tests
- `cli.py` — updated imports for new file structure

## Option Flag Renames (all with backward-compat hidden aliases)

| Command | Old Flag | New Flag | Short |
|---------|----------|----------|-------|
| serci | --subject | --subjekto | -s |
| serci | --predicate | --predikato | -p |
| serci | --object | --objekto | -o |
| modifi | --new-subject | --nova-subjekto | -ns |
| modifi | --new-predicate | --nova-predikato | -np |
| modifi | --new-object | --nova-objekto | -no |

## Deprecation Pattern
```python
def resolve_deprecated(new_val, old_val, old_name, new_name):
    """Resolve a CLI option renamed from old_name to new_name.
    Warns if old flag used, errors if both used.
    """
```

## Related
- PR: https://github.com/Ron-RONZZ-org/A-semantika/pull/11
- Issue: https://github.com/Ron-RONZZ-org/A-semantika/issues/10
