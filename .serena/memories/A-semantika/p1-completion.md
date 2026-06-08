# A-semantika P1 Complete

## Key Lessons for Future Work

### SQLiteDB Path Handling
- `SQLiteDB.__init__` checks `isinstance(name_or_path, Path)` — a string path is treated as a database NAME, not a path
- Always pass `SQLiteDB(path_object)` not `SQLiteDB(str(path_object))`
- Bug: `get_db()` used `SQLiteDB(str(db_path))` causing DB to be created at `~/.local/share/A//absolute/tmp/path/semantika.db.db` instead of the intended tmp_path

### FTS5 External Content + SQLite ≥ 3.50
- Direct `DELETE FROM fts_table WHERE rowid = ?` causes "database disk image is malformed" on SQLite ≥ 3.50 when FTS uses `content=external_table`
- Fix: use FTS5 `'delete'` command: `INSERT INTO fts_table(fts_table, rowid) VALUES('delete', ?)`
- Implemented as `NodeService._remove_from_fts()` override

### SQLiteDB.execute() for DML
- `SQLiteDB.execute()` returns `list[dict]` — for DELETE, `fetchall()` returns `[]`, so `len([])` is 0
- Use `with self.db.transaction() as conn: cursor = conn.execute(sql, params); return cursor.rowcount` to get actual affected row count

### CRUDService.delete() behavior
- `CRUDService.delete()` does NOT raise on nonexistent UUID — it silently returns
- Subclasses that need error behavior must override or check before calling

### FTS5 External Content Shadow Tables
- When using `content=table_name, content_rowid=rowid`, FTS5 does NOT create a `_content` shadow table
- Only creates: `{fts_name}`, `{fts_name}_data`, `{fts_name}_idx`, `{fts_name}_docsize`, `{fts_name}_config`
- Tests expecting `_content` tables need to be updated

### Typer/Click `no_args_is_help` exit code
- Click 8.x exits with code 2 (not 0) for `no_args_is_help=True` — it's treated as `UsageError` internally
- Tests should accept both 0 and 2: `assert result.exit_code in (0, 2)`

## Branch Strategy
- Worked on `feat/p1-core-triple-store` branch
- Merged into `main` and pushed
- Issue comment posted to workspace issue #8
