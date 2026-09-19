#!/usr/bin/env python3
"""Sanity checks for Drive path mapping and photographer resume stats."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from register_catalog import analyze_register, load_manifest, map_drive_path
from watch_drive import extract_new_images_from_zip, skip_archive


def _by_id() -> dict:
    return {item["id"]: analyze_register(item) for item in load_manifest()}


def main() -> None:
    mapping = {
        "incoming/baptism_2011/PAGE 068.JPG": "baptism_2011",
        "Baptism 2011-/PAGE 047.JPG": "baptism_2011",
        "Baptism 1839-1875/PAGE 133.JPG": "baptism_1839",
        "Baptism 1839-1875/PAGE 134.JPG": "funerals_1868",
        "Baptism 1839-1875/PAGE 140.JPG": "confirmation_early",
        "incoming/baptism_1839/PAGE 147.JPG": "confirmation_early",
        "Marriage 1937-1963/PAGE 059.JPG": "marriage_1937",
        "incoming/confirmation_2015/PAGE 4.JPG": "confirmation_2015",
        "Confirmation 2015-/PAGE 22.JPG": "confirmation_2015",
        "TITLE.JPG": None,
        "St. Joseph Section 1939/PAGE 067.JPG": "st_joseph_section_1939",
        "Baptism Registers/Baptism 2011-/PAGE 068.JPG": "baptism_2011",
        "Marriage Registers/Marriage 1937-1963/PAGE 059.JPG": "marriage_1937",
        "Death Registers/Death C 1924-1964/PAGE 047.JPG": "death_c_1924",
    }
    failed = 0
    for path, expected in mapping.items():
        got = map_drive_path(path)
        if got != expected:
            print(f"FAIL map {path!r}: expected {expected!r} got {got!r}")
            failed += 1

    stats = _by_id()

    def expect(register_id: str, attr: str, needle: str) -> None:
        nonlocal failed
        value = str(stats[register_id].get(attr) or "")
        if needle.lower() not in value.lower():
            print(f"FAIL {register_id}.{attr}: expected to contain {needle!r}, got {value!r}")
            failed += 1

    expect("baptism_1839", "last_name", "Early, John")
    expect("baptism_1839", "last_date_text", "1875")
    expect("marriage_1937", "last_name", "Collumb")
    expect("marriage_1937", "last_name", "Gartland")
    expect("baptism_2011", "last_name", "Hernandez, Gianna Marie")
    expect("confirmation_2015", "last_name", "Yeye")
    expect("marriage_2009", "last_name", "Velasquez")
    expect("marriage_1840", "last_name", "McKenna")
    if stats["confirmation_2015"]["holes"] != [4, 15]:
        print(f"FAIL confirmation_2015 holes {stats['confirmation_2015']['holes']}")
        failed += 1
    if stats["marriage_2009"]["holes"] != [18]:
        print(f"FAIL marriage_2009 holes {stats['marriage_2009']['holes']}")
        failed += 1

    if not skip_archive("NEW 2023-2024 UPDATED-20260817T172911Z-1-001.zip"):
        print("FAIL skip_archive should skip the duplicate 2023 dump")
        failed += 1
    if skip_archive("Baptism Registers-20260817T172854Z-1-003.zip"):
        print("FAIL skip_archive should not skip Baptism Registers.zip")
        failed += 1

    import tempfile
    import zipfile

    tmp = Path(tempfile.mkdtemp(prefix="zip_ingest_"))
    zip_path = tmp / "sample.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("Baptism 2011-/PAGE 068.JPG", b"new-page")
        zf.writestr("Baptism 2011-/PAGE 046.JPG", b"already")
        zf.writestr("Baptism 2011-/TITLE.JPG", b"skip-me")
    dest = tmp / "incoming"
    extracted = extract_new_images_from_zip(
        zip_path,
        dest,
        {"baptism_2011": {"PAGE 046.JPG"}},
        "Baptism Registers.zip",
        10,
    )
    names = {row["name"] for row in extracted}
    if names != {"PAGE 068.JPG"}:
        print(f"FAIL zip extract names {names}")
        failed += 1
    copied = dest / "baptism_2011" / "PAGE 068.JPG"
    if not copied.exists() or copied.read_bytes() != b"new-page":
        print("FAIL zip extract did not copy PAGE 068.JPG")
        failed += 1

    if failed:
        raise SystemExit(f"{failed} check(s) failed")
    print(f"ok ({len(mapping)} maps, {len(stats)} registers)")


if __name__ == "__main__":
    main()
