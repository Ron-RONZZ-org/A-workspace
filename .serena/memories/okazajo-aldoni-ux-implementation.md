# okazajo aldoni UX Improvement (#30)

## What Changed
Three UX enhancements for `okazajo aldoni`:

### 1. `-k/--kalendaro` Optional
- 0 calendars → error
- 1 calendar → auto-select with `info("Uzas kalendaron #...")`
- Multiple → interactive picker via `select_candidate()`

### 2. Date+Time Split
- `--dato YYYYMMDD` — event date (required)
- `--dato-gis YYYYMMDD` — multi-day end date (optional)
- `--komenco HHMM` — start time, defaults 0000
- `--fino HHMM` — end time, defaults 2359 (or 0030 with `-R`)
- Cross-midnight: if `fino < komenco`, date advances by 1 day
- Same split applied to `okazajo modifi`
- `_combine_date_time(dato, komenco, fino, dato_gis)` in `okazajo.py`

### 3. RRULE Validation via `okazajo_rrule.py`
- `expand_shorthand()` — converts `daily`/`weekly`/`monthly`/`yearly`/`weekdays`/`weekends` to `FREQ=*`
- `validate_rrule()` — RFC 5545 validation: required FREQ, allowed params per FREQ type, BYDAY values, UNTIL format, COUNT/INTERVAL ranges, BYMONTH values, WKST values
- `normalize_rrule()` — combos: strip → expand shorthand → validate
- Invalid values rejected with clear Esperanto error messages

## Files
- `src/A_organizi/cli/okazajo.py` — 340 lines: aldoni + helpers + display + resolve
- `src/A_organizi/cli/okazajo_crud.py` — 371 lines: ls, vidi, serci, modifi, forigi, amase_forigi
- `src/A_organizi/cli/okazajo_rrule.py` — 235 lines: RRULE validator + shorthand
- `tests/test_rrule.py` — 31 tests for OKazajoRrule module
- `tests/test_kalendaro.py` — extended with 13 CLI integration tests

## Design Decisions
- Date+time merge in CLI layer, not service. Service still receives ISO 8601.
- RRULE validation local to okazajo (not A-core) — only calendar domain needs it.
- modifi with time-only flags (no `--dato`) fetches event's current date from DB.
- Cross-midnight uses string comparison (`fino < komenco`), not datetime arithmetic.
