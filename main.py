#!/usr/bin/env python3
"""news-image-20261119 entrypoint: copy the built broadsheet to /output.

The image (entry.png beside this file) sums up Thursday 19 November 2026's
world news as a front page. Standard library only; no network; deterministic:
every run writes the same bytes. Run with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"IEND"
MAX_BYTES = 1048576  # the gate caps the image at 1 MiB


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if not data.startswith(PNG_MAGIC):
        sys.exit("entry.png is not a PNG")
    if PNG_IEND not in data[-12:]:
        sys.exit("entry.png has no IEND chunk")
    if len(data) > MAX_BYTES:
        sys.exit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
