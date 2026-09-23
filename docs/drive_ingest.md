# Drive ingest — new scans onto the website

The nightly job watches the **same Google Drive folder** the original scans
came from, adds every new page to the website, and reads names off the page
when a vision provider is available.

Shared Drive: https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj

Live site: https://giancases21.github.io/SaintPetersRegistersDigitalization/

## What is automatic today

Every day at 11:00 UTC (and on demand) `.github/workflows/ingest-drive.yml`
runs `python3 scripts/auto_ingest.py`:

1. **See new scans** on that Drive — new loose `PAGE ….JPG` files, a new zip,
   or an existing zip whose **byte size changed** (in-place replace).
2. **Fetch** those pages into `incoming/<register_id>/`. Replaced zips are
   unpacked; only filenames not already in a CSV are copied. The duplicate
   `NEW 2023–2024 UPDATED` zip is skipped.
3. **Put them on the website immediately.** Each new page is written to
   `transcriptions/new_scans.csv` so search shows
   `New scan — PAGE 068.JPG` under **New scans (awaiting names)**.
4. **Read the names** with the first available vision provider:
   - `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY` if you set one
   - otherwise **GitHub Copilot** via the workflow `GITHUB_TOKEN`
     (`copilot-requests: write`). That needs a Copilot seat on the repo
     owner’s account — no extra secret.
5. **Publish** — named rows merge into `transcriptions/*.csv` with
   `needs_review=yes`; the pending “New scan” row is removed; the Action
   commits; Pages rebuilds. Hard-refresh the site (Ctrl+Shift+R).

No Google service account is required while the folder stays “anyone with the
link.” A service account is only needed if the folder is made private.

## What still needs a person

- Photograph and upload the pages (or drop a newer zip on Drive).
- If Copilot is not enabled for this repo, add **one** Actions secret
  (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY`) so names
  can be read. New pages still appear on the site without it.
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
