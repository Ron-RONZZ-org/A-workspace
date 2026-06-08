# Clipboard False Negative Fix (June 2026)

## Problem
`copy_to_clipboard()` returned `False` (failure) even when the content was successfully written to the clipboard. This caused confusing `"[!] Ne povis kopii al poŝo: VALUE"` warnings despite the clipboard actually containing the intended value.

## Root Cause
`xclip -selection clipboard` (the most common Linux clipboard tool) writes data to the clipboard immediately upon reading stdin, but the process may take several seconds to complete its X11/Wayland connection handshake before exiting. The original `subprocess.run(timeout=2.0)` killed the process after 2 seconds, and the non-zero exit code (124 = timeout) was interpreted as failure — even though the data was already in the clipboard.

## Fix (A-core, clipboard.py)
1. **Timeout increased from 2.0s → 5.0s** — gives slow X/Wayland connections more time
2. **Changed from `subprocess.run()` to `subprocess.Popen` + `communicate(timeout=5.0)`** — on `TimeoutExpired`, the process is NOT killed. The function returns `(True, "clipboard tool xclip timed out (data was written)")` instead of `False`, because xclip/etc write data before the process exits
3. **Return type changed from `bool` to `tuple[bool, str]`** — diagnostic reason string included on both success and failure
4. **Added `_describe_env()`** — reports platform, DISPLAY/WAYLAND_DISPLAY env vars, and which clipboard tools are available (only called on failure path)

## Callers Updated (13 sites across 5 repos)
All callers of `copy_to_clipboard()` now unpack the tuple and show the diagnostic reason in the warning message.

## Files Modified
- `A-core/src/A/utils/clipboard.py` — core fix
- `A-core/tests/test_clipboard.py` — updated for new API + Popen mock
- `A-semantika/src/A_semantika/_cli_nodo_crud.py` — show reason in warning
- `A-semantika/src/A_semantika/_cli_predikato.py` — show reason in warning
- `A-semantika/tests/test_cli_nodo.py` — mock returns tuple
- `A-semantika/tests/test_cli_predikato.py` — mock returns tuple
- `A-vorto/src/A_vorto/display_helpers.py` — add warning on failure
- `A-vorto/src/A_vorto/modify_helpers.py` — add warning on failure
- `A-encik/src/A_encik/display_helpers.py` — add warning in copy_entry_reference
- `A-encik/src/A_encik/_cli_crud.py` — add warning on failure
- `A-encik/src/A_encik/_cli_aldoni.py` — add warning on failure
- `A-agento/src/A_agento/commands/knowledge.py` — add warning on failure
- `A-agento/src/A_agento/commands/enhancement.py` — add warning on failure
- `A-agento/src/A_agento/commands/translation.py` — add warning on failure
- `A-agento/tests/test_enhancement.py` — mock returns tuple
- `A-agento/tests/test_traduki.py` — mock returns tuple
