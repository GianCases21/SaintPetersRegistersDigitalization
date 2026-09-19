# Drive ingest — new scans onto the website

When photographers add **new page images** to the shared Google Drive, this
pipeline is what turns them into searchable rows on the website.

Shared Drive: https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj

## What has to be true for it to be automatic

1. **Upload pages as individual JPGs**, in the existing book folder, named
   `PAGE 012.JPG` (or `PAGE 12-13.JPG` for a spread). Do not replace a whole
   register with a new zip. Today's Drive folder is 13 zip dumps plus the
   logbook; a watcher can see “a zip changed” but not “page 18 was added
   inside the zip.”
2. **GitHub Actions** enabled on this repository (Settings → Actions).
3. **A vision API key** stored as a repo secret named `OPENAI_API_KEY` or
   `ANTHROPIC_API_KEY`. Detection does not need a key; transcription does.
4. The workflow file `.github/workflows/ingest-drive.yml` merged onto
   `main` (scheduled jobs only run on the default branch).

Until 2–4 are in place, run the same scripts locally after an upload:

```bash
python3 scripts/watch_drive.py --download-new incoming
python3 scripts/ingest_incoming.py
python3 scripts/scan_resume.py
```

## What the job does

| Step | Script | Result |
|---|---|---|
| List Drive | `scripts/watch_drive.py` | Updates `transcriptions/drive_snapshot.json`. Writes `transcriptions/pending_scans.md` with any new files. |
| Download | `watch_drive.py --download-new incoming` | New JPGs land in `incoming/<register_id>/`. Zips are never downloaded. |
| Transcribe | `scripts/ingest_incoming.py` | If an API key is set, writes `transcriptions/parts/<register>_auto_<page>.csv` and merges into the register CSV. Every auto row is `needs_review=yes`. |
| Resume guide | `scripts/scan_resume.py` | Refreshes [scan_resume.md](scan_resume.md) so photographers see the new last date / last record. |
| Publish | GitHub Action commit + GitHub Pages from `main` | `index.html` reads the CSVs. Hard-refresh the site (Ctrl+Shift+R). |

Images under `incoming/` are gitignored. Only CSV rows and the pending queue are committed.

## Folder names

The watcher maps a Drive path to a register. Prefer the **book's own folder**
or a local folder named with the register id:

```
incoming/baptism_2011/PAGE 068.JPG
incoming/marriage_1937/PAGE 059.JPG
incoming/confirmation_2015/PAGE 4.JPG
```

On Drive, a folder named like the book (`Baptism 2011-`, `Marriage 1937-1963`)
works too. Loose `PAGE 068.JPG` files at the Drive root cannot be assigned to a
book — put them in the book folder.

The 1839 baptism zip/folder also holds other sacraments:

| Filename | Register |
|---|---|
| `PAGE 001.JPG` … `PAGE 133.JPG` | `baptism_1839` |
| `PAGE 134.JPG` | `funerals_1868` |
| `PAGE 135.JPG` … `PAGE 147.JPG` | `confirmation_early` |
| `PAGE 148.JPG` onward | accounts — skip |

## Secrets a repo admin needs to add

| Secret | Purpose |
|---|---|
| `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` | Transcribe new pages overnight |
| (later) a Google service account JSON | Needed only if the Drive folder is made private; today's public `gdown` listing works while the folder is “anyone with the link” |

Do not store the volunteer mailbox password in GitHub or in this repo.

## What still needs a person

- Photographing the fragment books (see [scan_resume.md](scan_resume.md))
- Spot-checking rows with `needs_review=yes`
- Deciding privacy on the Drive folder
- Enabling Actions and adding the vision key (once)

Detection without transcription still helps: `pending_scans.md` will list every
new JPG the day it appears, so nothing sits on Drive unnoticed.
