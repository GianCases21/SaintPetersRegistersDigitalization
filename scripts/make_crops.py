#!/usr/bin/env python3
"""Generate enhanced, readable page crops from raw register scans.

Each two-page spread scan produces a left and right crop, contrast/brightness
enhanced for transcription. Single-page scans produce one crop.

Usage:
    python3 scripts/make_crops.py SRC_DIR OUT_DIR [--single-page NAMES...]
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageEnhance


def enhance(im: Image.Image, max_width: int = 1600) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.5)
    im = ImageEnhance.Brightness(im).enhance(1.25)
    if im.width > max_width:
        ratio = max_width / im.width
        im = im.resize((max_width, int(im.height * ratio)), Image.LANCZOS)
    return im


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src")
    parser.add_argument("out")
    parser.add_argument("--single-page", nargs="*", default=[],
                        help="filenames that are single pages, not spreads")
    args = parser.parse_args()

    src, out = Path(args.src), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    singles = set(args.single_page)

    images = sorted(p for p in src.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
    if not images:
        sys.exit(f"no images in {src}")

    for img_path in images:
        stem = img_path.stem.replace(" ", "_")
        im = Image.open(img_path)
        w, h = im.size
        if img_path.name in singles:
            targets = [(im.crop((int(w * 0.03), 0, int(w * 0.97), h)), f"{stem}.jpg")]
        else:
            targets = [
                (im.crop((int(w * 0.04), 0, int(w * 0.56), h)), f"{stem}_L.jpg"),
                (im.crop((int(w * 0.48), 0, int(w * 0.99), h)), f"{stem}_R.jpg"),
            ]
        for crop, name in targets:
            dest = out / name
            if dest.exists():
                continue
            enhance(crop).save(dest, quality=88)
        print(stem)


if __name__ == "__main__":
    main()
