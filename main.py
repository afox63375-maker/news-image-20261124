#!/usr/bin/env python3
"""Validate entry.png and copy it unchanged to the output directory.

Standard library only: os, sys, struct, zlib, hashlib. Nothing else is
imported, because the competition allows only the standard library here.

What it checks before copying:
  * entry.png sits next to this file and is a real PNG (magic bytes);
  * the IHDR chunk says exactly 1024 x 1024;
  * the file is smaller than 1 MiB;
  * every PNG chunk's CRC matches (zlib.crc32 over type + data);
  * the copied file's sha256 equals the source's.

The destination is $MAKEFUN_OUTPUT_DIR/entry.png; when the variable is
not set, ./output/entry.png next to this file is used instead.
Run:  python3 main.py [--check-only]
With --check-only, validation runs but nothing is copied.
"""

import hashlib
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
EXPECT_W, EXPECT_H = 1024, 1024
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("main.py: error: %s" % message, file=sys.stderr)
    raise SystemExit(2)


def read_png_chunks(data):
    """Yield (type, payload) for each chunk; raise on bad structure/CRC."""
    if data[:8] != PNG_MAGIC:
        fail("entry.png is not a PNG file (bad magic bytes)")
    pos = 8
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated PNG chunk header at offset %d" % pos)
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail("truncated PNG chunk %r at offset %d"
                 % (ctype.decode("latin-1"), pos))
        payload = data[pos + 8:pos + 8 + length]
        crc_stored = struct.unpack(">I", data[pos + 8 + length:end])[0]
        crc_actual = zlib.crc32(ctype)
        crc_actual = zlib.crc32(payload, crc_actual) & 0xFFFFFFFF
        if crc_actual != crc_stored:
            fail("chunk %r has a bad CRC (stored %08x, actual %08x)"
                 % (ctype.decode("latin-1"), crc_stored, crc_actual))
        yield ctype, payload
        pos = end
        if ctype == b"IEND":
            if pos != len(data):
                fail("trailing bytes after IEND chunk")
            return
    fail("PNG ended without an IEND chunk")


def validate(data):
    """Return (width, height) after the structural checks pass."""
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    width = height = None
    for ctype, payload in read_png_chunks(data):
        if ctype == b"IHDR":
            if len(payload) != 13:
                fail("IHDR chunk has the wrong length")
            width, height = struct.unpack(">II", payload[:8])
    if width is None:
        fail("PNG has no IHDR chunk")
    if (width, height) != (EXPECT_W, EXPECT_H):
        fail("entry.png is %dx%d, expected %dx%d"
             % (width, height, EXPECT_W, EXPECT_H))
    return width, height


def main(argv):
    check_only = "--check-only" in argv
    if not os.path.isfile(SOURCE):
        fail("entry.png not found next to main.py: %s" % SOURCE)
    with open(SOURCE, "rb") as handle:
        data = handle.read()
    width, height = validate(data)
    digest = hashlib.sha256(data).hexdigest()
    print("entry.png: %dx%d, %d bytes, sha256 %s"
          % (width, height, len(data), digest))
    if check_only:
        print("check-only: not copied")
        return 0

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as handle:
        handle.write(data)
    with open(dest, "rb") as handle:
        copied = handle.read()
    if hashlib.sha256(copied).hexdigest() != digest:
        fail("copied file's sha256 does not match the source")

    print("copied unchanged to %s (sha256 match)" % dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
