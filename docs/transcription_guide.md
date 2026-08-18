# Transcription guide for register scans

You are transcribing scanned pages of historical church cemetery registers
into CSV. Accuracy and completeness matter more than speed. NEVER invent or
guess silently: every uncertain reading must be visibly marked.

## Workflow per scan

1. Read the prepared crop images (`_L.jpg` = left page, `_R.jpg` = right page)
   with the Read tool.
2. If any text is too small or faint, make your own zoomed crop from the
   original scan and read that. Example:

```bash
python3 -c "
from PIL import Image, ImageEnhance
im = Image.open('/path/to/ORIGINAL.JPG')   # originals are 5184x3456
c = im.crop((X1, Y1, X2, Y2))              # coordinates in the ORIGINAL
c = ImageEnhance.Contrast(c).enhance(1.6)
c = ImageEnhance.Brightness(c).enhance(1.3)
c.thumbnail((1400, 1400))
c.save('/tmp/zoom.jpg', quality=90)
"
```

   The prepared crops were taken from the original like this: the left crop
   spans x = 4%..56% of the original width, the right crop x = 48%..99%,
   both full height, then resized to 1600 px wide. Multiply crop coordinates
   by (original_region_width / 1600) and add the region x-offset to convert
   back to original coordinates.
3. Transcribe EVERY entry on the page, top to bottom. Do not skip faint
   entries — transcribe what you can and mark the rest.
4. Append rows to your assigned part CSV.

## Conventions (apply to all registers)

- Uncertain reading: transcribe your best reading, append `(?)` to that
  field, and set `needs_review=yes` for the row.
- Completely illegible: write `[illegible]` in the field, `needs_review=yes`.
- Ditto marks (`"` or `do`) mean "same as the entry above": expand them to
  the actual value (e.g. repeat the surname), so every row is self-contained.
- Marginal notes, cross-outs, insertions: put them in `notes`.
- Blank page or page with no entries: no rows; mention it in your report.
- CSV fields containing commas or quotes must be double-quoted (standard CSV).
- `source_image` = the ORIGINAL scan filename, e.g. `PAGE 018-019.JPG`
  (with spaces, as in the original folder), so a reviewer can find the scan.
- Two-digit years are 1800s or 1900s depending on the register period noted
  in your assignment (e.g. `'50` in the 1847 book = 1850).
- Dates: normalize to `Mon D YYYY` (e.g. `Jul 7 1850`) in date columns.
  Keep the year also in the `year` column for searchability. If only a year
  is known, put just the year.

## Register formats

### St. Joseph Section 1939 (`st_joseph_section_1939`)

Cemetery plot book, pages headed `Tier No X`. Left margin column = grave
numbers (descending). A grave may show a plot owner line (often with
"N graves" noted) and one or more interred persons with age, vault/box,
undertaker surname (e.g. Kiernan, Caffrey), and death/burial dates.

CSV header:
```
register,source_image,page,tier,grave_no,plot_owner,surname,given_name,age,interment_type,undertaker,date_of_death,date_of_burial,year,needs_review,notes
```
One row per interred person. If a grave has only an owner/reservation and no
burial, write one row with `plot_owner` filled and a note `plot reserved; no
interment recorded`. `page` = printed page number in the book corner where
the entry appears. `interment_type` = `vault` or `box` when given.

### St. Joseph 1939 name index (`st_joseph_index`)

Front-of-book alphabetical index: name and the page number where that
person's record appears. Some index pages have two columns per page.

CSV header:
```
register,source_image,surname,given_name,page_no,needs_review,notes
```
`register` value: `st_joseph_section_1939_index`.

### Cemetery Plots 1847 book (`cemetery_plots_1847`)

Pages headed like `Old Ground Tier 2` or `New Ground Tier 5`. Columns:
date (2-digit year like `'50` + month + day), name, lot number. Entries are
grouped by lot; the lot number appears once and dittos follow. Two-digit
years are 1800s (book spans ~1847-1890s).

CSV header:
```
register,source_image,page,ground,tier,lot,burial_date,year,surname,given_name,needs_review,notes
```
One row per person. Carry the lot number down to every row in its group.
Expand surname dittos. `page` = printed page number of that book page.

### Reception Into Full Communion (`reception_full_communion`)

Printed modern register. Title page has no data rows. Record page columns:
No., Name, Date of Reception, Father / Mother's maiden name, Sponsor,
Priest, Date/Place/Minister of Baptism, Remarks.

