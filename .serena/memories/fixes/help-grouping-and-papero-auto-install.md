# Fixes: A -h grouping & A-papero auto-install

## Issue 1: A-core — `A -h` should organise commands by module

**Root cause**: `LazyPluginGroup` (A-core/src/A/core/plugin_loader.py) overrode `list_commands()` to merge built-in commands with plugin names, but Click's default `format_commands()` rendered them all under a single "Commands:" section.

**Fix**: Added `format_commands()` override to `LazyPluginGroup` that separates commands into two sections:
- "Built-in Commands" (uzanto, modulo, migri, repl, list)
- "Installed Modules" (tempo, vorto, encik, medio, etc.)

**Commit**: A-core `def6f7c` on `fix/eo-locale-conformity` branch

## Issue 2: A-papero — auto-install missing optional deps

**Root cause**: `_check_dependencies()` in `service.py` and `_check_fitz()`/`_check_weasyprint()` in `formats/pdf.py` used bare `try: import fitz` / `try: import weasyprint` blocks that raised errors with install instructions instead of using `A.utils.deps.ensure_dependency()` for interactive auto-install.

**Fix**: Replaced all four locations with `ensure_dependency("fitz", "PyMuPDF")` and `ensure_dependency("weasyprint", "weasyprint")`. Falls through to original error message if user declines.

**Commit**: A-papero `17d8bc1` on `main` branch

## Systematic review findings (additional gaps)

The systematic review found the following gaps where auto-install is not used:

| Module | File | Gap | Priority |
|--------|------|-----|----------|
| A-organizi | `utils/sync.py:11-14` | Silent keyring degradation; `password()` raises RuntimeError at line 373 | MED |
| A-organizi | `data/migrate_from_autish.py:270-273` | Silent keyring fallback in migration | LOW |
| A-core | `core/markdown_parser.py:43-54` | Pygments silently falls back on import error (hard dep) | LOW |
