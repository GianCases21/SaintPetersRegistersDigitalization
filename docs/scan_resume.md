# Photographer resume guide

Where to stand in each physical register: the **latest date** and **last named
record** already in the database, the **last page photographed**, and where to
start taking pictures. Regenerated from the live CSVs:

```bash
python3 scripts/scan_resume.py
```

Shared Drive: https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj

## How to photograph and upload

1. Open the physical book to the last named record below. Confirm you are in
   the right volume, then start at the **next blank line / next page**.
2. Also shoot any **known missing pages** listed for that book.
3. Name files `PAGE 012.JPG` (or `PAGE 12-13.JPG` for a two-page spread),
   matching the names already used in that folder. Keep the spaces.
4. Upload **individual page images** into the existing book folder on Drive
   (or drop them in `incoming/<register_id>/` in this repo). Do **not** replace
   the whole register with a new zip — the website watcher cannot see a new
   page inside a 2 GB zip.
5. Skip title pages with no names, totals-only pages, and account/fee pages
   (put accounts in a subfolder named `_accounts` if you still want an archive
   photo).

New JPGs on Drive are picked up by `scripts/watch_drive.py` and, when a vision
API key is configured, transcribed into the website CSVs. See
[drive_ingest.md](drive_ingest.md).

## Start here

Priority is volumes that exist on the shelf but are missing most of their pages
on Drive, then known single-page holes.

1. **Baptism 1875–1903 / 1904–1921 fragments** — last in DB: Bogert, Francis (Apr 9 1898) on PAGE 358.JPG.
   Start: FRAGMENT. Photograph the rest of Baptism 1875–1903 and Baptism 1904–1921. Already on Drive: PAGE I, 008, 014, 061, 358. Do not redo those five. PAGE 358 is an 1898 leaf of the 1875–1903 book (last named: Bogert, Francis, 9 Apr 1898). PAGE 061 is a 1916 leaf of the 1904–1921 book (last named: Oldham, William, 21 May 1916).

2. **Marriage 1937–1963 (fragment)** — last in DB: John Aloysius Collumb & Elizabeth Delaney Gartland (Dec 30 1946) on PAGE 60.JPG.
   Start: FRAGMENT. Photograph the whole 1937–1963 marriage book. Drive only has PAGE 58 and PAGE 60. Fill PAGE 59 and every page before 58 and after 60. After Collumb & Gartland (30 Dec 1946, end of 1946 on page 60), continue with the first 1947 marriage.

3. **Death C 1924–1964 (fragment)** — last in DB: Flynn, Baby Girl (1949) on PAGE 46.JPG.
   Start: FRAGMENT. Only PAGE 46 is on Drive. Photograph the rest of Death C 1924–1964.

4. **Confirmation 1895–1944 (year index)** — last in DB: index/tabs only (—) on PAGE 000.JPG.
   Start: FRAGMENT — year/page index only (PAGE 000). Photograph the actual class lists of Confirmation 1895–1944.

5. **Confirmation 1957–1964 (fragment)** — last in DB: Li Mandri, Richard (Jun 7 1964) on PAGE 99.JPG.
   Start: FRAGMENT. Drive only has PAGE 96, PAGE 99, and letter tabs. Photograph the rest of Confirmation 1957–1964, including pages 97–98.

6. **Confirmation 1974–1990 folder (1923 baptism page)** — last in DB: O'Toole, Hugh (Oct 21 1923) on PAGE 164.JPG.
   Start: The Drive folder currently holds a misfiled 1923 baptism leaf (PAGE 164), not the 1974–1990 confirmation book. Photograph the real confirmation volume from the beginning.

7. **First Communion 1962–1970 (index)** — last in DB: index/tabs only (—) on PAGE R2-S.JPG, PAGE X-Y.JPG.
   Start: FRAGMENT — two index scans only (R2–S and X–Y). Photograph the actual class pages of First Communion 1962–1970.

8. **First Communion 2014–** — no scans on Drive yet.
   Start: The Drive folder for this book was empty. If the volume is on the shelf, photograph from the first named class (usually page 1) using PAGE 001.JPG naming, and upload into a folder named `First Communion 2014-` (or `incoming/first_communion_2014/`).

9. **Baptism 2011– (fragment)** — last in DB: Hernandez, Gianna Marie (Apr 20 2019) on PAGE 067.JPG.
   Start: FRAGMENT of the current baptism book. Drive only has PAGE 046, PAGE 067, and three index tabs. Photograph pages 1–45, 47–66, and 68 to the end. On page 46 the last named child is Moncayo, Ariana (23 Jul 2016). On page 67 the last named child is Hernandez, Gianna Marie (20 Apr 2019, entry 15) — continue from the next blank line / page 68.