CSV header:
```
register,source_image,page,entry_no,surname,given_name,date_of_reception,year,father,mother_maiden,sponsor,priest,baptism_date,baptism_place,baptism_minister,needs_review,notes
```
`register` value: `reception_full_communion`. Put marriage and confirmation
notes in `notes`.

### Record of Interments 1847–54 (`interments_1847`)

Narrative burial book, chronological. Each entry: date, name, age, burial
location relative to another grave, sometimes cause of death. PAGE 001 is
a subscription/account page (not burials). Title pages have a few stray
entries. Two-digit years are 1800s.

CSV header:
```
register,source_image,page,burial_date,year,surname,given_name,age,cause_of_death,burial_location,needs_review,notes
```
`register` value: `interments_1847`.

### Record of Cemetery 1854–1870 (`cemetery_1854`)

Continuation of the narrative burial book (starts Apr 1854). Each entry:
date, name, age, cause of death, nativity/residence, parents, burial
location (tier / relative to another grave), sometimes a cash fee.
Landscape scans are two-page spreads — transcribe BOTH pages.

CSV header:
```
register,source_image,page,burial_date,year,surname,given_name,age,cause_of_death,nativity,residence,parents,burial_location,fee,needs_review,notes
```
`register` value: `cemetery_1854`. Skip pure account lines.

### Baptism 1839–1875 (`baptism_1839`)

Chronological baptism entries (Latin early, then English). Typical fields:
date, child name (often with age or birth note), father, mother (maiden
when given), sponsors (`sp.` / Sponsores), officiant.

CSV header:
```
register,source_image,page,baptism_date,year,surname,given_name,age_or_birth,father,mother,sponsors,officiant,needs_review,notes
```
`register` value: `baptism_1839`. Source images are already single-page
portraits in the 2023–2024 updated folder (`PAGE 001.JPG` … `PAGE 149.JPG`).
Read the whole page; do not split left/right.

### Marriage 1840–1871 (`marriage_1840`)

Chronological marriages. Early entries Latin (`Matrimonio juncti sunt`),
later English (`Married X to Y`). Witnesses after the couple; priest signs.

CSV header:
```
register,source_image,page,marriage_date,year,groom_surname,groom_given,bride_surname,bride_given,witnesses,officiant,needs_review,notes
```
`register` value: `marriage_1840`. Landscape scans are two-page spreads
unless the filename is a single page (PAGE 1, PAGE 79–87).

### First Communion 1895–1941 (`first_communion_1895`)

Pages headed Communions + year. Columns: name, age. Portrait scans.

CSV header:
```
register,source_image,page,year,surname,given_name,age,needs_review,notes
```
`register` value: `first_communion_1895`. INDEX.JPG is a name index
(name + page); put page number in `notes` as `index page_no=N` and leave
`age` blank.

### Sick Call Register 1973–2006 (`sick_call_1973`)

Printed ledger. Left page: DATE, NAME, RESIDENCE, ministration ticks
(C'FES / COM. / VIAT.). Right page: more ticks (ANT'G / LAST B.), PRIEST,
REMARKS. One row per person (or couple listed as one visit). Expand dittos.
Letter-tab scans (PAGE AB.JPG etc.) are name indexes: surname, given_name,
page_no in notes.

CSV header:
```
register,source_image,page,call_date,year,surname,given_name,residence,confession,communion,viaticum,anointing,last_blessing,priest,needs_review,notes
```
`register` value: `sick_call_1973`. Ministration columns: `yes` if ticked,
else blank.

### Baptism 1989–2011 (`baptism_1989`)

Modern printed Baptismal Register, two-page spreads (~10 numbered entries
per spread). Left leaf: No., name + address, birth place/date, baptism
date, father / mother maiden. Right leaf: sponsors, priest, confirmation,
marriage remarks. Letter-tab scans (PAGE GH.JPG etc.) are name indexes.

CSV header:
```
register,source_image,page,entry_no,surname,given_name,residence,birth_date,birth_place,baptism_date,year,father,mother_maiden,sponsors,priest,confirmation,needs_review,notes
```
`register` value: `baptism_1989`. Put marriage notes in `notes`. Index
rows: leave dates blank; put the target page in `notes` as `index page_no=N`.

### Confirmation 1942–1952 (`confirmation_1942`)

Printed First Communion Register header; some spreads are confirmation
classes, others first communion. Columns typically: baptism date/place,
name, age, residence. Landscape scans are two-page spreads
(`PAGE 10-11.JPG`). Put the printed class date in `confirmation_date`
and note `event=first_communion` or `event=confirmation` in `notes`.

