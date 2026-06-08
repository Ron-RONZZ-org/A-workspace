# `selo-funkcio` Architecture Design

## Decision Record

### Q1: Separate DB (`bash_functions.db`)
- **Not** same DB as aliases — zero data relationship, different generated files, different sourcing order
- Separates lifecycle, avoids naming confusion (`bash_aliases.db` containing a `functions` table)
- No lock contention between two SQLiteDB instances

### Q2: Function name via regex extraction
- Regex: `^\s*(?:function\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:\(\))?\s*\{`
- Validates at `aldoni` time (must find a name, must be unique)
- Optional `bash -n` syntax check subprocess

### Q3: Generated file format
- `~/.A_bash_functions` with `#!/bin/bash` header + per-function metadata comments + body
- Normalize to `name() {` on output regardless of input style
- Same RO (0444) convention as `.A_bash_alias`
- Sourced in `.bashrc` AFTER `.A_bash_alias`

### Q4: Function sourcing risks
- Validate no top-level executable code (only function definitions)
- Run `bash -n` validation at add time
- Acceptable risk: function definitions at shell startup are standard practice

### Q5: File-only for v1
- Inline multiline is painful (heredocs, escaping)
- Add `--body` or `--name` CLI flags in v2 if users request it

## Schema
```sql
CREATE TABLE IF NOT EXISTS bash_functions (
    uid INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    body TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT
);
```

## Files to create
- `src/A_sistemo/cli/bash_function.py` (~200 lines)
- `src/A_sistemo/services/bash_function_db.py` (~250 lines)
- `tests/test_bash_function_db.py` (~120 lines)

## Files to modify
- `src/A_sistemo/cli/sistemo.py` (+1 line to register Typer app)

## CRUD pattern
Follow `BashAliasDB` pattern (dataclass + manual service class), do NOT use `CRUDService` from A-core (overkill for this use case).
