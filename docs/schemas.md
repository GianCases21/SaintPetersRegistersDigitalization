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

## Other registers (later volumes still being transcribed)

- **Record of Interments 1847–54** (`interments_1847`): chronological burial book. Extra columns: `burial_date`, `surname`, `given_name`, `age`, `cause_of_death`, `burial_location`. PAGE 001 is accounts (not burials); facing right-hand pages in this volume are cemetery subscription/account ledgers.
- **Baptism**: child name, birth date, baptism date, parents, sponsors, officiant.
- **Marriage**: groom, bride, date, witnesses, officiant.
- **Death / interment**: name, age, death date, burial date, cause (if given).
- **Confirmation / First Communion**: name, date, sponsor, officiant.
- **Sick call**: name, date, location, minister.