10. **Baptism 1965–1972 (name index)** — last in DB: index/tabs only (—) on PAGE A.JPG, PAGE F.JPG, PAGE K.JPG….
   Start: FRAGMENT — letter-tab name index only. Photograph the actual baptism pages of the 1965–1972 book (and any missing letter tabs).

11. **Death SECTION D (cemetery plots fragment)** — last in DB: LUKOWIAK, JAMES (Dec 22 1973) on PAGE 102-103.JPG.
   Start: FRAGMENT. Five cemetery-plot scans only. Photograph the rest of Death SECTION D.

12. **Confirmation 2015–** — last in DB: YEYE, JUSTIN RAFAEL (Jun 14 2019) on PAGE 21.JPG.
   Start: Re-shoot pages 4 and 15 (never on Drive). Then continue the current book after Yeye, Justin Rafael (14 Jun 2019, page 21, entry 59).

13. **Marriage 2009–** — last in DB: JORGE IVAN VELASQUEZ GARCIA & CLAUDIA INES VARGAS PIEROTTI (Oct 19 2019) on PAGE 23.JPG.
   Start: Re-shoot page 18 if it has marriages (never uploaded). Then continue the current book after Velasquez Garcia & Vargas Pierotti on page 23 (19 Oct 2019, entry 13).

## Every register

Latest date / last record are taken from the **last named entry on the highest
numbered record page** (not the name index). Cemetery plot books are
photographed by page, not by burial date.

