# Issue #30: okazajo aldoni UX improvements

**Status:** Filed, awaiting implementation  
**Link:** https://github.com/Ron-RONZZ-org/A-organizi/issues/30

## Proposal Summary

Three UX improvements for `okazajo aldoni`:

1. **`-k/--kalendaro` optional** — auto-infer if 1 calendar, interactive picker if >1
2. **Date+time split** — `--dato` (date) + `--komenco`/`--fino` (time HHMM), replacing `--komenco`/`--fino` as dates
3. **RRULE validation** — `--ripeto` accepts only valid CALDAV RRULE strings

## Architect Findings

- **No architectural changes required** — all CLI-layer only
- Date+time merge in CLI layer before passing to `EventService.create()`
- Multi-day events: auto-advance when `fino < komenco`; add `--dato-gis` for explicit multi-day
- Apply same split to `modifi` for API consistency
- New file: `okazajo_rrule.py` for RRULE validation + shorthand expansion
- Remove dead `komenco`/`fino` params from `_build_overrides` in `okazajo_retposto.py`
- Existing DB data unaffected (no schema change)
