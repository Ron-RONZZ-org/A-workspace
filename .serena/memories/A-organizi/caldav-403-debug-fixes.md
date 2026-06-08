# CalDAV 403 Forbidden Debug and Fixes

## Root Cause Analysis (2026-06-03)

### Issue
`okazajo reprovi` job `59c39cba6cdc` (push for event `e8b5e277`) failed with:
```
CalDAV PUT failed: Forbidden — check credentials or calendar permissions
```

### Investigation
1. Calendar: `45e3adea` → URL: `https://leo.it.tab.digital/remote.php/dav/calendars/ron@ronzz.org/mon-agenda/`
2. Password exists in keyring (stored at calendar creation)
3. All HTTP requests to the server return **403 with Nextcloud error code 1010** (invalid auth token)
4. Server is behind Cloudflare (IP: `104.21.3.117`)

### Determination
**Primary cause: User credential problem** — The Nextcloud app password has been revoked/expired. Nextcloud error code 1010 specifically indicates an invalid authentication token. The user needs to regenerate the app password in Nextcloud Security settings and update it via:
```bash
A organizi kalendaro modifi 45e3adea --pasvorto <new-app-password>
```

### Code Issues Found & Fixed

#### 1. Server response body discarded in error messages
- `http_fetch_text()` returns `(status, body_text)` but callers used `_` for body
- Response body contains server-specific error codes (e.g., Nextcloud 1010)
- **Fix**: All HTTP error paths now include the server response body snippet

#### 2. No password validation before push
- `process_sync_job()` called `get_password()` without checking for None
- If keyring is missing/unavailable, None is passed as password → credentials become `"username:None"` → always fails
- **Fix**: Added `if not password: raise ValueError(...)` with actionable suggestion

#### 3. Generic error messages without actionable suggestions
- 403 description updated: mentions Nextcloud app password may be revoked
- PUT URL is now included in CalDAV PUT errors for debugging
- `_http_error` renamed to `http_error` and exported

#### 4. `kalendaro modifi` also discarded response body
- Same pattern in `kalendaro.py:152` — now captures body and uses `http_error()`

### Real Root Cause (2026-06-03 correction)

The earlier analysis was WRONG. The credentials were never the problem!

**Real root cause: Missing User-Agent header**

`http_fetch_text()` used Python's default `urllib` User-Agent (`Python-urllib/3.x`).
The CalDAV server (Nextcloud behind Cloudflare) has a **Cloudflare WAF rule** that blocks
requests with the default Python `urllib` User-Agent.

- Without User-Agent → **403** with Cloudflare "Access denied" HTML page
- With `User-Agent: A-organizi/1.0` → **201 Created** — push succeeds

The password/username were valid all along.

## Fix Summary

### Root Cause Fix
- Added `User-Agent: A-organizi/1.0` to default headers in `http_fetch_text()`
- Improved Accept header to prioritize `application/xml, text/calendar` for CalDAV

### Secondary Fixes (from earlier round)
- Clear `eraro` field on success in `process_sync_job()` (was leaving stale errors)
- Server response body included in HTTP error messages
- Password validation before push
- PUT URL included in CalDAV error messages
- 403 description mentions Nextcloud app passwords
- `http_error()` exported from sync.py

## Files Changed
- `src/A_organizi/utils/sync.py` — Multiple error handling improvements
- `src/A_organizi/cli/kalendaro.py` — Better error in modifi command

### All 290 tests pass.
