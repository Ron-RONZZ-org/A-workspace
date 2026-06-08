# Single Colon ` : ` as Difino-Uzo Separator

## Decision (2026-05-25)

**Approved**: Accept ` : ` (space-colon-space) as a difino-uzo separator in `split_difino_uzo()`.

## Rationale

- Matches natural dictionary format (Aspect: `definition : usage example`)
- ` : ` pattern avoids false positives on `"14:30"`, `"3:1"`, emoticons, labels
- Zero impact on existing stored data (parsing is input-time only)
- Existing test `test_difino_with_colon_no_uzo` is unaffected (uses `"just: text"` without leading space)
- Explicit `::` remains highest priority separator

## Implementation

Insert after `::` check, before `:{...}` check in `split_difino_uzo()`:
```python
if " : " in text:
    left, right = text.split(" : ", 1)
    return left.strip(), right.strip()
```

## Issue

https://github.com/Ron-RONZZ-org/A-vorto/issues/37