| Register | Status | Latest date | Last named record | Last page | Known holes |
|---|---|---|---|---|---|
| St. Joseph Section 1939 | complete for Drive | Feb 21 1964 | Faltraco, Alexander | PAGE 078-079.JPG | page 67 |
| St. Joseph 1939 Name Index | complete for Drive | — | (index only) | INDEX AB.JPG, INDEX CD.JPG, INDEX EF-GH.JPG… | none known |
| Cemetery Plots 1847 | complete for Drive | Mar 16 1964 | Burke, Mrs. Mary D. | PAGE 244-245.JPG | none known |
| Reception Into Full Communion | complete for Drive | Apr 7 2012 | May, McKenzie | PAGE 001.JPG | none known |
| Record of Interments 1847–54 | complete for Drive | Mar 12 1854 | Costello, Ellen B | PAGE 062.JPG | none known |
| Record of Cemetery 1854–1870 | complete for Drive | Dec 14 1870 | Black, Julian Theodorus | PAGE 054.JPG | page 17 |
| Baptism 1839–1875 | complete for Drive | Mar 17 1875 | Early, John | PAGE 133.JPG | none known |
| Marriage 1840–1871 | complete for Drive | Dec 31 1871 | Felix McKenna & Mary Burns | PAGE 086.JPG | none known |
| First Communion 1895–1941 | complete for Drive | 1941 | Silkowski, Lillian | PAGE 262.JPG | none known |
| Sick Call Register 1973–2006 | complete for Drive | Mar 24 2006 | Majewski(?), Sophie | PAGE 103.JPG | none known |
| Confirmation 2015– | complete for Drive | Jun 14 2019 | YEYE, JUSTIN RAFAEL | PAGE 21.JPG | page 4, page 15 |
| Confirmation 1991–2014 | complete for Drive | Jun 8 2014 | Moreno, Gonzalo | PAGE 103.JPG | none known |
| Baptism 1989–2011 | complete for Drive | Oct 2 2010 | Navarro, Ava | PAGE 199.JPG | none known |
| First Communion 1953–1961 | complete for Drive | Oct 22 1961 | Meyer, Margaret Lillian | PAGE 109.JPG | none known |
| Death 2001–2018 | complete for Drive | Apr 2 2018 | Fragapane, Damian | PAGE 51.JPG | none known |
| Death 1990–2001 | complete for Drive | Jul 28 2001 | PALUMBO, DOROTHY | PAGE 50.JPG | none known |
| Marriage 1872–1907 | complete for Drive | Jan 29 1908 | Augustus Barber & Matilda Zeigler | PAGE 114-115.JPG | none known |
| Marriage 2009– | complete for Drive | Oct 19 2019 | JORGE IVAN VELASQUEZ GARCIA & CLAUDIA INES VARGAS PIEROTTI | PAGE 23.JPG | page 18 |
| Marriage 1937–1963 (fragment) | fragment | Dec 30 1946 | John Aloysius Collumb & Elizabeth Delaney Gartland | PAGE 60.JPG | page 59 |
| Confirmation 1895–1944 (year index) | fragment | — | (index only) | PAGE 000.JPG | photograph everything except PAGE 000.JPG |
| Confirmation 1974–1990 folder (1923 baptism page) | fragment | Oct 21 1923 | O'Toole, Hugh | PAGE 164.JPG | photograph everything except 164 |
| Death C 1924–1964 (fragment) | fragment | 1949 | Flynn, Baby Girl | PAGE 46.JPG | photograph everything except 46 |
| Baptism 2011– (fragment) | fragment | Apr 20 2019 | Hernandez, Gianna Marie | PAGE 067.JPG | photograph everything except 46, 67 |
| Baptism 1965–1972 (name index) | fragment | — | (index only) | PAGE A.JPG, PAGE F.JPG, PAGE K.JPG… | photograph everything except PAGE A.JPG, PAGE F.JPG, PAGE K.JPG, PAGE L.JPG, PAGE Mc.JPG, PAGE N.JPG, PAGE P2.JPG, PAGE Q.JPG, PAGE S.JPG, PAGE S2.JPG, PAGE V.JPG, PAGE W.JPG, PAGE X.JPG, PAGE Y.JPG, PAGE Z.JPG |
| First Communion 1962–1970 (index) | fragment | — | (index only) | PAGE R2-S.JPG, PAGE X-Y.JPG | photograph everything except PAGE R2-S.JPG, PAGE X-Y.JPG |
| Death Section E (cemetery tiers) | complete for Drive | Jan 2 1980 | Cammarata, Louise | PAGE 40-41.JPG | none known |
| Death Registers name index | complete for Drive | — | (index only) | PAGE A.JPG, PAGE B.JPG, PAGE B2.JPG… | none known |
| Death 1895–1899 | complete for Drive | Feb 26 1899 | McIntyre, John | PAGE 7.JPG | none known |
| Confirmation 1957–1964 (fragment) | fragment | Jun 7 1964 | Li Mandri, Richard | PAGE 99.JPG | page 97, page 98 |
| Marriage 1908–1936 | complete for Drive | Dec 13 1936 | Andrew Colannino & Anne Catherine Mistrario | PAGE 84.JPG | none known |
| Confirmation / First Communion 1942–1952 | complete for Drive | May 24 1953 | McNick, John J. | PAGE 92-93.JPG | none known |
| Death SECTION D (cemetery plots fragment) | fragment | Dec 22 1973 | LUKOWIAK, JAMES | PAGE 102-103.JPG | photograph everything except 90, 91, 94, 95, 96, 97, 102, 103 |
| Baptism 1875–1903 / 1904–1921 fragments | fragment | Apr 9 1898 | Bogert, Francis | PAGE 358.JPG | photograph everything except 8, 14, 61, 358 |
| Confirmation 1854–1875 (in Baptism 1839 book) | complete for Drive | Jul 2 1854 | Hogan, Daniel | PAGE 147.JPG | none known |
| Funerals 1868 (in Baptism 1839 book) | complete for Drive | Jul 16 1868 | Healy, Mrs | PAGE 134.JPG | none known |
| Marriage 1840–1871 name index | complete for Drive | — | (index only) | PAGE A.JPG, PAGE F.JPG, PAGE H.JPG… | none known |
| First Communion 2014– | not on Drive | — | — | none | photograph from the start |

## Details

### St. Joseph Section 1939

- **Register id:** `st_joseph_section_1939` (folder name for `incoming/st_joseph_section_1939/`)
- **Status:** complete for Drive
- **Records in the website:** 465 named entries + 10 index rows, from 32 scan(s)
- **Last named record:** Faltraco, Alexander — Feb 21 1964
- **Last page on Drive:** PAGE 078-079.JPG
- **Known missing pages:** 67
- **Start photographing:** Plot book pages 17–79 are on Drive. Re-shoot page 67 if that leaf has graves (we have 66 then 68–69). Book ends at page 79.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/st_joseph_section_1939/PAGE ….JPG`.

### St. Joseph 1939 Name Index

- **Register id:** `st_joseph_section_1939_index` (folder name for `incoming/st_joseph_section_1939_index/`)
- **Status:** complete for Drive
- **Records in the website:** 0 named entries + 148 index rows, from 7 scan(s)
- **Last named record:** none (index/tabs only)
- **Last page on Drive:** INDEX AB.JPG, INDEX CD.JPG, INDEX EF-GH.JPG…
- **Start photographing:** Front-of-book name index is complete (tabs AB through UV).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/st_joseph_section_1939_index/PAGE ….JPG`.

### Cemetery Plots 1847

