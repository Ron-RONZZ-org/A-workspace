#!/usr/bin/env python3
"""Brute-force recovery of encik DB — scans raw file for entries.

Preserves all UUIDs. Outputs a clean SQLite DB.
"""

import json
import re
import sqlite3
from pathlib import Path

DB = Path.home() / "/.local/share/A/encik.db"
NEW = DB.with_name("encik_recovered.db")
BAK = DB.with_name("encik.db.bak3")

# Known encik columns in order
COLUMNS = [
    "uuid", "titolo", "difinio", "terminologio", "terminologio_search",
    "difinoj", "enhavo", "superklaso", "ligilo", "fonto", "citajo",
    "datumo", "semantika", "ligiloj", "kreita_je", "modifita_je",
]

# Patterns for fields
JSON_FIELDS = {"terminologio", "difinoj", "superklaso", "ligilo",
               "fonto", "citajo", "datumo", "semantika", "ligiloj"}
STR_FIELDS = {"uuid", "difinio", "enhavo", "kreita_je", "modifita_je",
              "terminologio_search"}


def find_text_blocks(data: bytes, min_size: int = 8) -> list[bytes]:
    """Find printable text blocks in binary data."""
    blocks = []
    current = bytearray()
    for b in data:
        if 32 <= b <= 126 or b in (10, 13, 9):  # printable + newline + tab
            current.append(b)
        else:
            if len(current) >= min_size:
                blocks.append(bytes(current))
            current = bytearray()
    if len(current) >= min_size:
        blocks.append(bytes(current))
    return blocks


def scan_entries(data: bytes) -> list[dict]:
    """Scan raw data for encik entries by finding terminologio patterns."""
    entries = []
    # Find blocks containing terminologio JSON
    text_blocks = find_text_blocks(data)
    uuid_pattern = re.compile(
        rb"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I
    )

    for block in text_blocks:
        text = block.decode("utf-8", errors="replace")
        if '"terminologio"' not in text and "'terminologio'" not in text:
            continue

        # Try to parse as JSON
        try:
            entry = json.loads(text)
            if isinstance(entry, dict) and "uuid" in entry and "terminologio" in entry:
                entries.append(entry)
                continue
        except (json.JSONDecodeError, ValueError):
            pass

        # Try to find JSON-like object boundaries
        for match in re.finditer(r'\{[^{}]*"uuid"[^{}]*\}[^{}]*\}', text):
            try:
                entry = json.loads(match.group())
                if isinstance(entry, dict) and "uuid" in entry:
                    entries.append(entry)
            except (json.JSONDecodeError, ValueError):
                pass

    # Deduplicate by UUID
    seen = set()
    unique = []
    for e in entries:
        uid = e.get("uuid", "")
        if uid and uid not in seen:
            seen.add(uid)
            unique.append(e)
    return unique


def main():
    data = open(DB, "rb").read()
    print(f"File size: {len(data)} bytes")

    entries = scan_entries(data)
    print(f"Recovered {len(entries)} entries from raw data")

    if not entries:
        print("No entries recovered. Trying more aggressive scan...")
        entries = aggressive_scan(data)

    if entries:
        # Print sample
        for e in entries[:3]:
            term = e.get("terminologio", {})
            title = next(iter(term.values()), "?")
            print(f"  {e['uuid'][:8]} {title}")

        # Write clean DB
        print(f"\nWriting clean DB to {NEW}...")
        write_db(entries)
        print("Done!")
    else:
        print("Cannot recover. File may be too corrupted.")


def aggressive_scan(data: bytes) -> list[dict]:
    """More aggressive scan — look for JSON objects in the entire file."""
    entries = []
    # Find all JSON-like structures in the data
    decoder = json.JSONDecoder()
    text = data.decode("utf-8", errors="replace")

    pos = 0
    while pos < len(text):
        try:
            obj, end = decoder.raw_decode(text, pos)
            if isinstance(obj, dict) and "uuid" in obj:
                entries.append(obj)
            pos = end + 1
        except (json.JSONDecodeError, ValueError):
            pos += 1

    seen = set()
    unique = []
    for e in entries:
        uid = e.get("uuid", "")
        if uid and uid not in seen:
            seen.add(uid)
            unique.append(e)
    return unique


def write_db(entries: list[dict]):
    """Write recovered entries to a clean SQLite database."""
    if NEW.exists():
        NEW.unlink()

    conn = sqlite3.connect(str(NEW), timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")

    conn.execute("""CREATE TABLE encik (
        uuid TEXT PRIMARY KEY, difinio TEXT NOT NULL DEFAULT '',
        terminologio TEXT NOT NULL DEFAULT '{}', terminologio_search TEXT NOT NULL DEFAULT '',
        difinoj TEXT NOT NULL DEFAULT '{}', enhavo TEXT NOT NULL DEFAULT '',
        superklaso TEXT NOT NULL DEFAULT '[]', ligilo TEXT NOT NULL DEFAULT '[]',
        fonto TEXT NOT NULL DEFAULT '[]', citajo TEXT NOT NULL DEFAULT '[]',
        datumo TEXT NOT NULL DEFAULT '{}', semantika TEXT NOT NULL DEFAULT '[]',
        ligiloj TEXT NOT NULL DEFAULT '[]', kreita_je TEXT NOT NULL, modifita_je TEXT NOT NULL
    )""")

    count = 0
    for e in entries:
        try:
            row = {}
            for col in COLUMNS:
                val = e.get(col, "")
                if col in JSON_FIELDS and isinstance(val, (dict, list)):
                    val = json.dumps(val, ensure_ascii=False)
                row[col] = str(val) if val else ""
            row["uuid"] = e["uuid"]

            cols = ", ".join(f'"{c}"' for c in COLUMNS)
            ph = ", ".join(["?"] * len(COLUMNS))
            conn.execute(
                f"INSERT INTO encik ({cols}) VALUES ({ph})",
                [row[c] for c in COLUMNS],
            )
            count += 1
        except Exception as exc:
            print(f"  Skip {e.get('uuid', '?')[:8]}: {exc}")

    conn.commit()

    for idx in [
        "CREATE INDEX idx_encik_uuid_prefix ON encik(substr(uuid, 1, 8))",
        "CREATE INDEX idx_encik_kreita_je ON encik(kreita_je)",
        "CREATE INDEX idx_encik_terminologio_search ON encik(terminologio_search)",
        "CREATE INDEX idx_encik_difinio_lower ON encik(LOWER(difinio))",
    ]:
        conn.execute(idx)
    conn.commit()
    conn.close()
    print(f"Wrote {count} entries to {NEW}")


if __name__ == "__main__":
    main()
