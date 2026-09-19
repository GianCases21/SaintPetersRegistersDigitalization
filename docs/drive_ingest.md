# Drive ingest — new scans onto the website

When photographers add **new page images** to the shared Google Drive, this
pipeline turns them into searchable rows on the website.

Shared Drive: https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj

Live site (GitHub Pages from `main`):
https://giancases21.github.io/SaintPetersRegistersDigitalization/

## Upload new pictures (same Drive as the original scans)

Use the existing book folder on that Drive. Either:

1. **Preferred:** upload individual files named `PAGE 012.JPG` (or `PAGE 12-13.JPG`
   for a spread) next to the current zips / in the book folder, **or**
2. Replace a register zip with a newer dump that contains the new pages.
   The watcher downloads that new zip and pulls out any `PAGE ….JPG` that is
   not already in a CSV. The duplicate `NEW 2023–2024 UPDATED` zip is ignored.

Skip title pages, totals-only pages, and account/fee pages (put accounts in
`_accounts` if you still want an archive photo).

## Automatic website update

GitHub Actions is already on for this repo. After this branch is merged to
`main`, `.github/workflows/ingest-drive.yml` runs every day (and on demand):

| Step | Script | Result |
|---|---|---|
| List Drive | `scripts/watch_drive.py` | Diffs `transcriptions/drive_snapshot.json` |
| Fetch | `--download-new incoming` | New JPGs, and new pages inside replaced zips, land in `incoming/<register_id>/` |
| Transcribe | `scripts/ingest_incoming.py` | Needs `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. Writes part CSVs, merges, flags `needs_review=yes` |
| Publish | commit on `main` + Pages | Search site updates. Hard-refresh (Ctrl+Shift+R) |

Images under `incoming/` are gitignored. Only CSV rows and the pending queue
are committed.

Until a vision key is stored as a GitHub Actions secret, new files are still
**detected** and listed in `transcriptions/pending_scans.md`, but names are not
transcribed onto the site.

Add **one** of these repo secrets (Settings → Secrets and variables → Actions):

| Secret | Purpose |
|---|---|
| `OPENAI_API_KEY` | Transcribe new pages (OpenAI vision) |
| `ANTHROPIC_API_KEY` | Transcribe new pages (Anthropic vision) |

Do not store the volunteer mailbox password in GitHub or in this repo.

## Local run

```bash
python3 scripts/watch_drive.py --download-new incoming
python3 scripts/ingest_incoming.py
python3 scripts/scan_resume.py
```

## Folder names

Prefer `incoming/<register_id>/PAGE 012.JPG` or a Drive folder named like the
book (`Baptism 2011-`, `Marriage 1937-1963`). Loose `PAGE 068.JPG` at the Drive
root cannot be assigned to a book.

The 1839 baptism zip/folder also holds other sacraments:

| Filename | Register |
|---|---|
| `PAGE 001.JPG` … `PAGE 133.JPG` | `baptism_1839` |
| `PAGE 134.JPG` | `funerals_1868` |
| `PAGE 135.JPG` … `PAGE 147.JPG` | `confirmation_early` |
| `PAGE 148.JPG` onward | accounts — skip |