- **Register id:** `cemetery_plots_1847` (folder name for `incoming/cemetery_plots_1847/`)
- **Status:** complete for Drive
- **Records in the website:** 2,463 named entries, from 110 scan(s)
- **Last named record:** Burke, Mrs. Mary D. — Mar 16 1964
- **Last page on Drive:** PAGE 244-245.JPG
- **Start photographing:** Complete for named plot pages on Drive. Blank/numbered-only pages (70, 79–81, 86–87, 92, 97, 149, 159, 179, and similar) do not need re-shooting.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/cemetery_plots_1847/PAGE ….JPG`.

### Reception Into Full Communion

- **Register id:** `reception_full_communion` (folder name for `incoming/reception_full_communion/`)
- **Status:** complete for Drive
- **Records in the website:** 5 named entries, from 1 scan(s)
- **Last named record:** May, McKenzie — Apr 7 2012
- **Last page on Drive:** PAGE 001.JPG
- **Start photographing:** Whole book (5 people on PAGE 001). Title page has no names. Only photograph if new receptions were added after McKenzie May (7 Apr 2012).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/reception_full_communion/PAGE ….JPG`.

### Record of Interments 1847–54

- **Register id:** `interments_1847` (folder name for `incoming/interments_1847/`)
- **Status:** complete for Drive
- **Records in the website:** 225 named entries, from 61 scan(s)
- **Last named record:** Costello, Ellen B — Mar 12 1854
- **Last page on Drive:** PAGE 062.JPG
- **Start photographing:** Burial pages 2–62 are complete. Later pages are church accounts — skip or put them in `_accounts`. Do not enter accounts as burials.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/interments_1847/PAGE ….JPG`.

### Record of Cemetery 1854–1870

- **Register id:** `cemetery_1854` (folder name for `incoming/cemetery_1854/`)
- **Status:** complete for Drive
- **Records in the website:** 686 named entries, from 53 scan(s)
- **Last named record:** Black, Julian Theodorus — Dec 14 1870
- **Last page on Drive:** PAGE 054.JPG
- **Known missing pages:** 17
- **Start photographing:** Complete for Drive through December 1870. Re-shoot page 17 if it has named burials (no rows in the CSV).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/cemetery_1854/PAGE ….JPG`.

### Baptism 1839–1875

- **Register id:** `baptism_1839` (folder name for `incoming/baptism_1839/`)
- **Status:** complete for Drive
- **Records in the website:** 2,514 named entries, from 133 scan(s)
- **Last named record:** Early, John — Mar 17 1875
- **Last page on Drive:** PAGE 133.JPG
- **Start photographing:** This baptism volume is finished on Drive through the last baptism. Page 133 notes “See new Registry” and the rest of the page is blank. Do not reshoot 1–133. Pages 134–147 are funerals/confirmations (already transcribed). Skip account pages after that. Start the next baptisms in Baptism 1875–1903.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/baptism_1839/PAGE ….JPG`.

### Marriage 1840–1871

- **Register id:** `marriage_1840` (folder name for `incoming/marriage_1840/`)
- **Status:** complete for Drive
- **Records in the website:** 613 named entries, from 46 scan(s)
- **Last named record:** Felix McKenna & Mary Burns — Dec 31 1871
- **Last page on Drive:** PAGE 086.JPG
- **Start photographing:** This marriage book is complete on Drive through the 31 Dec 1871 note to see the next registry. Do not reshoot pages 57–58 or 73–74 (overlapping photos; we kept the clearer 59–60 and 75–76 scans). Continue marriages in Marriage 1872–1907.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/marriage_1840/PAGE ….JPG`.

### First Communion 1895–1941

- **Register id:** `first_communion_1895` (folder name for `incoming/first_communion_1895/`)
- **Status:** complete for Drive
- **Records in the website:** 2,336 named entries + 41 index rows, from 78 scan(s)
- **Last named record:** Silkowski, Lillian — 1941
- **Last page on Drive:** PAGE 262.JPG
- **Start photographing:** Complete for named pages on Drive. PAGE 183 is totals only — skip. Large unused numbered stretches are blank class pages, not missing people.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/first_communion_1895/PAGE ….JPG`.

### Sick Call Register 1973–2006

- **Register id:** `sick_call_1973` (folder name for `incoming/sick_call_1973/`)
- **Status:** complete for Drive
- **Records in the website:** 3,213 named entries, from 115 scan(s)
- **Last named record:** Majewski(?), Sophie — Mar 24 2006
- **Last page on Drive:** PAGE 103.JPG
- **Start photographing:** Complete for Drive through March 2006. If the book continues after page 103, photograph from the next visit.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/sick_call_1973/PAGE ….JPG`.

