# Bug Fix: String literal value on wrong preview row

## Root Cause
Issue #3 (literal preview row swap) only fixed the **typed literal** branch of `build_triple_preview_table()` in `_preview.py`. The **string literal** branch was overlooked.

## The Bug
In `_preview.py:173-175`, the string literal `else` branch had:
- Row 1: empty string `""` for object column 
- Row 2: the quoted `"value"` 

This meant the actual string value appeared on Row 2 (raw IDs row) instead of Row 1 (labels row).

## The Fix
Swapped the two `table.add_row()` calls in the string literal branch. Now:
- Row 1: `subj_label, pred_label, quoted_val` (value on labels row)
- Row 2: `subj_id, predicate_id, ""` (empty on raw IDs row)

Consistent with typed literal pattern where value is on Row 1 and type annotation on Row 2.

## Systematic Review
All 28 `table.add_row()` calls across 6 source files were checked. Only `_preview.py:173-175` was affected. `confirm_node_with_arcs()` already had correct ordering (value on Row 1).

## Test Updated
`test_build_string_literal_preview` now verifies row ordering: asserts the quoted value appears before the raw subject ID in the rendered output.
