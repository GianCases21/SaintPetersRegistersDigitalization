#!/usr/bin/env python3
"""Print a manager briefing for the Saint Peter's digitization project.

Reads live CSV counts from transcriptions/ so the numbers stay current.

Usage:
    python3 scripts/manager_report.py
    python3 scripts/manager_report.py --out briefing.md
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTIONS = ROOT / "transcriptions"
MANIFEST = TRANSCRIPTIONS / "manifest.json"
DRIVE_URL = "https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj"
SITE_NOTE = (
    "Search website: open index.html (GitHub Pages from the main branch, "
    "or python3 -m http.server 8000 in the repo folder)."
)

# Coverage notes that numbers alone cannot show. Keep in sync with README.
COVERAGE = {
    "st_joseph_section_1939": "Full plot book on Drive (pages 17–79).",
    "st_joseph_section_1939_index": "Front-of-book name index, complete.",
    "cemetery_plots_1847": "Complete for named plot pages on Drive.",
    "reception_full_communion": "Whole book (5 people). Title page has no names.",
    "interments_1847": "Burials pages 2–62. Later pages are church accounts, not burials.",
    "cemetery_1854": "Complete for Drive scans.",
    "baptism_1839": "Baptisms pages 1–133. Pages 134–147 are other sacraments (see funerals / early confirmation).",
    "confirmation_early": "Confirmation lists bound in the back of the 1839 baptism book (pages 135–147).",
    "funerals_1868": "“Register of Funerals” leaf + slip on baptism page 134.",
    "marriage_1840": "Complete marriage book on Drive. Overlapping photos of the same openings were de-duplicated.",
    "marriage_1840_index": "Letter-tab index; only the tabs that exist on Drive.",
    "first_communion_1895": "Complete named pages. PAGE 183 is totals only (no names).",
    "sick_call_1973": "Complete visits + name index.",
    "confirmation_2015": "All Drive scans. Pages 4 and 15 were never uploaded.",
    "confirmation_1991": "Complete named pages. Title page has no names.",
    "baptism_1989": "Complete for Drive scans.",
    "first_communion_1953": "Complete for Drive scans.",
    "death_2001": "Complete for Drive scans.",
    "death_1990": "Complete for Drive scans.",
    "marriage_1872": "Complete for Drive scans (all 65 pages).",
    "marriage_2009": "All Drive scans. Page 18 was never uploaded.",
    "marriage_1937": "FRAGMENT — only PAGE 58 and 60 are on Drive.",
    "confirmation_1895": "FRAGMENT — year/page index only (PAGE 000).",
    "confirmation_1974": "FRAGMENT — PAGE 164 is a misfiled 1923 baptism leaf.",
    "death_c_1924": "FRAGMENT — only PAGE 46 is on Drive.",
    "baptism_2011": "FRAGMENT — 5 scans (entries + name indexes).",
    "baptism_1965": "Name index letter tabs only. Title page has no names.",
    "first_communion_1962": "FRAGMENT — two index scans (R2–S and X–Y).",
    "death_section_e": "Complete for Drive scans.",
    "death_index": "Complete letter-tab death index (30 scans).",
    "death_1895": "Complete for Drive scans.",
    "confirmation_1957": "FRAGMENT — PAGE 96, 99, and letter tabs on Drive.",
    "marriage_1908": "Complete for Drive scans (all 72 pages).",
    "confirmation_1942": "Complete named pages. Title page has no names.",
    "death_section_d": "FRAGMENT — 5 cemetery-plot scans.",
    "baptism_fragments": "FRAGMENT — stray leaves from 1875–1903 and 1904–1921.",
}

SCAN_NEXT = [
    (
        "Baptism 1875–1903 and 1904–1921",
        "Only a handful of stray pages are on Drive. Photograph the rest of both books.",
    ),
    (
        "Marriage 1937–1963",
        "Only pages 58 and 60 are on Drive. Photograph the remaining volume.",
    ),
    (
        "Death C 1924–1964",
        "Only page 46 is on Drive. Photograph the remaining volume.",
    ),
    (
        "Confirmation 1895–1944, 1957–1964, 1974–1990",
        "Index/fragment pages only. Photograph the missing class lists (1974 folder currently holds a misfiled baptism leaf).",
    ),
    (
        "First Communion 1962–1970 and 2014–",
        "1962–1970 has two index scans; the 2014– Drive folder is empty.",
    ),
    (
        "Baptism 2011–",
        "Five scans only. Photograph the rest of the current book.",
    ),
    (
        "Death SECTION D",
        "Five cemetery-plot scans. Photograph the rest of that book.",
    ),
    (
        "Known missing single pages",
        "Confirmation 2015 pages 4 and 15; Marriage 2009 page 18. Re-shoot if they exist in the physical book.",
    ),
]


def load_registers() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out = []
    for item in manifest["registers"]:
        path = TRANSCRIPTIONS / item["file"]
        rows: list[dict] = []
        if path.exists():
            with path.open(newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
        review = sum(1 for r in rows if (r.get("needs_review") or "").strip().lower() == "yes")
        images = { (r.get("source_image") or "").strip() for r in rows if (r.get("source_image") or "").strip() }
        years = sorted({ (r.get("year") or "").strip() for r in rows if (r.get("year") or "").strip() })
        out.append({
            **item,
            "rows": len(rows),
            "needs_review": review,
            "images": len(images),
            "year_min": years[0] if years else "",
            "year_max": years[-1] if years else "",
            "note": COVERAGE.get(item["id"], ""),
            "fragment": "fragment" in (item.get("title") or "").lower()
            or "FRAGMENT" in COVERAGE.get(item["id"], ""),
        })
    return out


def fmt(n: int) -> str:
    return f"{n:,}"


def build_report(registers: list[dict]) -> str:
    total_rows = sum(r["rows"] for r in registers)
    total_review = sum(r["needs_review"] for r in registers)
    total_images = sum(r["images"] for r in registers)
    by_type = Counter(r["type"] for r in registers)
    fragments = [r for r in registers if r["fragment"]]
    complete = [r for r in registers if not r["fragment"]]
    today = date.today().isoformat()

    type_lines = "\n".join(
        f"- {kind}: {count} register(s)" for kind, count in sorted(by_type.items())
    )

    def table(rows: list[dict]) -> str:
        lines = [
            "| Register | Records | Scans used | Flagged for review | Notes |",
            "|---|---:|---:|---:|---|",
        ]
        for r in rows:
            note = r["note"].replace("|", "/")
            lines.append(
                f"| {r['title']} | {fmt(r['rows'])} | {fmt(r['images'])} | "
                f"{fmt(r['needs_review'])} | {note} |"
            )
        return "\n".join(lines)

    scan_lines = "\n".join(f"- **{title}.** {detail}" for title, detail in SCAN_NEXT)

    return f"""# Saint Peter's Registers — status for leadership
