# Register CSV schemas

Every transcription CSV shares a few common columns so records can be
searched across registers:

| Column | Meaning |
|---|---|
| `register` | which register the row came from (matches the CSV filename) |
| `source_image` | the scanned page image the row was transcribed from |
| `page` | page number(s) as written in the register |
| `year` | best-known year for the record (for search); blank if unknown |
| `needs_review` | `yes` if any field was hard to read and should be checked against the scan |
| `notes` | anything unusual: marginal notes, cross-outs, uncertain readings |

Uncertain readings inside a field are marked with `(?)`.

## Cemetery plot registers (`st_joseph_section_1939`)

Organized by tier and grave number. A grave often lists the plot owner and
one or more interments.

Extra columns: `tier`, `grave_no`, `plot_owner`, `surname`, `given_name`,
`age`, `interment_type` (vault/box), `undertaker`, `date_of_death`,
`date_of_burial`.

## Record of Interments 1847–54 (`interments_1847`)

Narrative burial book, chronological, Sep 1847–Mar 1854. Extra columns:
`burial_date`, `age`, `cause_of_death`, `burial_location` (relative to
another grave). Facing right pages are cemetery accounts, not burials.

## Reception Into Full Communion (`reception_full_communion`)

Modern printed register of persons received into the Catholic Church at
St. Peter, Belleville. Extra columns: `entry_no`, `date_of_reception`,
`father`, `mother_maiden`, `sponsor`, `priest`, `baptism_date`,
`baptism_place`, `baptism_minister`. Marriage / confirmation notes go in
`notes`.

## Record of Cemetery 1854–1870 (`cemetery_1854`)

Narrative burial book continuing from 1854. Extra columns: `burial_date`,
`age`, `cause_of_death`, `nativity`, `residence`, `parents`,
`burial_location`, `fee`.

## Baptism 1839–1875 (`baptism_1839`)

Extra columns: `baptism_date`, `age_or_birth`, `father`, `mother`,
`sponsors`, `officiant`.

## Marriage 1840–1871 (`marriage_1840`)

Extra columns: `marriage_date`, `groom_surname`, `groom_given`,
`bride_surname`, `bride_given`, `witnesses`, `officiant`.

## First Communion 1895–1941 (`first_communion_1895`)

Extra columns: `age`. Index pages store the target page in `notes`.

## Sick Call Register 1973–2006 (`sick_call_1973`)

Extra columns: `call_date`, `residence`, `confession`, `communion`,
`viaticum`, `anointing`, `last_blessing`, `priest`.

## Baptism 1989–2011 (`baptism_1989`)

Extra columns: `entry_no`, `residence`, `birth_date`, `birth_place`,
`baptism_date`, `father`, `mother_maiden`, `sponsors`, `priest`,
`confirmation`. Marriage notes go in `notes`.

## Confirmation 1942–1952 / 1991–2014 / 2015– (`confirmation_1942`, `confirmation_1991`, `confirmation_2015`)

Extra columns: `confirmation_date`, `entry_no`, `confirmation_name`,
`age`, `baptism_date`, `baptism_place`, `residence`, `father`, `mother`,
`sponsor`, `minister`. The 1942–1952 book is a First Communion Register
form; some classes are confirmation, some first communion (`notes` has
`event=`).

## Death 1895–1899 (`death_1895`)

Extra columns: `death_date`, `age`, `residence`, `state_of_life`,
`cause_of_death`, `sacraments`, `doctor`, `undertaker`, `cemetery`.

## Death 1990–2001 / 2001–2018 / Section E (`death_1990`, `death_2001`, `death_section_e`)

Extra columns: `entry_no`, `age`, `nearest_relative`, `relative_address`,
`death_date`, `sacraments`, `priest`, `burial_date`, `cemetery`,
`undertaker`.

## First Communion 1953–1961 (`first_communion_1953`)

Extra columns: `entry_no`, `communion_date`, `age`, `birth_date`,
`birth_place`, `baptism_date`, `baptism_place`, `residence`, `parents`.

## Marriage 1872–1907 / 1908–1936 / 2009– (`marriage_1872`, `marriage_1908`, `marriage_2009`)

Extra columns: `marriage_date`, `groom_surname`, `groom_given`,
`groom_parents`, `bride_surname`, `bride_given`, `bride_parents`,
`witnesses`, `officiant`, `groom_age`, `bride_age`.

## Other fragment volumes (indexes / stray pages)

Letter-tab and one-page fragments (Baptism 1875–1903, 1904–1921,
1965–1972, 2011; Confirmation 1895–1944, 1957–1964, 1974–1990;
Death C 1924–1964 and SECTION D; First Communion 1962–1970;
Marriage 1937–1963) use the matching register schema above, or a
name-index row (`notes` = `index page_no=N`) when the scan is only a tab.
