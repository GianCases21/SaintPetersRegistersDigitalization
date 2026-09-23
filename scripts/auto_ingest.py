#!/usr/bin/env python3
"""One-command Drive → website ingest.

Usage:
    python3 scripts/auto_ingest.py
    python3 scripts/auto_ingest.py --download-new incoming
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingest_incoming import run_ingest, vision_name  # noqa: E402
from register_catalog import ROOT, TRANSCRIPTIONS  # noqa: E402

STATUS = TRANSCRIPTIONS / "ingest_status.json"
PENDING_JSON = TRANSCRIPTIONS / "pending_scans.json"


def write_status(payload: dict) -> None:
    STATUS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {STATUS}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download-new", default="incoming")
    parser.add_argument("--skip-fingerprint", action="store_true")
    parser.add_argument("--skip-zips", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    watch_cmd = [
        sys.executable,
        str(ROOT / "scripts" / "watch_drive.py"),
        "--download-new",
        args.download_new,
    ]
    if args.skip_fingerprint:
        watch_cmd.append("--skip-fingerprint")
    if args.skip_zips:
        watch_cmd.append("--skip-zips")
    subprocess.run(watch_cmd, check=True)

    incoming = Path(args.download_new)
    if not incoming.is_absolute():
        incoming = ROOT / incoming
    ingest = run_ingest(incoming, dry_run=args.dry_run)

    pending = json.loads(PENDING_JSON.read_text(encoding="utf-8")) if PENDING_JSON.exists() else {}
    snapshot = {}
    snap_path = TRANSCRIPTIONS / "drive_snapshot.json"
    if snap_path.exists():
        snapshot = json.loads(snap_path.read_text(encoding="utf-8"))

    status = {
        "checked_on": date.today().isoformat(),
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "drive_files": len(snapshot.get("files") or []),
        "new_images": len(pending.get("new_images") or []),
        "new_zips": len(pending.get("new_zips") or []),
        "size_changed_zips": len(pending.get("size_changed_zips") or []),
        "extracted_from_zips": len(pending.get("extracted_from_zips") or []),
        "transcribed_pages": ingest["transcribed_pages"],
        "rows_added": ingest["rows_added"],
        "pending_pages": ingest["queued"],
        "errors": ingest["errors"],
        "vision": vision_name(),
        "queued_files": ingest["queued_files"],
    }
    write_status(status)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "scan_resume.py")], check=False)


if __name__ == "__main__":
    main()
