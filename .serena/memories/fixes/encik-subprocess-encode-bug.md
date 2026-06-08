# Bug: subprocess.run() double-encode (fixed May 2026)

## Symptom
`encik serci -sk usono` → `[✗] bytes object has no attribute encode`

## Root Cause
`A-core/src/A/utils/subprocess.py:run()` does `input.encode()` to convert str→bytes,
then passes `text=True` to `subprocess.run`. With `text=True`, subprocess expects
str input and tries to `.encode()` again on the already-bytes value.

## Fix
Removed manual `.encode()` — let `text=True` handle encoding:
```python
# Before: input=input.encode() if input else None,
# After:  input=input if input else None,
```

## Affected
All clipboard operations in all A-modules (copy_to_clipboard → run)
