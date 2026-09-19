# Pending scans

Drive listing at 2026-09-19T14:56:03Z.

The website is updated from CSVs under `transcriptions/`. This file is the
queue of Drive files that are not in those CSVs yet.

No new page images. The Drive folder is still the original zip dumps plus
the logbook. When photographers add `PAGE ….JPG` files next to (not inside)
those zips, they will show up here and `scripts/ingest_incoming.py` can
transcribe them into the website.

## What happens next

```bash
python3 scripts/watch_drive.py --download-new incoming
python3 scripts/ingest_incoming.py
```

With a vision API key (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`) the ingest
script transcribes new pages into `transcriptions/parts/` and merges them so
`index.html` can search the new names. Without a key, the images stay queued.
