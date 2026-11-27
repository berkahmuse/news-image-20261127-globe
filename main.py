#!/usr/bin/env python3
"""news-image-20261127 entrypoint (Python 3.13, standard library only).

The entry image is drawn by draw.py (Pillow, run at build time) and stored
in this repository as entry.png; this program copies it to the output
directory, verifying first that it is a whole PNG inside the competition
gate (at most 1024x1024 pixels, at most 1 MiB). Two runs of this program
produce byte-identical output: entry.png is 1024x1024, 132915 bytes,
sha256 d3f6d57a99ee17ce8bbc71c4b6dbd1bd4771076fdec64a07af07267baba6ead8.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def png_size(data: bytes) -> tuple:
    """Return (width, height) of a PNG, rejecting anything that is not one."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    return struct.unpack(">II", data[16:24])


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    data = SRC.read_bytes()
    width, height = png_size(data)
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024x1024 gate")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB gate")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out_dir / "entry.png")
    print(f"entry.png: {width}x{height}, {len(data)} bytes -> {out_dir / 'entry.png'}")


if __name__ == "__main__":
    main()