Generated {today} from the live transcription files.

## Bottom line

**Every named page already on the shared Google Drive is in the searchable database.**
That is **{len(registers)} registers** and **{fmt(total_rows)} records**, drawn from **{fmt(total_images)}** distinct scans.

What remains is **photographing the rest of the physical books** and uploading those images. After that, transcription and the website can follow the same process we already use — and can be automated so new scans appear in search without a developer in the loop.

{SITE_NOTE}

Shared Drive: {DRIVE_URL}

## What has been built

1. **A searchable website** — type a name, year, or register; results come from the transcribed spreadsheets. Host on GitHub Pages from the `main` branch (hard-refresh after updates: Ctrl+Shift+R).
2. **Structured records (CSV)** — one file per register under `transcriptions/`, with fields suited to that book (child/parents for baptisms, bride/groom for marriages, grave/tier for cemetery books, and so on).
3. **A review trail** — every row points at the original scan filename (`source_image`). Uncertain handwriting is marked `needs_review` instead of guessed silently. **{fmt(total_review)}** rows currently carry that flag (often because one field on a faded page was hard to read, not because the whole entry is unusable).
4. **Tools** — download scans from Drive; search from the command line; optionally build a SQLite database from the CSVs.
5. **Rules of the road** — transcription conventions and column layouts live in `docs/transcription_guide.md` and `docs/schemas.md`, so the next batch of pages can be done the same way.

This is **not** ordinary OCR (Adobe / Google Docs). Nineteenth-century cursive and faded ink need a vision model, then a person on the flagged lines.

## How it works today (after a page is photographed)

1. Scan the page (person, on site).
2. Upload the image to the correct book folder on the shared Drive.
3. Download the new images.
4. Transcribe them into the matching CSV (vision model + the existing schema).
5. Merge into the website files and publish.

