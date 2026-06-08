# --ligilo Debug: A-core must be editable install

## Problem
Running `agento generi --ligilo <URL>` gives:
```
--ligilo requires A-core version with http module
```

Even after `uv pip install -U A-core`, the issue persists.

## Root Cause
A-core was installed as a **static copy** (not editable) in the venv.
`uv pip install -U A-core` checks PyPI (no update needed), not the local
source. New files like `http.py` exist in the source tree at
`A-core/src/A/core/http.py` but are never deployed to `site-packages/`.

## How to detect
Check if A-core has a `.pth` file:
```bash
find <venv>/lib/python*/site-packages -name "*a_core*.pth"
```
If no `.pth`, it's a static install.

## Fix
```bash
uv pip install -e A-core --no-deps
```
This creates `_editable_impl_a_core.pth` pointing to `A-core/src/`.
Source-tree changes are live instantly.

## Prevention
The error message in `A-agento/src/A_agento/commands/knowledge.py` now
recommends `uv pip install -e A-core --no-deps` instead of
`uv pip install -U A-core`.