### Confirmation 2015–

- **Register id:** `confirmation_2015` (folder name for `incoming/confirmation_2015/`)
- **Status:** complete for Drive
- **Records in the website:** 363 named entries + 393 index rows, from 30 scan(s)
- **Last named record:** YEYE, JUSTIN RAFAEL — Jun 14 2019
- **Last page on Drive:** PAGE 21.JPG
- **Known missing pages:** 4, 15
- **Start photographing:** Re-shoot pages 4 and 15 (never on Drive). Then continue the current book after Yeye, Justin Rafael (14 Jun 2019, page 21, entry 59).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/confirmation_2015/PAGE ….JPG`.

### Confirmation 1991–2014

- **Register id:** `confirmation_1991` (folder name for `incoming/confirmation_1991/`)
- **Status:** complete for Drive
- **Records in the website:** 1,739 named entries + 2,024 index rows, from 111 scan(s)
- **Last named record:** Moreno, Gonzalo — Jun 8 2014
- **Last page on Drive:** PAGE 103.JPG
- **Start photographing:** Complete for Drive through page 103. Continue later confirmations in Confirmation 2015–.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/confirmation_1991/PAGE ….JPG`.

### Baptism 1989–2011

- **Register id:** `baptism_1989` (folder name for `incoming/baptism_1989/`)
- **Status:** complete for Drive
- **Records in the website:** 1,641 named entries + 374 index rows, from 177 scan(s)
- **Last named record:** Navarro, Ava — Oct 2 2010
- **Last page on Drive:** PAGE 199.JPG
- **Start photographing:** Complete for Drive through page 199. Continue later baptisms in Baptism 2011– (still a fragment).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/baptism_1989/PAGE ….JPG`.

### First Communion 1953–1961

- **Register id:** `first_communion_1953` (folder name for `incoming/first_communion_1953/`)
- **Status:** complete for Drive
- **Records in the website:** 1,725 named entries + 2,024 index rows, from 121 scan(s)
- **Last named record:** Meyer, Margaret Lillian — Oct 22 1961
- **Last page on Drive:** PAGE 109.JPG
- **Start photographing:** Complete for Drive. Continue later first communions in the 1962–1970 book (still a fragment) and 2014– (not on Drive).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/first_communion_1953/PAGE ….JPG`.

### Death 2001–2018

- **Register id:** `death_2001` (folder name for `incoming/death_2001/`)
- **Status:** complete for Drive
- **Records in the website:** 1,359 named entries + 1,246 index rows, from 62 scan(s)
- **Last named record:** Fragapane, Damian — Apr 2 2018
- **Last page on Drive:** PAGE 51.JPG
- **Start photographing:** Complete for Drive through April 2018. If the physical book continues after Fragapane, Damian (page 51), photograph from the next entry.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/death_2001/PAGE ….JPG`.

### Death 1990–2001

- **Register id:** `death_1990` (folder name for `incoming/death_1990/`)
- **Status:** complete for Drive
- **Records in the website:** 1,163 named entries + 1,164 index rows, from 75 scan(s)
- **Last named record:** PALUMBO, DOROTHY — Jul 28 2001
- **Last page on Drive:** PAGE 50.JPG
- **Start photographing:** Complete for Drive. Continue later deaths in Death 2001–2018.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/death_1990/PAGE ….JPG`.

### Marriage 1872–1907

- **Register id:** `marriage_1872` (folder name for `incoming/marriage_1872/`)
- **Status:** complete for Drive
- **Records in the website:** 440 named entries + 16 index rows, from 65 scan(s)
- **Last named record:** Augustus Barber & Matilda Zeigler — Jan 29 1908
- **Last page on Drive:** PAGE 114-115.JPG
- **Start photographing:** Complete for Drive through the last page. Continue later marriages in Marriage 1908–1936.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/marriage_1872/PAGE ….JPG`.

### Marriage 2009–

- **Register id:** `marriage_2009` (folder name for `incoming/marriage_2009/`)
- **Status:** complete for Drive
- **Records in the website:** 200 named entries + 398 index rows, from 37 scan(s)
- **Last named record:** JORGE IVAN VELASQUEZ GARCIA & CLAUDIA INES VARGAS PIEROTTI — Oct 19 2019
- **Last page on Drive:** PAGE 23.JPG
- **Known missing pages:** 18
- **Start photographing:** Re-shoot page 18 if it has marriages (never uploaded). Then continue the current book after Velasquez Garcia & Vargas Pierotti on page 23 (19 Oct 2019, entry 13).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/marriage_2009/PAGE ….JPG`.

