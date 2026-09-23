#!/usr/bin/env python3
"""List the shared Google Drive folder and queue scans the website does not have.

Compares the live Drive listing to transcriptions/drive_snapshot.json and to
source_image names already in the CSVs. New page images can be downloaded into
incoming/<register_id>/ for ingest_incoming.py.

Loose JPGs are preferred. If a zip on Drive is replaced (new file id / name),
that archive is downloaded and any PAGE images not already in a CSV are
extracted. The duplicate “NEW 2023–2024 UPDATED” zip is skipped.

Usage:
    python3 scripts/watch_drive.py
    python3 scripts/watch_drive.py --download-new incoming
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from drive_fingerprint import fingerprint_files  # noqa: E402
from register_catalog import (  # noqa: E402
    DRIVE_URL,
    ROOT,
    TRANSCRIPTIONS,
    analyze_register,
    kind_for_name,
    load_manifest,
    map_drive_path,
    should_skip_filename,
    zip_label,
)

SNAPSHOT = TRANSCRIPTIONS / "drive_snapshot.json"
PENDING = TRANSCRIPTIONS / "pending_scans.md"
PENDING_JSON = TRANSCRIPTIONS / "pending_scans.json"


def skip_archive(path: str) -> bool:
    """Duplicate portrait dump of the 1839 book — not a source of new pages."""
    lower = path.lower()
    return "new 2023" in lower or "2023-2024 updated" in lower


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def list_drive(url: str) -> list[dict]:
    try:
        import gdown
    except ImportError as exc:
        raise SystemExit("gdown is not installed. Run: pip install -r requirements.txt") from exc

    listed = gdown.download_folder(url, output=str(ROOT / "drive_sample"), skip_download=True, quiet=False)
    files = []
    for item in listed or []:
        file_id = getattr(item, "id", "") or ""
        rel = getattr(item, "path", "") or str(item)
        rel = str(rel).replace("\\", "/")
        files.append(
            {
                "id": file_id,
                "path": rel,
                "name": Path(rel).name,
                "kind": kind_for_name(rel),
            }
        )
    files.sort(key=lambda row: row["path"].lower())
    return files


def transcribed_names() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for item in load_manifest():
        stats = analyze_register(item)
        found[item["id"]] = {name.upper() for name in stats["images"]}
    return found


def classify(
    files: list[dict],
    old_ids: set[str],
    transcribed: dict[str, set[str]],
    old_sizes: dict[str, int] | None = None,
) -> dict:
    old_sizes = old_sizes or {}
    new_files = []
    for row in files:
        size_changed = False
        old_size = old_sizes.get(row.get("id") or "")
        new_size = row.get("size")
        if old_size and new_size and int(old_size) != int(new_size):
            size_changed = True
        if not old_ids:
            is_new = False
        elif size_changed:
            is_new = True
        elif row["id"]:
            is_new = row["id"] not in old_ids
        else:
            is_new = True
        payload = {
            **row,
            "register_id": map_drive_path(row["path"]),
            "skip": should_skip_filename(row["name"]),
            "is_new": is_new,
            "size_changed": size_changed,
        }
        names = transcribed.get(payload["register_id"] or "", set())
        payload["already_transcribed"] = row["name"].upper() in names
        new_files.append(payload)

    images = [
        row for row in new_files
        if row["kind"] == "image" and not row["skip"] and not row["already_transcribed"]
    ]
    new_images = [row for row in images if row["is_new"]]
    new_zips = [row for row in new_files if row["kind"] == "zip" and row["is_new"]]
    size_changed_zips = [row for row in new_zips if row.get("size_changed")]
    unknown = [
        row for row in new_images
        if row["is_new"] and not row["register_id"]
    ]
    return {
        "images_not_in_csv": images,
        "new_images": new_images,
        "new_zips": new_zips,
        "size_changed_zips": size_changed_zips,
        "unknown_folder": unknown,
        "files": new_files,
    }


def extract_new_images_from_zip(
    zip_path: Path,
    dest_root: Path,
    transcribed: dict[str, set[str]],
    archive_name: str,
    max_files: int,
) -> list[dict]:
    """Copy PAGE images that are not already transcribed into dest_root/<register_id>/."""
    found: list[dict] = []
    dest_root = dest_root.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir() or "__MACOSX" in info.filename:
                continue
            inner = info.filename.replace("\\", "/")
            name = Path(inner).name
            if name.startswith(".") or kind_for_name(name) != "image":
                continue
            if should_skip_filename(name):
                continue
            register_id = map_drive_path(inner) or map_drive_path(f"{archive_name}/{inner}")
            if not register_id:
                continue
            if name.upper() in transcribed.get(register_id, set()):
                continue
            dest_dir = dest_root / register_id
            dest = (dest_dir / name).resolve()
            try:
                dest.relative_to(dest_dir.resolve())
            except ValueError:
                continue
            dest_dir.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                with zf.open(info) as src, dest.open("wb") as out:
                    out.write(src.read())
            found.append(
                {
                    "register_id": register_id,
                    "name": name,
                    "path": inner,
                    "dest": str(dest),
                }
            )
            if len(found) >= max_files:
                break
    return found


def write_pending(classified: dict, listed_at: str, extracted: list[dict] | None = None) -> None:
    lines = [
        "# Pending scans",
        "",
        f"Drive listing at {listed_at}.",
        "",
        "The website is updated from CSVs under `transcriptions/`. This file is the",
        "queue of Drive files that are not in those CSVs yet.",
        "",
    ]
    new_images = classified["new_images"]
    new_zips = classified["new_zips"]
    queued = classified["images_not_in_csv"]
    extracted = extracted or []

    if not new_images and not new_zips and not queued and not extracted:
        lines += [
            "No new page images. The Drive folder is still the original zip dumps plus",
            "the logbook. When photographers add `PAGE ….JPG` files next to those zips,",
            "or replace a zip with a newer dump that contains new pages, they will show",
            "up here and `scripts/ingest_incoming.py` can transcribe them into the website.",
            "",
        ]
    if new_zips:
        lines += ["## New or replaced zip archives", ""]
        lines.append(
            "A new zip dump was detected. `watch_drive.py --download-new` unpacks it "
            "and copies any `PAGE ….JPG` files that are not already in a CSV into `incoming/`."
        )
        lines.append("The duplicate “NEW 2023–2024 UPDATED” zip is skipped.")
        lines.append("")
        for row in new_zips:
            skipped = " (skipped duplicate dump)" if skip_archive(row["path"]) else ""
            lines.append(f"- `{row['path']}` — {zip_label(row['path'])}{skipped}")
        lines.append("")
    if extracted:
        lines += ["## New pages extracted from zips", ""]
        for row in extracted:
            lines.append(f"- `{row['name']}` → `{row['register_id']}`")
        lines.append("")
    if new_images:
        lines += ["## New page images on Drive", ""]
        for row in new_images:
            register = row["register_id"] or "UNKNOWN FOLDER — put this in the book folder"
            flag = "" if row["register_id"] else " **(needs a book folder)**"
            lines.append(f"- `{row['path']}` → `{register}`{flag}")
        lines.append("")
    elif queued:
        lines += ["## Images on Drive not yet in a CSV", ""]
        for row in queued:
            register = row["register_id"] or "UNKNOWN"
            lines.append(f"- `{row['path']}` → `{register}`")
        lines.append("")

    lines += [
        "## What happens next",
        "",
        "```bash",
        "python3 scripts/watch_drive.py --download-new incoming",
        "python3 scripts/ingest_incoming.py",
        "```",
        "",
        "The ingest job publishes each new page to `transcriptions/new_scans.csv`",
        "(visible on the website) and transcribes names with Copilot or an optional",
        "`OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY`.",
        "",
    ]
    PENDING.write_text("\n".join(lines), encoding="utf-8")
    PENDING_JSON.write_text(
        json.dumps(
            {
                "listed_at": listed_at,
                "new_images": classified["new_images"],
                "new_zips": classified["new_zips"],
                "size_changed_zips": classified.get("size_changed_zips") or [],
                "images_not_in_csv": classified["images_not_in_csv"],
                "extracted_from_zips": extracted,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def snapshot_payload(files: list[dict], listed_at: str) -> dict:
    return {
        "drive_url": DRIVE_URL,
        "listed_at": listed_at,
        "files": [
            {
                "id": row["id"],
                "path": row["path"],
                "kind": row["kind"],
                "size": row.get("size"),
                "label": row.get("label") or "",
            }
            for row in files
        ],
    }


def files_changed(old: dict | None, new_files: list[dict]) -> bool:
    if not old:
        return True
    old_rows = {
        (row.get("id"), row.get("path"), row.get("size"))
        for row in old.get("files") or []
    }
    new_rows = {(row["id"], row["path"], row.get("size")) for row in new_files}
    return old_rows != new_rows


def download_new_images(rows: list[dict], dest_root: Path, max_files: int) -> list[Path]:
    import gdown

    saved: list[Path] = []
    for row in rows[:max_files]:
        register_id = row["register_id"]
        if not register_id:
            print(f"skip (unknown register): {row['path']}", file=sys.stderr)
            continue
        dest_dir = dest_root / register_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / row["name"]
        if dest.exists():
            saved.append(dest)
            continue
        print(f"downloading {row['path']} -> {dest}")
        gdown.download(id=row["id"], output=str(dest), quiet=False)
        if dest.exists():
            saved.append(dest)
    return saved


def download_and_unpack_zips(
    rows: list[dict],
    dest_root: Path,
    transcribed: dict[str, set[str]],
    max_files: int,
) -> list[dict]:
    import gdown

    extracted: list[dict] = []
    remaining = max_files
    for row in rows:
        if remaining <= 0:
            break
        if skip_archive(row["path"]):
            print(f"skip duplicate archive: {row['path']}", file=sys.stderr)
            continue
        tmpdir = Path(tempfile.mkdtemp(prefix="drive_zip_"))
        zip_path = tmpdir / Path(row["name"]).name
        print(f"downloading zip {row['path']} -> {zip_path}")
        gdown.download(id=row["id"], output=str(zip_path), quiet=False, resume=True)
        if not zip_path.exists():
            print(f"zip download failed: {row['path']}", file=sys.stderr)
            continue
        batch = extract_new_images_from_zip(
            zip_path, dest_root, transcribed, row["path"], remaining
        )
        extracted.extend(batch)
        remaining = max_files - len(extracted)
        print(f"extracted {len(batch)} new page(s) from {row['name']}")
    return extracted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DRIVE_URL)
    parser.add_argument("--snapshot", default=str(SNAPSHOT))
    parser.add_argument("--download-new", metavar="DIR", help="download new JPGs into DIR/<register_id>/")
    parser.add_argument("--max-files", type=int, default=40, help="cap on downloaded/extracted new images")
    parser.add_argument("--offline", action="store_true", help="do not call Drive; rewrite pending from snapshot")
    parser.add_argument(
        "--skip-zips",
        action="store_true",
        help="do not download/unpack replaced zip archives",
    )
    parser.add_argument(
        "--skip-fingerprint",
        action="store_true",
        help="do not probe Drive zip byte sizes",
    )
    args = parser.parse_args()

    snapshot_path = Path(args.snapshot)
    old = json.loads(snapshot_path.read_text(encoding="utf-8")) if snapshot_path.exists() else None
    old_ids = {row.get("id") for row in (old or {}).get("files") or [] if row.get("id")}
    old_sizes = {
        row["id"]: int(row["size"])
        for row in (old or {}).get("files") or []
        if row.get("id") and row.get("size")
    }

    if args.offline:
        if not old:
            raise SystemExit(f"no snapshot at {snapshot_path}")
        files = list(old["files"])
        listed_at = old.get("listed_at") or _utc_now()
    else:
        files = list_drive(args.url)
        if not args.skip_fingerprint:
            files = fingerprint_files(files)
        listed_at = _utc_now()
        payload = snapshot_payload(files, listed_at)
        if files_changed(old, files) or not snapshot_path.exists():
            snapshot_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            print(f"Wrote {snapshot_path} ({len(files)} files)")
        else:
            print(f"Drive listing unchanged ({len(files)} files)")

    transcribed = transcribed_names()
    classified = classify(files, old_ids, transcribed, old_sizes)
    extracted: list[dict] = []

    if args.download_new:
        dest = Path(args.download_new)
        if not dest.is_absolute():
            dest = ROOT / dest
        downloaded = download_new_images(classified["new_images"], dest, args.max_files)
        print(f"downloaded {len(downloaded)} image(s) into {dest}")
        remaining = max(0, args.max_files - len(downloaded))
        if not args.skip_zips and remaining and classified["new_zips"]:
            extracted = download_and_unpack_zips(
                classified["new_zips"], dest, transcribed, remaining
            )
            print(f"extracted {len(extracted)} new page(s) from replaced zips")

    previous_pending = json.loads(PENDING_JSON.read_text(encoding="utf-8")) if PENDING_JSON.exists() else None
    pending_changed = previous_pending is None or any(
        previous_pending.get(key) != classified[key]
        for key in ("new_images", "new_zips", "images_not_in_csv")
    ) or (extracted and previous_pending.get("extracted_from_zips") != extracted)
    if pending_changed or not PENDING.exists() or extracted:
        write_pending(classified, listed_at, extracted)
        print(f"Wrote {PENDING}")
    else:
        print("Pending queue unchanged")
    print(
        f"new images={len(classified['new_images'])} "
        f"new zips={len(classified['new_zips'])} "
        f"untranscribed images={len(classified['images_not_in_csv'])} "
        f"extracted={len(extracted)}"
    )


if __name__ == "__main__":
    main()