CSV header:
```
register,source_image,page,confirmation_date,year,entry_no,surname,given_name,age,baptism_date,baptism_place,father,mother,sponsor,residence,needs_review,notes
```
`register` value: `confirmation_1942`.

### Confirmation 1991–2014 (`confirmation_1991`)

Printed Confirmation Register, two-page spreads. Header has class date
and bishop/minister. Columns: No., surname + given, confirmation name,
age, baptism place/date, residence, father / mother maiden, sponsor.
Letter-tab scans are name indexes.

CSV header:
```
register,source_image,page,confirmation_date,year,entry_no,surname,given_name,confirmation_name,age,baptism_date,baptism_place,residence,father,mother,sponsor,minister,needs_review,notes
```
`register` value: `confirmation_1991`.

### Confirmation 2015– (`confirmation_2015`)

Same printed Confirmation Register format as 1991–2014.

CSV header: same as `confirmation_1991`.
`register` value: `confirmation_2015`.

### Death 1895–1899 (`death_1895`)

Landscape death ledger. Left leaf: name, residence, age, state of life,
date of death. Right leaf: cause, sacraments, doctor, undertaker,
cemetery, remarks. Expand cemetery/residence dittos. Letter-tab scans
are name indexes.

CSV header:
```
register,source_image,page,death_date,year,surname,given_name,age,residence,state_of_life,cause_of_death,sacraments,doctor,undertaker,cemetery,needs_review,notes
```
`register` value: `death_1895`.

### Death 1990–2001 (`death_1990`)

Printed death register, two-page spreads (~25 numbered rows). Left:
No., name, age, nearest relative, relative address. Right: death date,
sacraments, funeral priest, burial date/place, undertaker (Remarks).
Letter-tab scans are name indexes.

CSV header:
```
register,source_image,page,entry_no,surname,given_name,age,nearest_relative,relative_address,death_date,year,sacraments,priest,burial_date,cemetery,undertaker,needs_review,notes
```
`register` value: `death_1990`.

### Death 2001–2018 (`death_2001`)

Same printed death-register format as 1990–2001.

CSV header: same as `death_1990`.
`register` value: `death_2001`.

### Death Section E (`death_section_e`)

Later death/cemetery section, landscape spreads. Transcribe both leaves.
Use the death_1990 columns when they fit; put extra location/plot notes
in `notes`.

CSV header: same as `death_1990`.
`register` value: `death_section_e`.

### First Communion 1953–1961 (`first_communion_1953`)

Printed First Communion Register, two-page spreads. Header has class
date and priest. Columns: No., name, birth place/date, age, baptism
place/date, residence, parents, remarks (school grade / convert notes).
Letter-tab scans are name indexes.

CSV header:
```
register,source_image,page,entry_no,communion_date,year,surname,given_name,age,birth_date,birth_place,baptism_date,baptism_place,residence,parents,needs_review,notes
```
`register` value: `first_communion_1953`.

### Marriage 1872–1907 (`marriage_1872`)

Latin printed *Registrum Matrimoniorum*. Landscape spreads; some first
pages have an unused index leaf. Narrative block: groom + parents, bride
+ parents, witnesses, priest. Right notes: bachelor/spinster, occupation,
age. Letter-tab scans are name indexes.

CSV header:
```
register,source_image,page,marriage_date,year,groom_surname,groom_given,groom_parents,bride_surname,bride_given,bride_parents,witnesses,officiant,groom_age,bride_age,needs_review,notes
```
`register` value: `marriage_1872`. Keep Latin given names as written;
put occupation / status / Protestant / widow notes in `notes`.

### Marriage 1908–1936 (`marriage_1908`)

Continuation of the printed marriage register. Same CSV header as
`marriage_1872`. `register` value: `marriage_1908`.

### Marriage 2009– (`marriage_2009`)

Modern printed marriage register plus letter-tab name index. Same CSV
header as `marriage_1872`. `register` value: `marriage_2009`. Index rows:
put target page in `notes` as `index page_no=N`.

## Finishing up

1. Verify your part CSV parses: number of columns in every row must match
   the header (`python3 -c "import csv;rows=list(csv.reader(open('FILE')));
   print(len(rows), set(len(r) for r in rows))"`).
2. Report: rows written, pages with no entries, entries you flagged
   `needs_review`, and anything unusual.
