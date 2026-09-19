# incoming/

Drop new register photographs here when you are not uploading them to Google
Drive, or when the ingest job has downloaded new Drive pages for transcription.

```
incoming/<register_id>/PAGE 012.JPG
```

Register ids match `transcriptions/manifest.json` (also listed in
`docs/scan_resume.md`). Examples:

- `incoming/baptism_2011/PAGE 068.JPG`
- `incoming/marriage_1937/PAGE 001.JPG`
- `incoming/confirmation_2015/PAGE 4.JPG`

Then:

```bash
python3 scripts/ingest_incoming.py
```

Image files in this folder are gitignored on purpose. The website only stores
the transcribed CSV rows.
