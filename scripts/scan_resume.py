#!/usr/bin/env python3
"""Generate the photographer resume guide from live CSVs.

Usage:
    python3 scripts/scan_resume.py
    python3 scripts/scan_resume.py --out docs/scan_resume.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from register_catalog import (  # noqa: E402
    DRIVE_URL,
    EXTRA_BOOKS,
    PRIORITY_ORDER,
    ROOT,
    analyze_register,
    load_manifest,
)

DEFAULT_OUT = ROOT / "docs" / "scan_resume.md"


def _page_text(stats: dict) -> str:
    if stats.get("last_source"):
        page = stats.get("last_page")
        extra = ""
        if page and str(page) not in stats["last_source"]:
            extra = f" (page {page})"
        return f"{stats['last_source']}{extra}"
    if stats.get("last_page"):
        return str(stats["last_page"])
    if stats.get("images"):
        return ", ".join(stats["images"][:3]) + ("…" if len(stats["images"]) > 3 else "")
    return "—"


def _holes_text(stats: dict) -> str:
    holes = stats.get("holes") or []
    if holes:
        return ", ".join(f"page {n}" for n in holes)
    if stats.get("fragment"):
        already = stats.get("already_pages") or []
        if already and len(already) <= 12:
            return "photograph everything except " + ", ".join(str(n) for n in already)
        if stats.get("images"):
            return "photograph everything except " + ", ".join(stats["images"])
        return "photograph the rest of the volume"
    return "none known"


def build_markdown(registers: list[dict]) -> str:
    by_id = {item["id"]: item for item in registers}
    priority_ids = [rid for rid in PRIORITY_ORDER if rid in by_id or rid == "first_communion_2014"]

    lines = [
        "# Photographer resume guide",
        "",
        "Where to stand in each physical register: the **latest date** and **last named",
        "record** already in the database, the **last page photographed**, and where to",
        "start taking pictures. Regenerated from the live CSVs:",
        "",
        "```bash",
        "python3 scripts/scan_resume.py",
        "```",
        "",
        "Shared Drive: " + DRIVE_URL,
        "",
        "## How to photograph and upload",
        "",
        "1. Open the physical book to the last named record below. Confirm you are in",
        "   the right volume, then start at the **next blank line / next page**.",
        "2. Also shoot any **known missing pages** listed for that book.",
        "3. Name files `PAGE 012.JPG` (or `PAGE 12-13.JPG` for a two-page spread),",
        "   matching the names already used in that folder. Keep the spaces.",
        "4. Upload **individual page images** into the existing book folder on Drive",
        "   (or drop them in `incoming/<register_id>/` in this repo). Replacing a zip",
        "   with a newer dump also works: the watcher unpacks new `PAGE ….JPG` files.",
        "   Do not upload the duplicate `NEW 2023–2024 UPDATED` zip.",
        "5. Skip title pages with no names, totals-only pages, and account/fee pages",
        "   (put accounts in a subfolder named `_accounts` if you still want an archive",
        "   photo).",
        "",
        "New JPGs on Drive are picked up by `scripts/watch_drive.py` and, when a vision",
        "API key is configured, transcribed into the website CSVs. See",
        "[drive_ingest.md](drive_ingest.md).",
        "",
        "## Start here",
        "",
        "Priority is volumes that exist on the shelf but are missing most of their pages",
        "on Drive, then known single-page holes.",
        "",
    ]

    extra_by_id = {book["id"]: book for book in EXTRA_BOOKS}
    rank = 0
    for rid in priority_ids:
        rank += 1
        if rid in extra_by_id:
            book = extra_by_id[rid]
            lines += [
                f"{rank}. **{book['title']}** — no scans on Drive yet.",
                f"   Start: {book['start']}",
                "",
            ]
            continue
        stats = by_id[rid]
        last = stats["last_name"] or "index/tabs only"
        when = stats["last_date_text"] or "—"
        lines += [
            f"{rank}. **{stats['title']}** — last in DB: {last} ({when}) on {_page_text(stats)}.",
            f"   Start: {stats['photography']}",
            "",
        ]

    lines += [
        "## Every register",
        "",
        "Latest date / last record are taken from the **last named entry on the highest",
        "numbered record page** (not the name index). Cemetery plot books are",
        "photographed by page, not by burial date.",
        "",
        "| Register | Status | Latest date | Last named record | Last page | Known holes |",
        "|---|---|---|---|---|---|",
    ]

    def status_label(stats: dict) -> str:
        return "fragment" if stats["fragment"] else "complete for Drive"

    for stats in registers:
        lines.append(
            f"| {stats['title']} | {status_label(stats)} | "
            f"{stats['last_date_text'] or '—'} | {stats['last_name'] or '(index only)'} | "
            f"{_page_text(stats)} | {_holes_text(stats)} |"
        )
    for book in EXTRA_BOOKS:
        lines.append(
            f"| {book['title']} | not on Drive | — | — | none | photograph from the start |"
        )

    lines += ["", "## Details"]

    for stats in registers:
        lines += ["", f"### {stats['title']}", ""]
        lines.append(f"- **Register id:** `{stats['id']}` (folder name for `incoming/{stats['id']}/`)")
        lines.append(f"- **Status:** {status_label(stats)}")
        lines.append(f"- **Records in the website:** {stats['record_count']:,} named entries"
                     + (f" + {stats['index_count']:,} index rows" if stats['index_count'] else "")
                     + f", from {stats['image_count']} scan(s)")
        if stats["last_name"]:
            lines.append(
                f"- **Last named record:** {stats['last_name']}"
                + (f" — {stats['last_date_text']}" if stats['last_date_text'] else "")
            )
        else:
            lines.append("- **Last named record:** none (index/tabs only)")
        lines.append(f"- **Last page on Drive:** {_page_text(stats)}")
        if stats["holes"]:
            lines.append("- **Known missing pages:** " + ", ".join(str(n) for n in stats["holes"]))
        if stats["fragment"] and stats["images"]:
            shown = ", ".join(f"`{name}`" for name in stats["images"])
            lines.append(f"- **Already photographed (do not redo):** {shown}")
        if stats["photography"]:
            lines.append(f"- **Start photographing:** {stats['photography']}")
        lines.append(
            "- **Upload to:** the existing Drive folder for this book, as "
            f"`PAGE ….JPG`, or `incoming/{stats['id']}/PAGE ….JPG`."
        )

    lines += ["", "## Books not yet in the database"]
    for book in EXTRA_BOOKS:
        lines += [
            "",
            f"### {book['title']}",
            "",
            f"- **Register id:** `{book['id']}`",
            "- **Status:** no scans on Drive / no CSV yet",
            f"- **Start photographing:** {book['start']}",
        ]

    lines += [
        "",
        "## After the photos are on Drive",
        "",
        "The ingest job lists the Drive folder, downloads new JPGs, transcribes them",
        "when a vision API key is present, and merges new rows into `transcriptions/`",
        "so the search website picks them up. Until that job is enabled on GitHub,",
        "run locally:",
        "",
        "```bash",
        "python3 scripts/watch_drive.py --download-new incoming",
        "python3 scripts/ingest_incoming.py",
        "python3 scripts/scan_resume.py",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Markdown path to write")
    args = parser.parse_args()

    registers = [analyze_register(item) for item in load_manifest()]
    text = build_markdown(registers)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(registers)} registers)")


if __name__ == "__main__":
    main()
