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

## Finishing up

1. Verify your part CSV parses: number of columns in every row must match
   the header (`python3 -c "import csv;rows=list(csv.reader(open('FILE')));
   print(len(rows), set(len(r) for r in rows))"`).
2. Report: rows written, pages with no entries, entries you flagged
   `needs_review`, and anything unusual.
