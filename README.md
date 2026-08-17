# Saint Peter's Registers Digitalization

Digitization of Saint Peter's church records: scanned register images are
transcribed into structured CSV files that can be searched by name, year,
register type, and other fields.

## How it works

1. **Download** — `scripts/download_drive.py` pulls the scanned register
   images from the shared Google Drive folder.
2. **Transcribe** — each register page is transcribed into rows of a CSV.
   Old handwritten registers require vision-model transcription (not plain
   OCR); uncertain readings are flagged in a `needs_review` column instead
   of being silently guessed.
3. **Store** — one CSV per register under `transcriptions/`, with a schema
   suited to that register type (see `docs/schemas.md`).
4. **Query** — `scripts/query.py` searches across all transcribed CSVs by
   name, year, register type, etc.

## Registers

| Register | Date range | Status |
|---|---|---|
| St. Joseph Section (cemetery plots) | 1939– | sample transcribed |
| Baptism 1839–1875 / Marriage 1840–1871 | 1839–1875 | pending |
| Baptism Registers | | pending |
| Cemetery Plots | | pending |
| Confirmation Registers | | pending |
| Death Registers | | pending |
| First Communion Registers | | pending |
| Marriage Registers | | pending |
| NEW 2023–2024 UPDATED | 2023–2024 | pending |
| Reception Into Full Communion | | pending |
| Record of Cemetery 1854–1870 | 1854–1870 | pending |
| Record of Interments 1847–54 | 1847–1854 | pending |
| Sick Call Register | 1973–2009 | pending |

## Searching the records

**Web interface** — the easiest way to browse. From the repo folder run:

```bash
python3 -m http.server 8000
```

then open [http://localhost:8000](http://localhost:8000) in a browser. Search
by name, year, and register. (The page can also be hosted for free on GitHub
Pages: repo Settings → Pages → deploy from the main branch root.)

**Command line:**

```bash
python3 scripts/query.py --name "Monaghan"
python3 scripts/query.py --year 1940
python3 scripts/query.py --register st_joseph_section_1939 --name "Cody"
```

**SQL (optional)** — the CSVs are the master copy, but you can build a
SQLite database from them at any time:

```bash
python3 scripts/export_sqlite.py
sqlite3 registers.db "SELECT * FROM records WHERE surname LIKE '%Cody%' AND year > '1950'"
```

New registers are added to the web UI by listing their CSV in
`transcriptions/manifest.json`.

## Setup

```bash
pip install -r requirements.txt
python3 scripts/download_drive.py   # downloads scans from Google Drive
```

## Review workflow

Every transcribed row carries a `needs_review` flag and a `source_image`
reference so a human reviewer can pull up the original scan and confirm
uncertain readings. The `St. Peter's Registers Logbook` in the Drive tracks
which registers have been reviewed.
