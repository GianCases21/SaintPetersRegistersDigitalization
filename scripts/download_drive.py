#!/usr/bin/env python3
"""Download the scanned register images from the shared Google Drive folder.

Usage:
    python3 scripts/download_drive.py [--url FOLDER_URL] [--out DIR]

Zips found in the folder are extracted automatically.
"""

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

DEFAULT_URL = "https://drive.google.com/drive/folders/1JyB49OP-yAV43iojbGje6cwvLNFPdvZj"
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "drive_sample"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="Google Drive folder URL")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [sys.executable, "-m", "gdown", "--folder", args.url, "--continue"],
        cwd=out,
    )
    if result.returncode != 0:
        sys.exit("gdown failed - check that the folder is shared as 'Anyone with the link'.")

    for zip_path in out.rglob("*.zip"):
        dest = zip_path.with_suffix("")
        if dest.exists():
            continue
        print(f"Extracting {zip_path.name} -> {dest}")
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest)


if __name__ == "__main__":
    main()
