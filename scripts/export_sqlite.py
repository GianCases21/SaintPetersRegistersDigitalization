#!/usr/bin/env python3
"""Build a SQLite database from the transcription CSVs.

Usage:
    python3 scripts/export_sqlite.py            # writes registers.db
    sqlite3 registers.db "SELECT * FROM records WHERE surname LIKE '%Monaghan%'"

The CSVs remain the master copy; re-run this script after any CSV changes.
Each register CSV becomes its own table, and a combined `records` view/table
holds every row with a shared set of columns for cross-register searches.
"""

import csv
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTIONS = ROOT / "transcriptions"
DB_PATH = ROOT / "registers.db"


def sanitize(name: str) -> str:
    return "".join(c if c.isalnum() or c == "_" else "_" for c in name)


def main() -> None:
    csv_files = sorted(TRANSCRIPTIONS.glob("*.csv"))
    if not csv_files:
        sys.exit(f"no CSVs found in {TRANSCRIPTIONS}")

    DB_PATH.unlink(missing_ok=True)
    con = sqlite3.connect(DB_PATH)

    all_columns: list[str] = []
    tables: list[tuple[str, list[str]]] = []

    for f in csv_files:
        with open(f, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = [sanitize(h) for h in next(reader)]
            rows = list(reader)
        table = sanitize(f.stem)
        cols = ", ".join(f'"{h}" TEXT' for h in header)
        con.execute(f'CREATE TABLE "{table}" ({cols})')
        placeholders = ", ".join("?" * len(header))
        con.executemany(
            f'INSERT INTO "{table}" VALUES ({placeholders})',
            (row + [""] * (len(header) - len(row)) for row in rows),
        )
        tables.append((table, header))
        for h in header:
            if h not in all_columns:
                all_columns.append(h)
        print(f"{table}: {len(rows)} rows")

    selects = []
    for table, header in tables:
        cols = ", ".join(
            f'"{c}"' if c in header else f'NULL AS "{c}"' for c in all_columns
        )
        selects.append(f'SELECT {cols} FROM "{table}"')
    con.execute("CREATE VIEW records AS " + " UNION ALL ".join(selects))

    con.commit()
    con.close()
    print(f"\nWrote {DB_PATH}")
    print("Try:  sqlite3 registers.db \"SELECT given_name, surname, year FROM records WHERE surname LIKE '%onaghan%'\"")


if __name__ == "__main__":
    main()
