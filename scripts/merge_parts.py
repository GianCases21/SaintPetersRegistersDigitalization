#!/usr/bin/env python3
"""Merge transcription part files into the final register CSVs.

Part files live in transcriptions/parts/ and are produced by transcription
workers (or by hand). This script groups them by register, de-duplicates
identical rows, sorts by page, and writes the final CSVs that the website
and query tools read. Re-run after any part file changes.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / "transcriptions" / "parts"
OUT = ROOT / "transcriptions"

GROUPS = {
    "st_joseph_section_1939.csv": ["st_joseph_pages_*.csv"],
    "st_joseph_section_1939_index.csv": ["st_joseph_index*.csv"],
    "cemetery_plots_1847.csv": ["cem1847_*.csv"],
    "interments_1847.csv": ["interments_1847_*.csv"],
    "cemetery_1854.csv": ["cemetery_1854_*.csv"],
    "baptism_1839.csv": ["baptism_1839_*.csv"],
    "marriage_1840.csv": ["marriage_1840_*.csv"],
    "first_communion_1895.csv": ["first_communion_1895_*.csv"],
    "sick_call_1973.csv": ["sick_call_1973_*.csv"],
}


def page_key(row: dict) -> tuple:
    page = row.get("page") or row.get("page_no") or "0"
    m = re.search(r"\d+", page)
    return (int(m.group()) if m else 0, row.get("source_image", ""))


def main() -> None:
    for out_name, patterns in GROUPS.items():
        files = sorted({f for pat in patterns for f in PARTS.glob(pat)})
        if not files:
            continue
        header: list[str] | None = None
        rows: list[dict] = []
        seen = set()
        for f in files:
            with open(f, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                if header is None:
                    header = reader.fieldnames
                elif reader.fieldnames != header:
                    raise SystemExit(f"{f} header mismatch for {out_name}")
                for row in reader:
                    key = tuple(row.get(h, "") for h in header)
                    if key in seen:
                        continue
                    seen.add(key)
                    rows.append(row)
        rows.sort(key=page_key)
        out_path = OUT / out_name
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)
        print(f"{out_name}: {len(rows)} rows from {len(files)} part file(s)")


if __name__ == "__main__":
    main()
