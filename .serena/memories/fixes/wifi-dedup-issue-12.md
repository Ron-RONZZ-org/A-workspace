# Wi-Fi dedup and AP count column (Issue #12)

## Problem
`A sistemo wifi ls` showed every BSSID from nmcli as a separate row — same SSID repeated at different signal strengths (e.g., 8 rows of "eduroam").

## Fix
Added `_deduplicate_networks()` pure function in `src/A_sistemo/services/wifi_service.py`:
- Groups by SSID, keeps the entry with **highest signal**
- Active flag is OR'd across all duplicates for the same SSID
- Empty-SSID entries (hidden networks) pass through unchanged
- Sets `ap_count` field on the result to show total BSSIDs

Added `AP-oj`/APs/PA column to the Rich table in `cli/wifi.py`.

## Tests
7 new tests in `tests/test_wifi_service.py` covering: best signal, active flag propagation, tie-breaking, hidden networks, AP count aggregation, empty input.

## Branch
`fix/wifi-dedup-ap-count-#12` → merged to main as commit `375d7f8`.
