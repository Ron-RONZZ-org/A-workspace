# SQLiteDB.execute() does NOT auto-commit writes

## The Bug

`SQLiteDB.execute()` opens a connection, runs the SQL, and closes the connection **without committing**.

For `INSERT`, `UPDATE`, `DELETE` (DML), the operation is silently rolled back on connection close because Python 3.12+ `sqlite3` does not autocommit DML by default.

`CREATE TABLE`, `CREATE INDEX` (DDL) DO auto-commit, so schema creation works fine — only data writes are lost.

## Wrong vs Correct

```python
# WRONG — insert is rolled back
db.execute("INSERT INTO table (col) VALUES (?)", ("val",))

# CORRECT — insert is committed
with db.transaction() as conn:
    conn.execute("INSERT INTO table (col) VALUES (?)", ("val",))
```

## Why existing code works

`CRUDService.create()` / `.update()` / `.delete()` all use `self.db.transaction()` internally — they commit correctly. This bug only affects raw `db.execute()` calls for writes.

`SELECT` is unaffected since there's nothing to commit.

## Discovery

Found during A-organizi issue #7 implementation (`utils/ics.py`). The `insert_ics_events()` function used `db.execute()` for INSERTs, and subsequent reads returned zero rows. Fixed by wrapping in `with db.transaction()`.

## Affected code to audit

Search for patterns where `db.execute()` is called with INSERT/UPDATE/DELETE not inside a `with db.transaction()` block.
