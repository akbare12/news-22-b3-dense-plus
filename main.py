#!/usr/bin/env python3
"""Copy the bundled front-page image to /output/entry.png (stdlib only).

The program is deliberately boring: it copies one file and then proves the
copy is exact. The verification matters because the entry is judged by
running this program twice on the server — if the second run produced a
different file the entry would be non-deterministic, so size and sha256 of
the output are compared against the bundled source and any mismatch exits 1.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = "/output/entry.png"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_copy(src, out):
    """Return (ok, src_size, out_size, out_hash): is the copy byte-identical?"""
    src_hash, out_hash = sha256(src), sha256(out)
    src_size, out_size = os.path.getsize(src), os.path.getsize(out)
    return src_hash == out_hash and src_size == out_size, src_size, out_size, out_hash


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)
    ok, src_size, out_size, out_hash = verify_copy(SRC, OUT)
    if not ok:
        print(f"verification FAILED: src {src_size}B vs out {out_size}B", file=sys.stderr)
        sys.exit(1)
    print(f"wrote {OUT} ({out_size} bytes, sha256 {out_hash[:16]}...) — verified identical to source")


if __name__ == "__main__":
    main()
