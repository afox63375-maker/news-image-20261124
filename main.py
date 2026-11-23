#!/usr/bin/env python3
"""Entrypoint for the Tuesday 24 November 2026 front page.

Standard library only. It checks the bundled entry.png (PNG signature,
chunk CRCs, an IHDR no larger than 1024x1024, at most 1 MiB, at least one
IDAT chunk, IEND last) and copies the bytes unchanged to
$MAKEFUN_OUTPUT_DIR/entry.png (default ./output).

The copy is byte-for-byte, so two runs produce identical output.

Run:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024
MAX_EDGE = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class EntryError(Exception):
    """Raised when the bundled image fails a validity check."""


def read_chunks(data):
    """Yield (type, payload) for every chunk, verifying each CRC."""
    if data[:8] != PNG_SIGNATURE:
        raise EntryError("not a PNG file: bad signature")
    pos = 8
    while pos < len(data):
        if pos + 8 > len(data):
            raise EntryError("truncated chunk header")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            raise EntryError("truncated %s chunk" % ctype.decode("latin1"))
        payload = data[pos + 8:pos + 8 + length]
        stored_crc = struct.unpack(">I", data[pos + 8 + length:end])[0]
        actual_crc = zlib.crc32(ctype + payload) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            raise EntryError("CRC mismatch in %s chunk"
                             % ctype.decode("latin1"))
        yield ctype, payload
        pos = end


def check_image(data):
    """Run every structural check; return (width, height)."""
    if len(data) > MAX_BYTES:
        raise EntryError("entry.png is %d bytes, over the 1 MiB limit"
                         % len(data))
    chunks = list(read_chunks(data))
    if not chunks or chunks[0][0] != b"IHDR":
        raise EntryError("first chunk is not IHDR")
    if chunks[-1][0] != b"IEND":
        raise EntryError("last chunk is not IEND")
    width, height = struct.unpack(">II", chunks[0][1][:8])
    if width > MAX_EDGE or height > MAX_EDGE:
        raise EntryError("image is %dx%d, larger than 1024x1024"
                         % (width, height))
    if width < 1 or height < 1:
        raise EntryError("image has a zero dimension")
    types = [c for c, _ in chunks]
    if b"IDAT" not in types:
        raise EntryError("no IDAT chunk: no pixel data")
    return width, height


def main():
    try:
        with open(SOURCE, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        print("error: cannot read entry.png: %s" % exc, file=sys.stderr)
        return 1
    try:
        width, height = check_image(data)
    except EntryError as exc:
        print("error: entry.png failed validation: %s" % exc, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.png")
        with open(target, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        print("error: cannot write output: %s" % exc, file=sys.stderr)
        return 1

    print("entry.png: %dx%d, %d bytes, checks passed; wrote %s"
          % (width, height, len(data), target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
