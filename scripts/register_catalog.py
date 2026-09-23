"""Shared register metadata for photography resume + Drive ingest.

This module has no CLI. Import it from scan_resume.py, watch_drive.py, and
ingest_incoming.py.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTIONS = ROOT / "transcriptions"
MANIFEST = TRANSCRIPTIONS / "manifest.json"
DRIVE_URL = "https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj"
DRIVE_FOLDER_ID = "1JyB49OP-yAV43iojbGje6cwvLNFPdvZj"

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic"}
SKIP_NAME_RE = re.compile(
    r"(^title\b|\btitle\s*\d|\blogbook\b|_accounts|accounts?\s*only)",
    re.I,
)

PRIMARY_DATE_COL = {
    "baptism": "baptism_date",
    "marriage": "marriage_date",
    "confirmation": "confirmation_date",
    "death": "death_date",
    "interments": "burial_date",
    "cemetery_plots": "date_of_burial",
    "first_communion": "communion_date",
    "sick_call": "call_date",
    "reception": "date_of_reception",
    "name_index": None,
}

DATE_FALLBACKS = (
    "marriage_date",
    "baptism_date",
    "confirmation_date",
    "death_date",
    "burial_date",
    "date_of_burial",
    "date_of_death",
    "call_date",
    "date_of_reception",
    "communion_date",
)

MONTHS = {
    **{m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)},
    **{
        name: i
        for i, name in enumerate(
            "January February March April May June July August September October November December".split(),
            1,
        )
    },
}

# More-specific path tokens first. Each rule is (register_id, tokens that
# must all appear in the lowercased path).
PATH_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("confirmation_early", ("confirmation", "1854")),
    ("funerals_1868", ("funeral",)),
    ("marriage_1840_index", ("marriage 1840", "index")),
    ("marriage_1840", ("marriage 1840",)),
    ("baptism_2011", ("baptism 2011",)),
    ("baptism_1989", ("baptism 1989",)),
    ("baptism_1965", ("baptism 1965",)),
    ("baptism_1839", ("baptism 1839",)),
    ("baptism_fragments", ("baptism 1875",)),
    ("baptism_fragments", ("baptism 1904",)),
    ("confirmation_2015", ("confirmation 2015",)),
    ("confirmation_1991", ("confirmation 1991",)),
    ("confirmation_1942", ("confirmation 1942",)),
    ("confirmation_1957", ("confirmation 1957",)),
    ("confirmation_1895", ("confirmation 1895",)),
    ("confirmation_1974", ("confirmation 1974",)),
    ("marriage_2009", ("marriage 2009",)),
    ("marriage_1937", ("marriage 1937",)),
    ("marriage_1908", ("marriage 1908",)),
    ("marriage_1872", ("marriage 1872",)),
    ("first_communion_1962", ("first communion 1962",)),
    ("first_communion_1953", ("first communion 1953",)),
    ("first_communion_1895", ("first communion 1895",)),
    ("first_communion_2014", ("first communion 2014",)),
    ("death_2001", ("death 2001",)),
    ("death_1990", ("death 1990",)),
    ("death_1895", ("death 1895",)),
    ("death_c_1924", ("death c",)),
    ("death_c_1924", ("1924-1964",)),
    ("death_section_e", ("section e",)),
    ("death_section_d", ("section d",)),
    ("sick_call_1973", ("sick call",)),
    ("reception_full_communion", ("reception",)),
    ("cemetery_1854", ("1854-1870",)),
    ("cemetery_1854", ("record of cemet",)),
    ("interments_1847", ("enterment",)),
    ("interments_1847", ("interment",)),
    ("cemetery_plots_1847", ("cemetary plots",)),
    ("cemetery_plots_1847", ("cemetery plots",)),
    ("st_joseph_section_1939_index", ("st. joseph", "index")),
    ("st_joseph_section_1939_index", ("st joseph", "index")),
    ("st_joseph_section_1939", ("st. joseph",)),
    ("st_joseph_section_1939", ("st joseph",)),
    ("death_index", ("death registers", "index")),
]

# Zip dumps currently at the Drive root. Used to label snapshot rows.
ZIP_LABELS = {
    "baptism 1839": "Baptism 1839–1875 / Marriage 1840–1871 (shared zip)",
    "baptism registers": "Baptism Registers zip (1989, 1965, 2011, fragments)",
    "cemetary plots": "Cemetery Plots 1847 zip",
    "confirmation registers": "Confirmation Registers zip",
    "death registers": "Death Registers zip",
    "first communion": "First Communion Registers zip",
    "marriage registers": "Marriage Registers zip",
    "new 2023": "NEW 2023–2024 UPDATED (duplicate portraits of the 1839 book)",
    "reception": "Reception Into Full Communion zip",
    "record of cemet": "Record of Cemetery 1854–1870 zip",
    "enterment": "Record of Interments 1847–54 zip",
    "sick call": "Sick Call Register zip",
    "st. joseph": "St. Joseph Section 1939 zip",
    "st joseph": "St. Joseph Section 1939 zip",
}

# Pages that look missing from the CSV min–max range but should not be
# re-shot (overlapping photos, blanks, accounts, totals).
NOT_HOLES = {
    "marriage_1840": {57, 58, 73, 74},  # clearer 59–60 / 75–76 photos kept
    "first_communion_1895": {183},  # totals only
}

# Real missing pages inside an otherwise-photographed run.
KNOWN_HOLES = {
    "confirmation_2015": [4, 15],
    "marriage_2009": [18],
    "st_joseph_section_1939": [67],
    "marriage_1937": [59],
    "cemetery_1854": [17],
    "confirmation_1957": [97, 98],
}

FRAGMENTS = {
    "marriage_1937",
    "confirmation_1895",
    "confirmation_1974",
    "death_c_1924",
    "baptism_2011",
    "baptism_1965",
    "first_communion_1962",
    "confirmation_1957",
    "death_section_d",
    "baptism_fragments",
}

# Extra physical books with no CSV yet.
EXTRA_BOOKS = [
    {
        "id": "first_communion_2014",
        "title": "First Communion 2014–",
        "type": "first_communion",
        "status": "not_on_drive",
        "start": (
            "The Drive folder for this book was empty. If the volume is on the "
            "shelf, photograph from the first named class (usually page 1) using "
            "PAGE 001.JPG naming, and upload into a folder named "
            "`First Communion 2014-` (or `incoming/first_communion_2014/`)."
        ),
    },
]

# Human photography instructions. Computed last-page/name/date are appended
# by scan_resume.py; these strings say what to do in the physical book.
PHOTOGRAPHY = {
    "baptism_1839": (
        "This baptism volume is finished on Drive through the last baptism. "
        "Page 133 notes “See new Registry” and the rest of the page is blank. "
        "Do not reshoot 1–133. Pages 134–147 are funerals/confirmations "
        "(already transcribed). Skip account pages after that. "
        "Start the next baptisms in Baptism 1875–1903."
    ),
    "confirmation_early": (
        "Confirmation lists bound in the back of the 1839 baptism book "
        "(pages 135–147) are complete on Drive. Do not reshoot."
    ),
    "funerals_1868": (
        "The 1868 funerals leaf (baptism page 134 + attached slip) is complete. "
        "Do not reshoot."
    ),
    "marriage_1840": (
        "This marriage book is complete on Drive through the 31 Dec 1871 note "
        "to see the next registry. Do not reshoot pages 57–58 or 73–74 "
        "(overlapping photos; we kept the clearer 59–60 and 75–76 scans). "
        "Continue marriages in Marriage 1872–1907."
    ),
    "marriage_1840_index": (
        "Letter-tab index of the 1840–1871 marriage book. Photograph any tab "
        "that is missing from Drive (we have A, F, H, I, M, Mc2–N, P, R, V, W, Y)."
    ),
    "marriage_1937": (
        "FRAGMENT. Photograph the whole 1937–1963 marriage book. Drive only has "
        "PAGE 58 and PAGE 60. Fill PAGE 59 and every page before 58 and after 60. "
        "After Collumb & Gartland (30 Dec 1946, end of 1946 on page 60), continue "
        "with the first 1947 marriage."
    ),
    "marriage_2009": (
        "Re-shoot page 18 if it has marriages (never uploaded). Then continue the "
        "current book after Velasquez Garcia & Vargas Pierotti on page 23 "
        "(19 Oct 2019, entry 13)."
    ),
    "marriage_1872": (
        "Complete for Drive through the last page. Continue later marriages in "
        "Marriage 1908–1936."
    ),
    "marriage_1908": (
        "Complete for the scans on Drive. Continue later marriages in "
        "Marriage 1937–1963 (that book is still a fragment)."
    ),
    "baptism_2011": (
        "FRAGMENT of the current baptism book. Drive only has PAGE 046, PAGE 067, "
        "and three index tabs. Photograph pages 1–45, 47–66, and 68 to the end. "
        "On page 46 the last named child is Moncayo, Ariana (23 Jul 2016). "
        "On page 67 the last named child is Hernandez, Gianna Marie (20 Apr 2019, "
        "entry 15) — continue from the next blank line / page 68."
    ),
    "baptism_1989": (
        "Complete for Drive through page 199. Continue later baptisms in "
        "Baptism 2011– (still a fragment)."
    ),
    "baptism_1965": (
        "FRAGMENT — letter-tab name index only. Photograph the actual baptism "
        "pages of the 1965–1972 book (and any missing letter tabs)."
    ),
    "baptism_fragments": (
        "FRAGMENT. Photograph the rest of Baptism 1875–1903 and Baptism 1904–1921. "
        "Already on Drive: PAGE I, 008, 014, 061, 358. Do not redo those five. "
        "PAGE 358 is an 1898 leaf of the 1875–1903 book (last named: Bogert, "
        "Francis, 9 Apr 1898). PAGE 061 is a 1916 leaf of the 1904–1921 book "
        "(last named: Oldham, William, 21 May 1916)."
    ),
    "confirmation_2015": (
        "Re-shoot pages 4 and 15 (never on Drive). Then continue the current "
        "book after Yeye, Justin Rafael (14 Jun 2019, page 21, entry 59)."
    ),
    "confirmation_1991": (
        "Complete for Drive through page 103. Continue later confirmations in "
        "Confirmation 2015–."
    ),
    "confirmation_1942": (
        "Complete for named pages on Drive. Title page has no names — skip it."
    ),
    "confirmation_1957": (
        "FRAGMENT. Drive only has PAGE 96, PAGE 99, and letter tabs. Photograph "
        "the rest of Confirmation 1957–1964, including pages 97–98."
    ),
    "confirmation_1895": (
        "FRAGMENT — year/page index only (PAGE 000). Photograph the actual "
        "class lists of Confirmation 1895–1944."
    ),
    "confirmation_1974": (
        "The Drive folder currently holds a misfiled 1923 baptism leaf (PAGE 164), "
        "not the 1974–1990 confirmation book. Photograph the real confirmation "
        "volume from the beginning."
    ),
    "death_c_1924": (
        "FRAGMENT. Only PAGE 46 is on Drive. Photograph the rest of Death C "
        "1924–1964."
    ),
    "death_section_d": (
        "FRAGMENT. Five cemetery-plot scans only. Photograph the rest of "
        "Death SECTION D."
    ),
    "death_section_e": (
        "Complete for Drive scans of this cemetery tier book."
    ),
    "death_1990": (
        "Complete for Drive. Continue later deaths in Death 2001–2018."
    ),
    "death_2001": (
        "Complete for Drive through April 2018. If the physical book continues "
        "after Fragapane, Damian (page 51), photograph from the next entry."
    ),
    "death_1895": (
        "Complete for Drive. Later deaths are in the 20th-century death books."
    ),
    "death_index": (
        "Letter-tab death index (30 scans). Photograph any missing tabs."
    ),
    "first_communion_1895": (
        "Complete for named pages on Drive. PAGE 183 is totals only — skip. "
        "Large unused numbered stretches are blank class pages, not missing people."
    ),
    "first_communion_1953": (
        "Complete for Drive. Continue later first communions in the 1962–1970 "
        "book (still a fragment) and 2014– (not on Drive)."
    ),
    "first_communion_1962": (
        "FRAGMENT — two index scans only (R2–S and X–Y). Photograph the actual "
        "class pages of First Communion 1962–1970."
    ),
    "sick_call_1973": (
        "Complete for Drive through March 2006. If the book continues after "
        "page 103, photograph from the next visit."
    ),
    "reception_full_communion": (
        "Whole book (5 people on PAGE 001). Title page has no names. Only "
        "photograph if new receptions were added after McKenzie May (7 Apr 2012)."
    ),
    "interments_1847": (
        "Burial pages 2–62 are complete. Later pages are church accounts — skip "
        "or put them in `_accounts`. Do not enter accounts as burials."
    ),
    "cemetery_1854": (
        "Complete for Drive through December 1870. Re-shoot page 17 if it has "
        "named burials (no rows in the CSV)."
    ),
    "cemetery_plots_1847": (
        "Complete for named plot pages on Drive. Blank/numbered-only pages "
        "(70, 79–81, 86–87, 92, 97, 149, 159, 179, and similar) do not need "
        "re-shooting."
    ),
    "st_joseph_section_1939": (
        "Plot book pages 17–79 are on Drive. Re-shoot page 67 if that leaf has "
        "graves (we have 66 then 68–69). Book ends at page 79."
    ),
    "st_joseph_section_1939_index": (
        "Front-of-book name index is complete (tabs AB through UV)."
    ),
}

PRIORITY_ORDER = [
    "baptism_fragments",
    "marriage_1937",
    "death_c_1924",
    "confirmation_1895",
    "confirmation_1957",
    "confirmation_1974",
    "first_communion_1962",
    "first_communion_2014",
    "baptism_2011",
    "baptism_1965",
    "death_section_d",
    "confirmation_2015",
    "marriage_2009",
]


def load_manifest() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return list(data["registers"])


def register_title(register_id: str) -> str:
    for item in load_manifest():
        if item["id"] == register_id:
            return item["title"]
    return register_id


def load_rows(csv_name: str) -> list[dict]:
    path = TRANSCRIPTIONS / csv_name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def csv_header(register_id: str) -> list[str] | None:
    for item in load_manifest():
        if item["id"] == register_id:
            rows_path = TRANSCRIPTIONS / item["file"]
            if not rows_path.exists():
                return None
            with rows_path.open(newline="", encoding="utf-8") as fh:
                reader = csv.reader(fh)
                header = next(reader, None)
                return header
    return None


def parse_date(value: str | None) -> datetime | None:
    text = (value or "").strip()
    if not text:
        return None
    text = text.replace(".", " ").replace(",", " ")
    text = re.sub(r"\s+", " ", text)
    match = re.search(r"([A-Za-z]{3,9})\s+(\d{1,2})\s+(\d{4})", text)
    if match:
        mon = MONTHS.get(match.group(1)) or MONTHS.get(match.group(1)[:3].title())
        if mon:
            try:
                return datetime(int(match.group(3)), mon, int(match.group(2)))
            except ValueError:
                return datetime(int(match.group(3)), mon, 1)
    match = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", text)
    if match:
        a, b, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
        for month, day in ((a, b), (b, a)):
            try:
                return datetime(year, month, day)
            except ValueError:
                continue
    match = re.search(r"(\d{4})", text)
    if match:
        year = int(match.group(1))
        if 1800 <= year <= 2100:
            return datetime(year, 1, 1)
    return None


def event_date(row: dict, register_type: str) -> datetime | None:
    primary = PRIMARY_DATE_COL.get(register_type)
    if primary and row.get(primary):
        parsed = parse_date(row.get(primary))
        if parsed:
            return parsed
    for col in DATE_FALLBACKS:
        if col == primary:
            continue
        parsed = parse_date(row.get(col))
        if parsed:
            return parsed
    year = (row.get("year") or "").strip()
    match = re.search(r"\d{4}", year)
    if match:
        return datetime(int(match.group()), 1, 1)
    return None


def is_index_row(row: dict, register_type: str) -> bool:
    if register_type == "name_index":
        return True
    notes = (row.get("notes") or "").strip().lower()
    if notes.startswith("index") or "index page_no" in notes or notes == "index_pair":
        return True
    src = (row.get("source_image") or "").upper()
    if src.startswith("INDEX"):
        return True
    return False


def person_label(row: dict) -> str:
    if row.get("groom_surname") or row.get("bride_surname"):
        groom = " ".join(
            part for part in [(row.get("groom_given") or "").strip(), (row.get("groom_surname") or "").strip()] if part
        )
        bride = " ".join(
            part for part in [(row.get("bride_given") or "").strip(), (row.get("bride_surname") or "").strip()] if part
        )
        if groom and bride:
            return f"{groom} & {bride}"
        return groom or bride
    surname = (row.get("surname") or "").strip()
    given = (row.get("given_name") or "").strip()
    if surname or given:
        if surname and given:
            return f"{surname}, {given}"
        return surname or given
    return (row.get("plot_owner") or "").strip()


def pages_from_filename(name: str) -> list[int]:
    match = re.search(r"PAGE\s+(\d+)(?:\s*[-–]\s*(\d+))?", name or "", re.I)
    if not match:
        return []
    start = int(match.group(1))
    nums = [start]
    if match.group(2):
        end = int(match.group(2))
        if start <= end <= start + 8:
            nums.extend(range(start + 1, end + 1))
        else:
            nums.append(end)
    return nums


def page_numbers(row: dict) -> list[int]:
    nums = pages_from_filename(row.get("source_image") or "")
    if nums:
        return nums
    found = [int(match.group()) for match in re.finditer(r"\d+", row.get("page") or "")]
    return found[:4]


def max_page(row: dict) -> int:
    nums = page_numbers(row)
    return max(nums) if nums else -1


def entry_sort_key(row: dict) -> tuple:
    raw = (row.get("entry_no") or "").strip()
    match = re.search(r"\d+", raw)
    return (int(match.group()) if match else 0,)


def format_date(value: datetime | None, fallback: str = "") -> str:
    if not value:
        return fallback
    if value.month == 1 and value.day == 1:
        return str(value.year)
    return f"{value.strftime('%b')} {value.day} {value.year}"


def analyze_register(item: dict) -> dict:
    rows = load_rows(item["file"])
    rtype = item.get("type") or ""
    images = sorted(
        {(row.get("source_image") or "").strip() for row in rows if (row.get("source_image") or "").strip()}
    )
    records = [row for row in rows if not is_index_row(row, rtype)]
    index_rows = [row for row in rows if is_index_row(row, rtype)]
    last_row = None
    last_key = None
    latest_date = None
    latest_date_row = None
    covered: set[int] = set()
    for index, row in enumerate(records):
        when = event_date(row, rtype)
        if when and (latest_date is None or when > latest_date):
            latest_date = when
            latest_date_row = row
        covered.update(page_numbers(row))
        page = max_page(row)
        key = (page, when or datetime(1, 1, 1), entry_sort_key(row), index)
        if last_key is None or key > last_key:
            last_key = key
            last_row = row
    holes = list(KNOWN_HOLES.get(item["id"], []))
    already = sorted(covered) if covered else []
    fragment = item["id"] in FRAGMENTS or "fragment" in (item.get("title") or "").lower()
    last_page = max_page(last_row) if last_row else None
    last_date = event_date(last_row, rtype) if last_row else None
    return {
        **item,
        "rows": len(rows),
        "record_count": len(records),
        "index_count": len(index_rows),
        "images": images,
        "image_count": len(images),
        "last_row": last_row,
        "last_name": person_label(last_row) if last_row else "",
        "last_page": last_page,
        "last_source": (last_row.get("source_image") if last_row else "") or "",
        "last_date": last_date,
        "last_date_text": format_date(
            last_date, (last_row.get("year") if last_row else "") or ""
        ),
        "latest_date": latest_date,
        "latest_date_text": format_date(latest_date),
        "latest_date_name": person_label(latest_date_row) if latest_date_row else "",
        "holes": holes,
        "already_pages": already,
        "fragment": fragment,
        "photography": PHOTOGRAPHY.get(item["id"], ""),
        "status": "fragment" if fragment else "complete_for_drive",
    }


def should_skip_filename(name: str) -> bool:
    stem = Path(name).name
    if SKIP_NAME_RE.search(stem):
        return True
    return False


def kind_for_name(name: str) -> str:
    suffix = Path(name).suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        return "image"
    if suffix == ".zip":
        return "zip"
    return "other"


def route_bound_in_pages(register_id: str, filename: str) -> str | None:
    """Baptism 1839 book also holds funerals + early confirmations."""
    nums = pages_from_filename(filename)
    if register_id in {"baptism_1839", "confirmation_early", "funerals_1868"}:
        if 134 in nums and (not nums or max(nums) <= 134):
            return "funerals_1868"
        if nums and min(nums) >= 135 and max(nums) <= 147:
            return "confirmation_early"
        if nums and min(nums) >= 148:
            return None
        if nums and max(nums) <= 133:
            return "baptism_1839"
    return register_id


def match_tokens(path_lower: str, tokens: tuple[str, ...]) -> bool:
    return all(token in path_lower for token in tokens)


def map_drive_path(path: str) -> str | None:
    """Map a Drive-relative or incoming/ path to a register id."""
    cleaned = path.replace("\\", "/").strip("/")
    parts = Path(cleaned).parts
    filename = parts[-1] if parts else ""
    if should_skip_filename(filename):
        return None

    for part in reversed(parts[:-1]):
        if part in {item["id"] for item in load_manifest()} or part == "first_communion_2014":
            return route_bound_in_pages(part, filename)

    lower = cleaned.lower().replace("_", " ")
    for register_id, tokens in PATH_RULES:
        if match_tokens(lower, tokens):
            return route_bound_in_pages(register_id, filename)
    return None


def zip_label(path: str) -> str:
    lower = path.lower()
    for needle, label in ZIP_LABELS.items():
        if needle in lower:
            return label
    return Path(path).name