### Marriage 1937–1963 (fragment)

- **Register id:** `marriage_1937` (folder name for `incoming/marriage_1937/`)
- **Status:** fragment
- **Records in the website:** 20 named entries, from 2 scan(s)
- **Last named record:** John Aloysius Collumb & Elizabeth Delaney Gartland — Dec 30 1946
- **Last page on Drive:** PAGE 60.JPG
- **Known missing pages:** 59
- **Already photographed (do not redo):** `PAGE 58.JPG`, `PAGE 60.JPG`
- **Start photographing:** FRAGMENT. Photograph the whole 1937–1963 marriage book. Drive only has PAGE 58 and PAGE 60. Fill PAGE 59 and every page before 58 and after 60. After Collumb & Gartland (30 Dec 1946, end of 1946 on page 60), continue with the first 1947 marriage.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/marriage_1937/PAGE ….JPG`.

### Confirmation 1895–1944 (year index)

- **Register id:** `confirmation_1895` (folder name for `incoming/confirmation_1895/`)
- **Status:** fragment
- **Records in the website:** 0 named entries + 40 index rows, from 1 scan(s)
- **Last named record:** none (index/tabs only)
- **Last page on Drive:** PAGE 000.JPG
- **Already photographed (do not redo):** `PAGE 000.JPG`
- **Start photographing:** FRAGMENT — year/page index only (PAGE 000). Photograph the actual class lists of Confirmation 1895–1944.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/confirmation_1895/PAGE ….JPG`.

### Confirmation 1974–1990 folder (1923 baptism page)

- **Register id:** `confirmation_1974` (folder name for `incoming/confirmation_1974/`)
- **Status:** fragment
- **Records in the website:** 10 named entries, from 1 scan(s)
- **Last named record:** O'Toole, Hugh — Oct 21 1923
- **Last page on Drive:** PAGE 164.JPG
- **Already photographed (do not redo):** `PAGE 164.JPG`
- **Start photographing:** The Drive folder currently holds a misfiled 1923 baptism leaf (PAGE 164), not the 1974–1990 confirmation book. Photograph the real confirmation volume from the beginning.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/confirmation_1974/PAGE ….JPG`.

### Death C 1924–1964 (fragment)

- **Register id:** `death_c_1924` (folder name for `incoming/death_c_1924/`)
- **Status:** fragment
- **Records in the website:** 9 named entries, from 1 scan(s)
- **Last named record:** Flynn, Baby Girl — 1949
- **Last page on Drive:** PAGE 46.JPG
- **Already photographed (do not redo):** `PAGE 46.JPG`
- **Start photographing:** FRAGMENT. Only PAGE 46 is on Drive. Photograph the rest of Death C 1924–1964.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/death_c_1924/PAGE ….JPG`.

### Baptism 2011– (fragment)

- **Register id:** `baptism_2011` (folder name for `incoming/baptism_2011/`)
- **Status:** fragment
- **Records in the website:** 20 named entries + 194 index rows, from 5 scan(s)
- **Last named record:** Hernandez, Gianna Marie — Apr 20 2019
- **Last page on Drive:** PAGE 067.JPG
- **Already photographed (do not redo):** `INDEX CD2-EF.JPG`, `INDEX MN2-OP.JPG`, `INDEX QR.JPG`, `PAGE 046.JPG`, `PAGE 067.JPG`
- **Start photographing:** FRAGMENT of the current baptism book. Drive only has PAGE 046, PAGE 067, and three index tabs. Photograph pages 1–45, 47–66, and 68 to the end. On page 46 the last named child is Moncayo, Ariana (23 Jul 2016). On page 67 the last named child is Hernandez, Gianna Marie (20 Apr 2019, entry 15) — continue from the next blank line / page 68.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/baptism_2011/PAGE ….JPG`.

### Baptism 1965–1972 (name index)

- **Register id:** `baptism_1965` (folder name for `incoming/baptism_1965/`)
- **Status:** fragment
- **Records in the website:** 0 named entries + 621 index rows, from 15 scan(s)
- **Last named record:** none (index/tabs only)
- **Last page on Drive:** PAGE A.JPG, PAGE F.JPG, PAGE K.JPG…
- **Already photographed (do not redo):** `PAGE A.JPG`, `PAGE F.JPG`, `PAGE K.JPG`, `PAGE L.JPG`, `PAGE Mc.JPG`, `PAGE N.JPG`, `PAGE P2.JPG`, `PAGE Q.JPG`, `PAGE S.JPG`, `PAGE S2.JPG`, `PAGE V.JPG`, `PAGE W.JPG`, `PAGE X.JPG`, `PAGE Y.JPG`, `PAGE Z.JPG`
- **Start photographing:** FRAGMENT — letter-tab name index only. Photograph the actual baptism pages of the 1965–1972 book (and any missing letter tabs).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/baptism_1965/PAGE ….JPG`.

