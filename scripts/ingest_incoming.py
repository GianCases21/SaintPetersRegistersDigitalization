#!/usr/bin/env python3
"""Turn new page images in incoming/<register_id>/ into website CSV rows.

Images whose filenames are already a source_image in that register are skipped.
Vision providers, in order: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY,
then GitHub Copilot (GITHUB_TOKEN / Copilot CLI). Every auto row is flagged
needs_review=yes. Pages that cannot be read yet are listed on the website via
transcriptions/new_scans.csv.

Usage:
    python3 scripts/ingest_incoming.py
    python3 scripts/ingest_incoming.py --incoming incoming
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from register_catalog import (  # noqa: E402
    ROOT,
    TRANSCRIPTIONS,
    analyze_register,
    csv_header,
    kind_for_name,
    load_manifest,
    map_drive_path,
    pages_from_filename,
    register_title,
    should_skip_filename,
)

INCOMING = ROOT / "incoming"
PARTS = TRANSCRIPTIONS / "parts"
PENDING = TRANSCRIPTIONS / "pending_scans.md"
NEW_SCANS = TRANSCRIPTIONS / "new_scans.csv"
NEW_SCANS_HEADER = [
    "register",
    "source_image",
    "name",
    "page",
    "book",
    "notes",
    "needs_review",
]

SKIP_VALUES = {"register", "source_image", "needs_review"}
COPILOT_CHAT_URL = "https://api.githubcopilot.com/chat/completions"


def copilot_token() -> str:
    return (
        os.environ.get("COPILOT_GITHUB_TOKEN")
        or os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
        or ""
    )


def copilot_cli_path() -> str:
    import shutil

    return shutil.which(os.environ.get("COPILOT_CLI", "copilot")) or ""


def copilot_usable() -> bool:
    if os.environ.get("INGEST_SKIP_COPILOT"):
        return False
    return bool(copilot_token() or copilot_cli_path())


def vision_ready() -> bool:
    return bool(
        os.environ.get("OPENAI_API_KEY")
        or os.environ.get("ANTHROPIC_API_KEY")
        or os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("INGEST_STUB")
        or copilot_usable()
    )


def vision_name() -> str:
    if os.environ.get("INGEST_STUB"):
        return "stub"
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if copilot_usable():
        return "copilot"
    return "missing"


def discover_images(incoming: Path) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    if not incoming.exists():
        return found
    for path in sorted(incoming.rglob("*")):
        if not path.is_file() or kind_for_name(path.name) != "image":
            continue
        if should_skip_filename(path.name):
            continue
        rel = path.relative_to(incoming)
        register_id = map_drive_path(str(rel))
        if not register_id:
            print(f"skip (unknown register): {rel}", file=sys.stderr)
            continue
        found.append((register_id, path))
    return found


def already_transcribed(register_id: str, filename: str) -> bool:
    for item in load_manifest():
        if item["id"] != register_id:
            continue
        stats = analyze_register(item)
        return filename.upper() in {name.upper() for name in stats["images"]}
    return False


def example_rows(register_id: str, limit: int = 2) -> list[dict]:
    for item in load_manifest():
        if item["id"] != register_id:
            continue
        stats = analyze_register(item)
        rows = []
        if stats["last_row"]:
            rows.append(stats["last_row"])
        path = TRANSCRIPTIONS / item["file"]
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row not in rows:
                    rows.append(row)
                if len(rows) >= limit:
                    break
        return rows[:limit]
    return []


def resize_jpeg(path: Path, max_side: int = 2000) -> bytes:
    from PIL import Image

    image = Image.open(path)
    image = image.convert("RGB")
    if max(image.size) > max_side:
        image.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = BytesIO()
    image.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


def build_prompt(register_id: str, header: list[str], filename: str) -> str:
    samples = example_rows(register_id)
    sample_text = ""
    if samples:
        from io import StringIO

        sio = StringIO()
        writer = csv.DictWriter(sio, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in samples:
            writer.writerow({key: row.get(key, "") for key in header})
        sample_text = sio.getvalue().strip()
    return f"""You transcribe one scanned page of a Saint Peter's church register into CSV.

