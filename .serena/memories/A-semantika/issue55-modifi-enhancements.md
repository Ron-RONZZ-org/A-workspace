# Issue #55 — Three Modifi UX/Correctness Fixes

## Changes

### Item 1: `predikato modifi -ni` rename preview before confirmation
**File:** `_cli_predikato.py`
When running `predikato modifi old -ni new`, the rename line "Predikato renomita: old → new" now appears **before** the confirmation prompt, not after. This lets users preview what will change before confirming.

### Item 2: String literal footnote no longer duplicates table row
**File:** `_preview.py` (`build_triple_preview_table`)
The `→ literal, lang: en` footnote removed the `lang:` portion because the table's second row already shows `literal, lingvo: en`.

### Item 3: `modifi -np` preserves old literal value and datatype
**File:** `_cli_modify.py`
When the user runs `modifi SUBJ PRED OBJ -np NEWPRED` (changing predicate only, no `-no` or type flags), the code now inherits the old object value, type, lang, AND datatype directly — skipping URI resolution entirely. 

**Critical detail:** `old_object_datatype` is now captured from the existing triple (in both interactive and direct modes) and preserved. Previously `new_datatype = None` would silently drop `xsd:integer` → NULL for typed literals.

## Key pattern for future `modifi` changes:
```python
has_new_object = new_object is not None
has_type_flags = any([str_, int_, float_, bool_])

if not has_new_object and not has_type_flags:
    # Inherit old values — user only changing subject/predicate
    new_obj_value = old_object_value
    new_obj_lang = old_object_lang
    new_object_type = old_object_type
    new_datatype = old_object_datatype
else:
    # Resolve new object with type flags
    ...
```

## Tests
- `test_cli_rename_preview_before_confirm` (`test_predikato_id_rename.py`)
- `test_modifi_new_predicate_only_with_literal` (`test_triple_modifi_edge.py`)
- `test_modifi_new_predicate_only_with_typed_literal_preserves_datatype` (`test_triple_modifi_edge.py`)

## PR
https://github.com/Ron-RONZZ-org/A-semantika/pull/56