### First Communion 1962–1970 (index)

- **Register id:** `first_communion_1962` (folder name for `incoming/first_communion_1962/`)
- **Status:** fragment
- **Records in the website:** 0 named entries + 168 index rows, from 2 scan(s)
- **Last named record:** none (index/tabs only)
- **Last page on Drive:** PAGE R2-S.JPG, PAGE X-Y.JPG
- **Already photographed (do not redo):** `PAGE R2-S.JPG`, `PAGE X-Y.JPG`
- **Start photographing:** FRAGMENT — two index scans only (R2–S and X–Y). Photograph the actual class pages of First Communion 1962–1970.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/first_communion_1962/PAGE ….JPG`.

### Death Section E (cemetery tiers)

- **Register id:** `death_section_e` (folder name for `incoming/death_section_e/`)
- **Status:** complete for Drive
- **Records in the website:** 419 named entries + 133 index rows, from 33 scan(s)
- **Last named record:** Cammarata, Louise — Jan 2 1980
- **Last page on Drive:** PAGE 40-41.JPG
- **Start photographing:** Complete for Drive scans of this cemetery tier book.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/death_section_e/PAGE ….JPG`.

### Death Registers name index

- **Register id:** `death_index` (folder name for `incoming/death_index/`)
- **Status:** complete for Drive
- **Records in the website:** 0 named entries + 2,125 index rows, from 30 scan(s)
- **Last named record:** none (index/tabs only)
- **Last page on Drive:** PAGE A.JPG, PAGE B.JPG, PAGE B2.JPG…
- **Start photographing:** Letter-tab death index (30 scans). Photograph any missing tabs.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/death_index/PAGE ….JPG`.

### Death 1895–1899

- **Register id:** `death_1895` (folder name for `incoming/death_1895/`)
- **Status:** complete for Drive
- **Records in the website:** 154 named entries + 192 index rows, from 26 scan(s)
- **Last named record:** McIntyre, John — Feb 26 1899
- **Last page on Drive:** PAGE 7.JPG
- **Start photographing:** Complete for Drive. Later deaths are in the 20th-century death books.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/death_1895/PAGE ….JPG`.

### Confirmation 1957–1964 (fragment)

- **Register id:** `confirmation_1957` (folder name for `incoming/confirmation_1957/`)
- **Status:** fragment
- **Records in the website:** 38 named entries + 911 index rows, from 16 scan(s)
- **Last named record:** Li Mandri, Richard — Jun 7 1964
- **Last page on Drive:** PAGE 99.JPG
- **Known missing pages:** 97, 98
- **Already photographed (do not redo):** `PAGE 96.JPG`, `PAGE 99.JPG`, `PAGE FG.JPG`, `PAGE HI.JPG`, `PAGE L.JPG`, `PAGE LM.JPG`, `PAGE M.JPG`, `PAGE N.JPG`, `PAGE P.JPG`, `PAGE RS.JPG`, `PAGE S.JPG`, `PAGE ST.JPG`, `PAGE TU.JPG`, `PAGE V.JPG`, `PAGE W.JPG`, `PAGE Y.JPG`
- **Start photographing:** FRAGMENT. Drive only has PAGE 96, PAGE 99, and letter tabs. Photograph the rest of Confirmation 1957–1964, including pages 97–98.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/confirmation_1957/PAGE ….JPG`.

### Marriage 1908–1936

- **Register id:** `marriage_1908` (folder name for `incoming/marriage_1908/`)
- **Status:** complete for Drive
- **Records in the website:** 802 named entries, from 72 scan(s)
- **Last named record:** Andrew Colannino & Anne Catherine Mistrario — Dec 13 1936
- **Last page on Drive:** PAGE 84.JPG
- **Start photographing:** Complete for the scans on Drive. Continue later marriages in Marriage 1937–1963 (that book is still a fragment).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/marriage_1908/PAGE ….JPG`.

### Confirmation / First Communion 1942–1952

