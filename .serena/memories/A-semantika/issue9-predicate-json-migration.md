# Issue #9 — Predicate JSON Migration + UX Cleanup

## Summary

Implemented the architectural decision from [comment 4524817416](https://github.com/Ron-RONZZ-org/A-semantika/issues/9#issuecomment-4524817416):

### Changes

1. **Schema** — `predicates` table: replaced `label_eo`/`label_en`/`priskribo` flat columns with `etikedoj`/`priskriboj` JSON columns

2. **PredicateService** — custom `create()`/`update()` with JSON serialization; `search()` uses LIKE on JSON text fields

3. **CLI (`_cli_predikato.py`)**:
   - `aldoni()`: removed `--en` flag, removed `--fonto` flag, `-p` changed from `Optional[str]` to `Optional[list[str]]` with `LANGCODE::TEKSTO` format
   - `modifi()`: removed `--label-eo`/`--label-en`, added `-e`/`--etikedo` (repeatable), `-r`/`--anstatauxigi` for replace semantics, `-p` now repeatable LANGCODE::TEKSTO
   - `vidi()`: shows all languages from JSON etikedoj/priskriboj
   - `ls()`: single label column (eo/en fallback from JSON)
   - `serci()`: unchanged (delegates to `pred_svc.search()`)

4. **Wikidata helper** — `fetch_wikidata_details()` returns `etikedoj`/`priskriboj` dicts instead of flat `label_eo`/`label_en`/`priskribo`

5. **`_ensure_predicate()`** — creates with `{"eo": label_eo}` dict

6. **`resolve_predicate_label()`** — reads from `etikedoj` JSON

7. **`list_members()`** — SQL join updated, display reads from JSON

### Test count
155 tests all passing (up from 155 before — no new tests needed since existing tests were updated for the new format).

### Commits
- `035a4f5` — feat: predicate JSON migration + UX cleanup (issue #9)