Steps 1–2 are parish work. Steps 3–5 are still started by hand. Steps 3–5 are what we can automate once uploads are consistent (see below).

## Inventory

**{len(complete)} volumes** are complete for everything currently on Drive. **{len(fragments)}** are fragments — the physical book continues, but those pages were never photographed.

By type:
{type_lines}

### Complete for Drive (named pages transcribed)

{table(complete)}

### Fragments (more scanning needed)

{table(fragments)}

## What we are *not* putting in the database

- Title pages with no personal names
- Parish **account / fee** pages (for example later Interments 1847 pages, baptism pages 148–149)
- Totals-only pages (First Communion 1895 page 183)
- Blank or layout-only cemetery grids
- Duplicate photographs of the same opening (we keep the clearer scan)

Those files can stay on Drive for the archive; they should not be treated as missing people.

## Photographing the rest — do this next

Priority is books that exist on the shelf but are only fragments on Drive:

{scan_lines}

Full per-register **latest date, last named record, last page, and where to
start photographing:** `docs/scan_resume.md` (regenerate with
`python3 scripts/scan_resume.py`).

**How to upload so the rest of the pipeline can be automated:**

- Put files in the **existing book folder**, not a second copy of the whole archive.
- Name images `PAGE 012.JPG` (or `PAGE 12-13.JPG` for a two-page spread). Match the names already used in that folder.
- **Preferred:** upload individual page images. If you instead replace a register zip, the watcher downloads that new dump and pulls out pages that are not already in the database. Do not upload the duplicate `NEW 2023–2024 UPDATED` zip.
- One book, one folder. Do not duplicate St. Joseph / Cemetery Plots / First Communion 1895 in a second tree.
- Skip blank title pages, or put accounts in a subfolder named `_accounts`.

## Making it automatic after scanning

| Phase | What you get | What we need from the parish / IT |
|---|---|---|
| **A. Detect new scans** | A daily list: “these new pages are not in the database yet.” `scripts/watch_drive.py` plus `.github/workflows/ingest-drive.yml`. | Upload pages as individual JPGs (above). Enable GitHub Actions on the repo. |
| **B. Transcribe new scans** | New pages become CSV rows overnight, flagged `needs_review=yes`. | A vision-model API key (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`) and a small budget. A Google **service account** invited to the Drive folder if the folder is made private. |
| **C. Publish + review** | Website updates itself. Someone spot-checks rows marked needs review. | Name a reviewer. Merges to `main` publish GitHub Pages. |

**Blockers for a Drive watcher today**

1. Listing the folder with a public link (`gdown`) works only while the folder is “anyone with the link.” Church records should probably be **private**, which requires the official Google Drive API and a service account.
2. This project’s GitHub access cannot store secrets; a repo admin has to add a vision API key (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`) so new pages are transcribed, not only listed.
3. Detection is not transcription. Without that key, `transcriptions/pending_scans.md` still lists every new JPG so nothing sits on Drive unnoticed.

Until A–C are in place, the operating model stays: photograph → upload → we transcribe → website updates.

## What to ask of leadership

1. **Keep scanning** the fragment volumes first, using the naming rules above.
2. **Merge the current leftover-pages work** (funerals 1868, 1854–1875 confirmations in the baptism book, 1840 marriage index) so the public site matches the Drive.
3. **Approve automation phase A** (detect new files) as soon as new scans are uploaded as pages, not zips.
4. **Name a reviewer** for the {fmt(total_review)} uncertain readings, and for future batches.
5. **Decide privacy** on the Drive folder (stay link-shared vs service account + private folder).

## One sentence

The search site and database are built and already cover every named page on Drive ({fmt(total_rows)} records). Remaining work is photographing the incomplete books; if new scans are uploaded as individual pages, we can watch Drive and feed the same transcription pipeline so the site updates with little more than a review of uncertain names.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", help="write Markdown to this file as well as stdout")
    args = parser.parse_args()

    if not MANIFEST.exists():
        raise SystemExit(f"missing {MANIFEST}")

    report = build_report(load_registers())
    print(report)
    if args.out:
        path = Path(args.out)
        path.write_text(report + "\n", encoding="utf-8")
        print(f"\nWrote {path}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