- **Register id:** `confirmation_1942` (folder name for `incoming/confirmation_1942/`)
- **Status:** complete for Drive
- **Records in the website:** 1,852 named entries, from 45 scan(s)
- **Last named record:** McNick, John J. — May 24 1953
- **Last page on Drive:** PAGE 92-93.JPG
- **Start photographing:** Complete for named pages on Drive. Title page has no names — skip it.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/confirmation_1942/PAGE ….JPG`.

### Death SECTION D (cemetery plots fragment)

- **Register id:** `death_section_d` (folder name for `incoming/death_section_d/`)
- **Status:** fragment
- **Records in the website:** 56 named entries + 105 index rows, from 5 scan(s)
- **Last named record:** LUKOWIAK, JAMES — Dec 22 1973
- **Last page on Drive:** PAGE 102-103.JPG
- **Already photographed (do not redo):** `INDEX B-C.JPG`, `PAGE 090-091.JPG`, `PAGE 094-095.JPG`, `PAGE 096-097.JPG`, `PAGE 102-103.JPG`
- **Start photographing:** FRAGMENT. Five cemetery-plot scans only. Photograph the rest of Death SECTION D.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/death_section_d/PAGE ….JPG`.

### Baptism 1875–1903 / 1904–1921 fragments

- **Register id:** `baptism_fragments` (folder name for `incoming/baptism_fragments/`)
- **Status:** fragment
- **Records in the website:** 59 named entries + 6 index rows, from 5 scan(s)
- **Last named record:** Bogert, Francis — Apr 9 1898
- **Last page on Drive:** PAGE 358.JPG
- **Already photographed (do not redo):** `PAGE 008.JPG`, `PAGE 014.JPG`, `PAGE 061.JPG`, `PAGE 358.JPG`, `PAGE I.JPG`
- **Start photographing:** FRAGMENT. Photograph the rest of Baptism 1875–1903 and Baptism 1904–1921. Already on Drive: PAGE I, 008, 014, 061, 358. Do not redo those five. PAGE 358 is an 1898 leaf of the 1875–1903 book (last named: Bogert, Francis, 9 Apr 1898). PAGE 061 is a 1916 leaf of the 1904–1921 book (last named: Oldham, William, 21 May 1916).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/baptism_fragments/PAGE ….JPG`.

### Confirmation 1854–1875 (in Baptism 1839 book)

- **Register id:** `confirmation_early` (folder name for `incoming/confirmation_early/`)
- **Status:** complete for Drive
- **Records in the website:** 911 named entries, from 13 scan(s)
- **Last named record:** Hogan, Daniel — Jul 2 1854
- **Last page on Drive:** PAGE 147.JPG
- **Start photographing:** Confirmation lists bound in the back of the 1839 baptism book (pages 135–147) are complete on Drive. Do not reshoot.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/confirmation_early/PAGE ….JPG`.

### Funerals 1868 (in Baptism 1839 book)

- **Register id:** `funerals_1868` (folder name for `incoming/funerals_1868/`)
- **Status:** complete for Drive
- **Records in the website:** 16 named entries, from 1 scan(s)
- **Last named record:** Healy, Mrs — Jul 16 1868
- **Last page on Drive:** PAGE 134.JPG
- **Start photographing:** The 1868 funerals leaf (baptism page 134 + attached slip) is complete. Do not reshoot.
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/funerals_1868/PAGE ….JPG`.

### Marriage 1840–1871 name index

- **Register id:** `marriage_1840_index` (folder name for `incoming/marriage_1840_index/`)
- **Status:** complete for Drive
- **Records in the website:** 0 named entries + 255 index rows, from 11 scan(s)
- **Last named record:** none (index/tabs only)
- **Last page on Drive:** PAGE A.JPG, PAGE F.JPG, PAGE H.JPG…
- **Start photographing:** Letter-tab index of the 1840–1871 marriage book. Photograph any tab that is missing from Drive (we have A, F, H, I, M, Mc2–N, P, R, V, W, Y).
- **Upload to:** the existing Drive folder for this book, as `PAGE ….JPG`, or `incoming/marriage_1840_index/PAGE ….JPG`.

## Books not yet in the database

### First Communion 2014–

- **Register id:** `first_communion_2014`
- **Status:** no scans on Drive / no CSV yet
- **Start photographing:** The Drive folder for this book was empty. If the volume is on the shelf, photograph from the first named class (usually page 1) using PAGE 001.JPG naming, and upload into a folder named `First Communion 2014-` (or `incoming/first_communion_2014/`).

## After the photos are on Drive

The ingest job lists the Drive folder, downloads new JPGs, transcribes them
when a vision API key is present, and merges new rows into `transcriptions/`
so the search website picks them up. Until that job is enabled on GitHub,
run locally:

```bash
python3 scripts/watch_drive.py --download-new incoming
python3 scripts/ingest_incoming.py
python3 scripts/scan_resume.py
```
