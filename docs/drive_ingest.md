# Drive ingest — new scans onto the website

The nightly job watches the **same Google Drive folder** the original scans
came from and, when a vision key is present, transcribes new pages into the
searchable CSVs so GitHub Pages updates.

Shared Drive: https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj

Live site: https://giancases21.github.io/SaintPetersRegistersDigitalization/

## What is automatic today

Every day (and on demand) `.github/workflows/ingest-drive.yml` runs
`python3 scripts/auto_ingest.py`:

1. **See new scans** on that Drive — new loose `PAGE ….JPG` files, a new zip,
   or an existing zip whose **byte size changed** (in-place replace).
2. **Fetch** those pages into `incoming/<register_id>/`. Replaced zips are
   unpacked; only filenames not already in a CSV are copied. The duplicate
   `NEW 2023–2024 UPDATED` zip is skipped.
3. **Transcribe** each new page when `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or
   `GEMINI_API_KEY` is set. Rows are merged into `transcriptions/*.csv` with
   `needs_review=yes`.
4. **Publish** — the Action commits CSVs and `ingest_status.json`; Pages
   rebuilds. Hard-refresh the site (Ctrl+Shift+R).

No Google service account is required while the folder stays “anyone with the
link.” A service account is only needed if the folder is made private.

## What still needs a person

- Photograph and upload the pages (or drop a newer zip on Drive).
- Add **one** GitHub Actions secret so names can be read off the page:
  `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY`.
  Detection works without it; transcription does not.
- Spot-check rows flagged `needs_review`.

## Upload

Prefer `PAGE 012.JPG` in the book folder. Replacing a register zip also works
because the watcher fingerprints zip size each run.

```
incoming/baptism_2011/PAGE 068.JPG
```

## Local

```bash
python3 scripts/auto_ingest.py --download-new incoming
```
