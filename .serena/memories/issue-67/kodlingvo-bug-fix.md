## Bug Fix: `--kodlingvo` silently dropped in non-kodbloko branches

**Problem:** In `_cli_triples.py:aldoni()`, the `kodlingvo_val` variable was explicitly
set to `None` in the `elif katex is not None:`, `elif str_dosiero is not None:`, and
`elif object is not None:` branches. This meant that `--kodlingvo` passed without
`--kodbloko` was silently ignored — the subsequent `validate_type_flags()` call
received `kodlingvo=None` and couldn't catch the misconfiguration.

**Fix:** Changed all three branches to preserve the user-supplied `kodlingvo` value
instead of resetting it to `None`:
```python
# Before:
kodlingvo_val = None

# After:
kodlingvo_val = kodlingvo
```

Now `validate_type_flags()` properly catches `--kodlingvo` without `--kodbloko`
regardless of which object source branch is active.

**Tests:** New test `test_aldoni_kodlingvo_without_kodbloko_exits_error` in
`test_cli_type_flags.py`.