Return ONLY CSV text (header + data rows). No markdown fences, no commentary.

Rules:
- Header must be exactly: {",".join(header)}
- register={register_id}
- source_image={filename}  (keep spaces; this exact filename)
- needs_review=yes for every row (machine transcription)
- Uncertain readings: best guess plus (?) in that field
- Completely illegible: [illegible]
- Expand ditto marks to the value from the row above
- Dates like Mon D YYYY (e.g. Jul 7 1850); also fill year
- One row per person / couple / burial, not per page
- Skip blank pages: return only the header
- Ignore title/account/totals-only pages: return only the header
- Do not invent names

Example rows from this register:
{sample_text}
"""


def parse_csv_text(text: str, header: list[str], register_id: str, filename: str) -> list[dict]:
    text = text.strip()
    text = re.sub(r"^```(?:csv)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    reader = csv.DictReader(lines)
    rows = []
    fields = reader.fieldnames or header
    for row in reader:
        out = {key: (row.get(key) or "").strip() for key in header}
        if not any(out[key] for key in header if key not in SKIP_VALUES):
            continue
        out["register"] = register_id
        out["source_image"] = filename
        out["needs_review"] = "yes"
        # drop rows that are just a repeated header
        if out.get(fields[0] if fields else "") == (fields[0] if fields else ""):
            continue
        rows.append(out)
    return rows


def openai_transcribe(image_bytes: bytes, prompt: str) -> str:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")
    body = {
        "model": os.environ.get("OPENAI_VISION_MODEL", "gpt-4o"),
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode("ascii")
                        },
                    },
                ],
            }
        ],
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI HTTP {exc.code}: {detail[:500]}") from exc
    return payload["choices"][0]["message"]["content"]


def anthropic_transcribe(image_bytes: bytes, prompt: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY missing")
    body = {
        "model": os.environ.get("ANTHROPIC_VISION_MODEL", "claude-sonnet-4-5"),
        "max_tokens": 8000,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64.b64encode(image_bytes).decode("ascii"),
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic HTTP {exc.code}: {detail[:500]}") from exc
    parts = payload.get("content") or []
    return "".join(part.get("text", "") for part in parts if part.get("type") == "text")


def gemini_transcribe(image_bytes: bytes, prompt: str) -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing")
    model = os.environ.get("GEMINI_VISION_MODEL", "gemini-2.0-flash")
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64.b64encode(image_bytes).decode("ascii"),
                        }
                    },
                ]
            }
        ],
        "generationConfig": {"temperature": 0},
    }
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={key}"
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini HTTP {exc.code}: {detail[:500]}") from exc
    parts = (((payload.get("candidates") or [{}])[0].get("content") or {}).get("parts") or [])
    return "".join(part.get("text", "") for part in parts)


def copilot_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Copilot-Integration-Id": os.environ.get(
            "COPILOT_INTEGRATION_ID", "copilot-developer-cli"
        ),
        "copilot-vision-request": "true",
        "Editor-Version": os.environ.get("COPILOT_EDITOR_VERSION", "vscode/1.104.0"),
        "Editor-Plugin-Version": "SaintPetersRegistersIngest/1.0",
        "User-Agent": "SaintPetersRegistersIngest/1.0",
    }


def copilot_request_body(image_bytes: bytes, prompt: str) -> dict:
    model = os.environ.get("COPILOT_VISION_MODEL", "gpt-4o")
    return {
        "model": model,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/jpeg;base64,"
                            + base64.b64encode(image_bytes).decode("ascii")
                        },
                    },
                ],
            }
        ],
    }


def copilot_http_transcribe(image_bytes: bytes, prompt: str) -> str:
    token = copilot_token()
    if not token:
        raise RuntimeError("GITHUB_TOKEN missing for Copilot")
    url = os.environ.get("COPILOT_API_URL", COPILOT_CHAT_URL)
    req = urllib.request.Request(
        url,
        data=json.dumps(copilot_request_body(image_bytes, prompt)).encode("utf-8"),
        headers=copilot_headers(token),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Copilot HTTP {exc.code}: {detail[:500]}") from exc
    choices = payload.get("choices") or []
    if choices:
        message = choices[0].get("message") or {}
        content = message.get("content") or ""
        if isinstance(content, list):
            return "".join(part.get("text", "") for part in content if isinstance(part, dict))
        return str(content)
    raise RuntimeError(f"Copilot response had no choices: {str(payload)[:300]}")


def copilot_cli_transcribe(path: Path, prompt: str) -> str:
    cli = copilot_cli_path()
    if not cli:
        raise RuntimeError("copilot CLI is not installed")
    image = path.resolve()
    full = f"{prompt}\n\nThe register page image is attached here: @{image}\nReturn ONLY CSV."
    cmd = [cli, "-p", full, "-s", "--no-ask-user"]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("copilot CLI is not installed") from exc
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"copilot CLI {proc.returncode}: {err[:500]}")
    return proc.stdout


def copilot_transcribe(image_bytes: bytes, prompt: str, path: Path) -> str:
    errors: list[str] = []
    if copilot_cli_path():
        try:
            return copilot_cli_transcribe(path, prompt)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"cli: {exc}")
    if copilot_token():
        try:
            return copilot_http_transcribe(image_bytes, prompt)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"http: {exc}")
    raise RuntimeError("copilot failed: " + " | ".join(errors or ["no token or CLI"]))


def load_new_scans() -> list[dict]:
    if not NEW_SCANS.exists():
        return []
    with NEW_SCANS.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_new_scans(rows: list[dict]) -> None:
    with NEW_SCANS.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=NEW_SCANS_HEADER)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in NEW_SCANS_HEADER})


def pending_scan_row(register_id: str, filename: str) -> dict:
    pages = pages_from_filename(filename)
    return {
        "register": register_id,
        "source_image": filename,
        "name": f"New scan — {filename}",
        "page": ", ".join(str(n) for n in pages),
        "book": register_title(register_id),
        "notes": "Detected on Drive; names fill in after automatic transcription",
        "needs_review": "yes",
    }


def upsert_new_scans(queued: list[tuple[str, Path]]) -> int:
    existing = load_new_scans()
    seen = {
        (row.get("register"), (row.get("source_image") or "").upper()) for row in existing
    }
    added = 0
    for register_id, path in queued:
        key = (register_id, path.name.upper())
        if key in seen:
            continue
        existing.append(pending_scan_row(register_id, path.name))
        seen.add(key)
        added += 1
    write_new_scans(existing)
    return added


def remove_new_scan(register_id: str, filename: str) -> None:
    remaining = [
        row
        for row in load_new_scans()
        if not (
            row.get("register") == register_id
            and (row.get("source_image") or "").upper() == filename.upper()
        )
    ]
    write_new_scans(remaining)


def stub_rows(register_id: str, filename: str, header: list[str]) -> list[dict]:
    row = {key: "" for key in header}
    row["register"] = register_id
    row["source_image"] = filename
    row["needs_review"] = "yes"
    row["notes"] = "stub ingest — replace by a real vision transcription"
    if "surname" in row:
        row["surname"] = "Stub"
        row["given_name"] = Path(filename).stem
    if "year" in row:
        row["year"] = "1900"
    return [row]


def transcribe_image(path: Path, register_id: str, header: list[str]) -> list[dict]:
    if os.environ.get("INGEST_STUB"):
        return stub_rows(register_id, path.name, header)
    prompt = build_prompt(register_id, header, path.name)
    image_bytes = resize_jpeg(path)
    if os.environ.get("OPENAI_API_KEY"):
        text = openai_transcribe(image_bytes, prompt)
    elif os.environ.get("ANTHROPIC_API_KEY"):
        text = anthropic_transcribe(image_bytes, prompt)
    elif os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        text = gemini_transcribe(image_bytes, prompt)
    elif copilot_usable():
        text = copilot_transcribe(image_bytes, prompt, path)
    else:
        raise RuntimeError("no vision API key")
    return parse_csv_text(text, header, register_id, path.name)


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem
    return re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_") or "page"


def write_part(register_id: str, filename: str, header: list[str], rows: list[dict]) -> Path:
    PARTS.mkdir(parents=True, exist_ok=True)
    dest = PARTS / f"{register_id}_auto_{safe_stem(filename)}.csv"
    with dest.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    return dest


def merge_parts() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "merge_parts.py")], check=True)


def append_pending(queued: list[tuple[str, Path]], errors: list[str]) -> None:
    extra = []
    if queued:
        extra += ["", "## Local incoming/ images waiting for transcription", ""]
        for register_id, path in queued:
            extra.append(f"- `{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}` → `{register_id}`")
    if errors:
        extra += ["", "## Ingest errors", ""]
        extra.extend(f"- {line}" for line in errors)
    if not extra:
        return
    existing = PENDING.read_text(encoding="utf-8") if PENDING.exists() else "# Pending scans\n"
    if "## Local incoming/" in existing and not errors:
        return
    PENDING.write_text(existing.rstrip() + "\n" + "\n".join(extra) + "\n", encoding="utf-8")


def run_ingest(incoming: Path, dry_run: bool = False) -> dict:
    if not incoming.is_absolute():
        incoming = ROOT / incoming

    has_key = vision_ready()
    queued: list[tuple[str, Path]] = []
    written = 0
    errors: list[str] = []
    rows_added = 0

    for register_id, path in discover_images(incoming):
        if already_transcribed(register_id, path.name):
            print(f"already in CSV: {register_id} {path.name}")
            continue
        header = csv_header(register_id)
        if not header:
            errors.append(f"{path.name}: no CSV header for {register_id}")
            continue
        if not has_key or dry_run:
            queued.append((register_id, path))
            print(f"queued (no API key or dry-run): {register_id} {path.name}")
            continue
        try:
            rows = transcribe_image(path, register_id, header)
        except Exception as exc:  # noqa: BLE001 — surface any provider/parse error
            errors.append(f"{register_id}/{path.name}: {exc}")
            queued.append((register_id, path))
            print(f"FAILED {register_id} {path.name}: {exc}", file=sys.stderr)
            continue
        if not rows:
            print(f"no named rows (blank/title?): {register_id} {path.name}")
            continue
        dest = write_part(register_id, path.name, header, rows)
        written += 1
        rows_added += len(rows)
        remove_new_scan(register_id, path.name)
        print(f"wrote {dest} ({len(rows)} rows)")

    if written:
        merge_parts()
        subprocess.run([sys.executable, str(ROOT / "scripts" / "scan_resume.py")], check=False)

    published = upsert_new_scans(queued) if queued else 0
    append_pending(queued, errors)
    print(f"transcribed_pages={written} queued={len(queued)} errors={len(errors)}")
    if not has_key and queued:
        print(
            "No vision provider. New pages are listed on the website as "
            "'New scan — filename'. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or "
            "GEMINI_API_KEY, or run in GitHub Actions with Copilot, to fill names.",
            file=sys.stderr,
        )
    return {
        "transcribed_pages": written,
        "rows_added": rows_added,
        "queued": len(queued),
        "published_pending": published,
        "errors": len(errors),
        "vision": vision_name(),
        "queued_files": [f"{rid}/{path.name}" for rid, path in queued],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--incoming", default=str(INCOMING))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    incoming = Path(args.incoming)
    if not incoming.is_absolute():
        incoming = ROOT / incoming
    run_ingest(incoming, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
