#!/usr/bin/env python3
"""Copy the bundled front-page image to /output/entry.png (stdlib only)."""
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


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)
    src_hash, out_hash = sha256(SRC), sha256(OUT)
    src_size, out_size = os.path.getsize(SRC), os.path.getsize(OUT)
    if src_hash != out_hash or src_size != out_size:
        print(f"verification FAILED: src {src_size}B {src_hash} vs out {out_size}B {out_hash}", file=sys.stderr)
        sys.exit(1)
    print(f"wrote {OUT} ({out_size} bytes, sha256 {out_hash[:16]}...) — verified identical to source")


if __name__ == "__main__":
    main()
