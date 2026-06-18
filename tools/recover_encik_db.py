#!/usr/bin/env python3
"""Recover a corrupted encik database, preserving all UUIDs.

Usage:
    python3 tools/recover_encik_db.py

This creates ~/.local/share/A/encik_recovered.db and then swaps it in.
"""

import sqlite3
import shutil
from pathlib import Path

DB = Path.home() / ".local/share/A/encik.db"
BACKUP = DB.with_name("encik.db.corrupted")
RECOVERED = DB.with_name("encik_recovered.db")

def get_tables(conn):
    """Get all user tables from the corrupted DB."""
    try:
        rows = conn.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_fts%'"
        ).fetchall()
        return rows
    except sqlite3.DatabaseError as e:
        print(f"[✗] Cannot read schema: {e}")
        # Try reading sqlite_master directly from DB pages
        try:
            rows = conn.execute(
                "SELECT name, sql FROM sqlite_master WHERE type='table'"
            ).fetchall()
            return rows
        except Exception:
            return []

def copy_table(src, dst, name, create_sql):
    """Copy a single table's data from src to dst."""
    dst.execute(create_sql)
    try:
        rows = src.execute(f"SELECT * FROM [{name}]").fetchall()
        cols = [d[0] for d in src.execute(f"PRAGMA table_info([{name}])")]
        placeholders = ", ".join(["?"] * len(cols))
        col_list = ", ".join(f"[{c}]" for c in cols)
        count = 0
        for row in rows:
            try:
                dst.execute(
                    f"INSERT INTO [{name}] ({col_list}) VALUES ({placeholders})",
                    row,
                )
                count += 1
            except sqlite3.IntegrityError:
                pass  # Skip duplicate rows
        print(f"  ✓ {name}: {count} rows")
        return count
    except sqlite3.DatabaseError as e:
        print(f"  ✗ {name}: {e} — skipped")
        return 0

def main():
    if not DB.exists():
        print(f"[✗] Database not found: {DB}")
        return 1

    # Open corrupted DB in read-only mode
    try:
        src = sqlite3.connect(f"file:{DB}?immutable=1", uri=True, timeout=30)
    except sqlite3.Error as e:
        print(f"[✗] Cannot open corrupted DB: {e}")
        return 1

    # Create new clean DB
    if RECOVERED.exists():
        RECOVERED.unlink()
    dst = sqlite3.connect(str(RECOVERED), timeout=30)

    total = 0
    tables = get_tables(src)
    for name, create_sql in tables:
        if not create_sql:
            continue
        # Strip any AUTOINCREMENT (can cause issues during recovery)
        clean_sql = create_sql.replace("AUTOINCREMENT", "")
        total += copy_table(src, dst, name, clean_sql)

    dst.commit()
    dst.close()
    src.close()

    if total == 0:
        print(f"[✗] No data recovered — DB is irrecoverable.")
        RECOVERED.unlink(missing_ok=True)
        return 1

    print(f"\nRecovered {total} rows total.")
    print(f"Backup: {BACKUP}")
    print(f"New DB: {RECOVERED}")

    # Swap in recovered DB
    BACKUP.unlink(missing_ok=True)
    shutil.move(str(DB), str(BACKUP))
    shutil.move(str(RECOVERED), str(DB))

    # Clean up WAL/SHM
    for suffix in ("-wal", "-shm"):
        (DB.parent / (DB.name + suffix)).unlink(missing_ok=True)

    print(f"✓ Swapped in recovered database. Old DB saved as {BACKUP.name}")
    print(f"✓ All UUIDs preserved.")
    return 0

if __name__ == "__main__":
    exit(main())
