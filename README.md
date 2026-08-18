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
| St. Joseph Section 1939 (plot book) | 1939–1980s | **complete** — 475 entries, pages 17–79 |
| St. Joseph 1939 name index | — | **complete** — 148 name→page pointers |
| Cemetery Plots 1847 | ~1847–1890s | **complete** — 2,463 entries |
| Reception Into Full Communion | 2009–2012 | **complete** — 5 entries (the whole book) |
| Baptism 1839–1875 | 1839–1875 | **complete** — 2,514 baptisms |
| Marriage 1840–1871 | 1840–1871 | **complete** — 612 marriages |
| First Communion 1895–1941 | 1895–1941 | **complete** — 2,377 communicants |
| Record of Cemetery 1854–1870 | 1854–1870 | **complete** — 686 burials |
| Record of Interments 1847–54 | 1847–1854 | **complete** — 225 burials (pages 2–62; later pages are accounts) |
| Sick Call Register | 1973–2006 | **complete** — 3,213 visits + index |
| Confirmation 2015– | 2015–2019 | **complete** — 756 confirmations + index (all Drive scans; pages 4 and 15 were never on Drive) |
| Confirmation 1991–2014 | 1991–2014 | **complete** — 3,763 confirmations (all assigned scans) |
| Marriage 1872–1907 | 1872–1908 | **complete** — 456 marriages (all 65 scans) |
| Marriage 2009– | 2009–2010 | in progress — first page (9 marriages) |
| Baptism 1989–2011 | 1989–2011 | **complete** — 2,015 baptisms (all assigned scans) |
| First Communion 1953–1961 | 1953–1961 | **complete** — 3,749 communicants (all assigned scans) |
| Death 1990–2001 | 1990–2001 | **complete** — 2,327 deaths + index (all 75 scans) |
| Death 2001–2018 | 2001–2018 | **complete** — 2,605 deaths + index (all 62 scans) |
| Confirmation 1942–1952 | 1942–1952 | pending — on Drive (transcribing) |
| Death 1895–1899 | 1895–1899 | **complete** — 346 deaths + index (all 26 scans) |
| Death Registers name index | — | **complete** — 2,125 name→page pointers (all 30 letter-tab scans) |
| Marriage 1908–1936 | 1908–1936 | pending — on Drive (transcribing) |
| Marriage 1937–1963 | 1946 fragment | **complete for Drive scans** — 20 marriages (PAGE 58, 60) |
| Confirmation 1895–1944 | 1895–1944 | **complete for Drive scans** — year/page index (PAGE 000) |
| Confirmation 1974–1990 folder | 1923 | **complete for Drive scans** — 10 baptisms (PAGE 164 is a misfiled 1923 baptism leaf) |
| Death C 1924–1964 | 1948–1949 fragment | **complete for Drive scans** — 9 burials (PAGE 46) |
| Death Section E | ~1929–1970s | **complete** — 552 burials + index (all 33 scans) |
| Baptism 2011– | 2016–2019 fragment | **complete for Drive scans** — 20 baptisms + name indexes (5 scans) |
| Baptism 1965–1972 | 1965–1972 | in progress — 250 name-index entries (tabs A, F, K, L; remaining tabs still on Drive) |
| First Communion 1962–1970 | ~1962–1964 | in progress — 92 name-index entries (PAGE R2-S; PAGE X-Y still on Drive) |

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
