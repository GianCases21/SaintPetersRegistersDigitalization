#!/usr/bin/env python3
"""Search the transcribed church records.

Examples:
    python3 scripts/query.py --name Monaghan
    python3 scripts/query.py --year 1940
    python3 scripts/query.py --register st_joseph_section_1939 --name Cody
    python3 scripts/query.py --name "O'Connell" --year 1966
"""

import argparse
import csv
from pathlib import Path

TRANSCRIPTIONS = Path(__file__).resolve().parent.parent / "transcriptions"

NAME_COLUMNS = (
    "surname", "given_name", "plot_owner", "name", "child", "father",
    "mother", "mother_maiden", "groom", "bride", "groom_surname",
    "groom_given", "bride_surname", "bride_given", "groom_parents",
    "bride_parents", "sponsors", "sponsor", "witnesses", "officiant",
    "priest", "parents", "nearest_relative",
)


def row_matches(row: dict, name: str | None, year: str | None) -> bool:
    if name:
        haystack = " ".join(row.get(c, "") or "" for c in NAME_COLUMNS).lower()
        if name.lower() not in haystack:
            return False
    if year:
        if year not in " ".join(v or "" for v in row.values()):
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", help="name to search for (partial match, any name field)")
    parser.add_argument("--year", help="year to search for, e.g. 1940")
    parser.add_argument("--register", help="limit to one register (CSV filename without .csv)")
    args = parser.parse_args()

    if not (args.name or args.year or args.register):
        parser.error("give at least one of --name, --year, --register")

    csv_files = sorted(TRANSCRIPTIONS.glob("*.csv"))
    if args.register:
        csv_files = [f for f in csv_files if f.stem == args.register]
        if not csv_files:
            parser.error(f"no register named {args.register!r} in {TRANSCRIPTIONS}")

    total = 0
    for csv_file in csv_files:
        with open(csv_file, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if not row_matches(row, args.name, args.year):
                    continue
                total += 1
                fields = [
                    f"{k}={v}" for k, v in row.items()
                    if v and k not in ("register", "source_image")
                ]
                print(f"[{csv_file.stem}] " + "  ".join(fields))
                print(f"    scan: {row.get('source_image', '?')}")

    print(f"\n{total} record(s) found.")


if __name__ == "__main__":
    main()
