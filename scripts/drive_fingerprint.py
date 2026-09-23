"""Fingerprints public Google Drive files without downloading them.

Large files show a virus-scan interstitial that includes a rounded size
label; posting the confirm form then returns an exact Content-Length header
before any zip bytes are saved.
"""

from __future__ import annotations

import re
from typing import Any

SIZE_RE = re.compile(r'class="uc-name-size"[^>]*>.*?\(([^)]+)\)', re.S)
UUID_RE = re.compile(r'name="uuid"\s+value="([^"]+)"')


def parse_interstitial(html: str) -> dict[str, str]:
    label = ""
    match = SIZE_RE.search(html)
    if match:
        label = match.group(1).strip()
    uuid = ""
    match = UUID_RE.search(html)
    if match:
        uuid = match.group(1).strip()
    return {"label": label, "uuid": uuid}


def fingerprint_file(file_id: str, timeout: int = 30) -> dict[str, Any]:
    """Return {size, label} for a public Drive file. size may be None."""
    import requests

    session = requests.Session()
    session.headers["User-Agent"] = "SaintPetersRegistersIngest/1.0"
    first = session.get(
        f"https://drive.google.com/uc?export=download&id={file_id}",
        timeout=timeout,
    )
    first.raise_for_status()
    ctype = (first.headers.get("content-type") or "").lower()
    if "text/html" not in ctype:
        length = first.headers.get("content-length")
        return {"size": int(length) if length and length.isdigit() else None, "label": ""}

    parsed = parse_interstitial(first.text)
    if not parsed["uuid"]:
        return {"size": None, "label": parsed["label"]}

    second = session.get(
        "https://drive.usercontent.google.com/download",
        params={
            "id": file_id,
            "export": "download",
            "confirm": "t",
            "uuid": parsed["uuid"],
        },
        timeout=timeout,
        stream=True,
    )
    length = second.headers.get("content-length")
    second.close()
    return {
        "size": int(length) if length and length.isdigit() else None,
        "label": parsed["label"],
    }


def fingerprint_files(files: list[dict], kinds: set[str] | None = None) -> list[dict]:
    """Add size/label onto each listing row. kinds defaults to zip only."""
    wanted = kinds if kinds is not None else {"zip"}
    out = []
    for row in files:
        extra = {"size": row.get("size"), "label": row.get("label") or ""}
        if row.get("kind") in wanted and row.get("id"):
            try:
                extra = fingerprint_file(row["id"])
                print(f"fingerprint {row.get('name')}: size={extra.get('size')} label={extra.get('label')}")
            except Exception as exc:  # noqa: BLE001
                print(f"fingerprint failed {row.get('name')}: {exc}")
        out.append({**row, **extra})
    return out
