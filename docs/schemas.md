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

## Reception Into Full Communion (`reception_full_communion`)

Modern printed register of persons received into the Catholic Church at
St. Peter, Belleville. Extra columns: `entry_no`, `date_of_reception`,
`father`, `mother_maiden`, `sponsor`, `priest`, `baptism_date`,
`baptism_place`, `baptism_minister`. Marriage / confirmation notes go in
`notes`.

## Other registers (schemas added as each register is transcribed)

- **Record of Interments 1847–54** (`interments_1847`): chronological burial book. Extra columns: `burial_date`, `surname`, `given_name`, `age`, `cause_of_death`, `burial_location`. PAGE 001 is accounts (not burials); facing right-hand pages in this volume are cemetery subscription/account ledgers.
- **Baptism**: child name, birth date, baptism date, parents, sponsors, officiant.
- **Marriage**: groom, bride, date, witnesses, officiant.
- **Death / interment**: name, age, death date, burial date, cause (if given).
- **Confirmation / First Communion**: name, date, sponsor, officiant.
- **Sick call**: name, date, location, minister.
